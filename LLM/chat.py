import openai, os, sys
import time


parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)

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
