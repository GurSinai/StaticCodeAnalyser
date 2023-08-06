import openai, os, sys


parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)

from analyzers import BanditImplementation, Flake8Implementation, PylintImplementation, PyflakesImplementation
file_ts = './ex1.py'
PylintI = PylintImplementation()
BanditI = BanditImplementation()
FlakeI = Flake8Implementation()
flakesI = PyflakesImplementation()
STA = []
STA.append(BanditI)
STA.append(FlakeI)
STA.append(flakesI)
STA.append(PylintI)


def scan_file(file_path):
    pass