import os, subprocess, sys

### Import Interface Module
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)
import interface
 
class Flake8Implementation(interface.StaticCodeAnylazer):
    def scan_file(self, file_path, output_path):
        if not os.path.isfile(file_path) or not os.path.isfile(output_path):
            return
        os.popen(f'flake8 {file_path} --output-file {output_path}')
        