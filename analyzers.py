import os, sys

### Import Interface Module
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)
import interface
 
from pylint.lint import Run

class PylintImplementation(interface.StaticCodeAnylazer):
    def scan_file(self, path, output_path):
        sys.stdout = open(output_path, 'w')
        results = Run([path], do_exit=False)

class PyflakesImplementation(interface.StaticCodeAnylazer):
    def scan_file(self, file_name, output_path):
        if not os.path.isfile(file_name) or not os.path.isfile(output_path):
            return
        os.popen(f'echo "" > {output_path}')
        os.popen(f'pyflakes {file_name} >> {output_path}')
    
 
class Flake8Implementation(interface.StaticCodeAnylazer):
    def scan_file(self, file_path, output_path):
        if not os.path.isfile(file_path) or not os.path.isfile(output_path):
            return
        os.popen(f'echo "" > {output_path}')
        os.popen(f'flake8 {file_path} --output-file {output_path}')
        

class BanditImplementation(interface.StaticCodeAnylazer):
    def scan_file(self, file_path, output_path):
        if not os.path.isfile(file_path) or not os.path.isfile(output_path):
            return
        os.popen('bandit ' + file_path + '-f txt -o ' + output_path)

        



