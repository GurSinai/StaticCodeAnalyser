import openai, os, sys ,fnmatch
import time


parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

file_path = 'myfile.txt'  # Replace this by text of type of analyzer
typeofana="bandit"#change this of each type of code (flake8 and more..)
# Read file content and store it in a string
sendtochatgpt = "fix this problem code from " + typeofana +" usinig minimum words "  +read_file_to_string(file_path)
import openai

api_key = "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"
openai.api_key = api_key

def chat_with_gpt3(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5",  # Use GPT-3.5 engine
        prompt=prompt,
        max_tokens=400  # Adjust as needed to control the response length
    )
    return response['choices'][0]['text']

if __name__ == "__main__":
    # Prompt to send to GPT-3.5
    askcode=sendtochatgpt
    chat_prompt = f"You: {askcode}\nChatGPT: "
    response = chat_with_gpt3(chat_prompt)
    #send the responde to website.
    # Print the response from GPT-3.5
    print("ChatGPT:", response)





from analyzers import BanditImplementation, Flake8Implementation, PylintImplementation, PyflakesImplementation
file_ts = './ex1.py'
PylintI = PylintImplementation()
BanditI = BanditImplementation()
FlakeI = Flake8Implementation()
flakesI = PyflakesImplementation()
Scan_basedir = './LLM'
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

def list_directory_recursive(directory_path):
    files = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            temp = list_directory_recursive(item_path)
            for file in temp:
                files.append(file)
        else:
            files.append(item_path)
    return files

def get_normalized_path(path):
    return path[::-1].replace('.', '', 1)[::-1].replace('\\', '/').replace(':', '').replace(' ', '').replace('/', '-') + '.txt'

def scan_file(file_path):
    for i, sta in enumerate(STA):
        temp = get_normalized_path(file_path)#./LLM-ChatGPT/Bandit/
        os.popen(f'echo  "" > {OUT_Paths[i]}{temp}')#'C-Users-gurgu-OneDrive-שולחןהעבודה-תכנות-שנה5-CyberB-Task1-UniversityOfFlorida-apppy.txt'

        time.sleep(1)
        sta.scan_file(file_path, OUT_Paths[i] + f'/{temp}')

def scan_project(project_path):
    files = list_directory_recursive(project_path)
    for file in files:
        if file[-2:] == 'py':
            scan_file(file)




def find_files_with_string(directory, string):
    typesofA = ['/Pylint/', '/Flake8/', '/Bandit/', '/Pyflakes/']
    vara = ""
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            for i in typesofA:
                if fnmatch.fnmatch(filename, f'*{i}*'):
                    vara=i
                    break
 
    if(vara=='/Pylint/'):
     return 'Pylint'
    if(vara=='/Flake8/'):
     return 'Flake8'  
    if(vara=='/Bandit/'):
     return 'Bandit'
    if(vara=='/Pyflakes/'):
     return 'Pyflakes'
    return "cant find which analyzer use!!"
