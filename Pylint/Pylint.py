import os, subprocess, sys

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


