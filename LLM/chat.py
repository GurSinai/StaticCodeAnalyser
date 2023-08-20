import openai, os, sys, json, base64
import time
from threading import Lock
from dotenv import load_dotenv
load_dotenv()

# IMPORT ANALIZERS FROM ABOVE DIRECTORY
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory)
from analyzers import BanditImplementation, Flake8Implementation, PylintImplementation, PyflakesImplementation

# Set basic directories
Scan_basedir = './LLM'
scan_summaries_dir = './LLM/scans_summary'
chat_fix_dir = './LLM/fixes'

# Load enviornment variables and setup anylizers
openai.api_key = os.getenv("CHAT_API_KEY")
PylintI = PylintImplementation()
BanditI = BanditImplementation()
FlakeI = Flake8Implementation()
flakesI = PyflakesImplementation()
STA = []
OUT_Paths = []
STA.append(BanditI)
OUT_Paths.append(Scan_basedir + '/Bandit/')
STA.append(FlakeI)
OUT_Paths.append(Scan_basedir + '/Flake8/')
STA.append(flakesI)
OUT_Paths.append(Scan_basedir + '/Pyflakes/')
STA.append(PylintI)
OUT_Paths.append(Scan_basedir + '/Pylint/')

########## DB MANAGEMENT ֳֳֳֳֳֳ##########
def list_directory_recursive(directory_path):
    """
    List every file under the directory path recieved, recursivly.
    """
    files = []
    listsdir = os.listdir(directory_path)
    for item in listsdir:
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            temp = list_directory_recursive(item_path)
            for file in temp:
                files.append(file)
        else:
            files.append(item_path)
    return files

def get_normalized_path(path):
    """
    This is a one way, One-To-One function to allow to saving a file with it's path as it's name.
    It removes : and does the following replacements: \ -> / , // -> /, / -> -
    It addition, turns file.type into filetype.txt
    """
    return path[::-1].replace('.', '', 1)[::-1].replace('\\', '/').replace('//', '/').replace(':', '').replace('/', '-') + '.txt'

fixes_lock = Lock()

def reset_scans_file(file):
    saved = []
    with open(file, 'w') as out:
        json.dump(saved, out, indent=1)
        out.close()


def add_fix(file, fix, fix_idx):
    saved = {}
    if os.path.isfile(file):
        saved = read_all_db_json(file)   
    with open(file, 'w') as out:
        fixes_lock.acquire()
        json_obj = json.loads(r'{"'+str(fix_idx)+'":"'+base64.b64encode(bytes(fix, encoding='utf-8')).decode()+'"}')
        saved = {**saved, **json_obj}
        json.dump(saved, out, indent=1)
        fixes_lock.release() 
        out.close()


def append_to_scans(file, str) -> bool:
    saved = []
    if os.path.isfile(file):
        saved = read_all_db(file)    
    with open(file, 'w') as out:
        saved.append(str)
        json.dump(saved, out, indent=1)
        out.close()


def read_all_db_json(file) -> list:
    if not os.path.isfile(file):
        return {}
    fixes_lock.acquire()
    with open(file, 'r') as openfile:
        read_data = openfile.read()
        openfile.close()
        fixes_lock.release() 
        if read_data == '':
            return {}
        json_obj = json.loads(read_data)
        return json_obj
    

def read_all_db(file) -> list:
    if not os.path.isfile(file):
        return []
    with open(file, 'r') as openfile:
        read_data = openfile.read()
        if read_data == '':
            return []
        json_obj = json.loads(read_data)
        return json_obj


def scan_file(file_path):
    """
    Append the scan from each STA to it's corrisponding folder in Outpaths/norm-file-path
    """
    for i, sta in enumerate(STA):
        temp = get_normalized_path(file_path)
        f = open(OUT_Paths[i] + f'/{temp}', 'w')
        f.close()
        time.sleep(0.1)
        sta.scan_file(file_path, OUT_Paths[i] + f'/{temp}')
    time.sleep(0.1)
    summarize_fixes(file_path)


def scan_project(project_path, files):
    """
    Scan each file inside project
    """
    for file in files:
        scan_file(project_path + '/' + file)


def summarize_fixes(abs_file_path):
    """
    Reset the scan summeries file and fetch scans from each STA, into a summary list
    Reset fixes file
    """
    norm_path = get_normalized_path(abs_file_path)
    reset_scans_file(scan_summaries_dir+ '/' + norm_path)
    for i, sta in enumerate(STA):
        path = OUT_Paths[i] + norm_path
        time.sleep(0.5)
        try:
            f = open(path, encoding='utf-8')
            content = f.read()
        except UnicodeDecodeError:
            f = open(path,'r')
            content = f.read() 
        errors = sta.split_output(content)
        for error in errors:
            append_to_scans(scan_summaries_dir + '/' + norm_path, sta.get_name())
            append_to_scans(scan_summaries_dir + '/' + norm_path, error)
    f = open(chat_fix_dir + '/' + norm_path, 'w')
    f.close()


def generate_prompt(sta_name, error):
    """
    Generates the prompt for chat-gpt to use
    """
    prompt = f"using the Static code anylizer \"{sta_name}\" i got this error:\n" + error \
            + "\nGive me a short and informed explanation on how to fix it. No more than 200 chars"
    return prompt


def request_file_fix(norm_path, error_idx):
    """
    Send a request for a fix from chat-gpt
    based on the file, and the error index.
    (The STA's name is always saved as the index before!)
    Scans are saved in Base64 to avoid escape character saving
    """
    scan = read_all_db(scan_summaries_dir + '/' + norm_path)
    fix = chat_with_gpt3(generate_prompt(scan[int(error_idx)-1], scan[int(error_idx)]))
    add_fix(chat_fix_dir + '/' + norm_path, fix, error_idx)
    return read_all_db(chat_fix_dir + '/' + norm_path)


def delete_scans(project_path, file_name):
    """
    Delete all scans CURRENTLY assosiated with a projects
    """
    norm = get_normalized_path(project_path + file_name)
    for path in OUT_Paths:
        try:
            os.remove(path + '/' + norm)
        except FileNotFoundError:
            print(f"No Scan Available at {path}")
    try:
        os.remove(scan_summaries_dir + '/' + norm)
    except FileNotFoundError:
        print(f"No Scan Available at {scan_summaries_dir}")
    try:
        os.remove(chat_fix_dir + '/' + norm)
    except FileNotFoundError:
        print(f"No Scan Available at {chat_fix_dir}")


def chat_with_gpt3(prompt):
    """
    Receive a responce from chat-gpt-3.5-turbo based on prompt saved.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt},
            ]
    )
    return response['choices'][0]['message']['content']
