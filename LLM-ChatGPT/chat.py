import openai, os, sys


parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)


from Pylint.Pylint import PylintImplementation
PylintI = PylintImplementation()
#PylintI.scan_file('./db.py', 'LLM-ChatGPT/Pylint/scan.txt')

from Bandit.Bandit import BanditImplementation
BanditI = BanditImplementation()
#BanditI.scan_file('./db.py', 'LLM-ChatGPT/Bandit/scan.txt')

from Flake8.Flake8 import Flake8Implementation
FlakeI = Flake8Implementation()
#FlakeI.scan_file('./db.py', 'LLM-ChatGPT/Flake8/scan.txt')

from Pyflakes.Pyflakes import PyflakesImplementation
flakesI = PyflakesImplementation()
flakesI.scan_file('./db.py', 'LLM-ChatGPT/Pyflakes/scan.txt')


def scan_files(project):
    pass