import os

class PylintImplementation():
    def get_name(self):
        return "Pylint"

    def scan_file(self, path, output_path):
        if not os.path.isfile(path):
            return

        os.popen(f'Pylint \"{path}\" > \"{output_path}\"')

    def split_output(self, content):
        errors = content.split('------------------------------------------------------------------')[0]
        errors = content.split('\n')
        errors = errors[1:-5]
        return errors


class PyflakesImplementation( ):
    def get_name(self):
        return "Pyflakes"
    
    def scan_file(self, file_name, output_path):
        if not os.path.isfile(file_name):
            return
        os.popen(f'pyflakes \"{file_name}\" >> \"{output_path}\"')

    def split_output(self, content):
        errors = content.split('\n')
        errors = errors[0:-1]
        return errors
    
 
class Flake8Implementation( ):
    def get_name(self):
        return "Flake8"
    
    def scan_file(self, file_path, output_path):
        if not os.path.isfile(file_path):
            return
        os.popen(f'flake8 \"{file_path}\" --format pylint --output-file \"{output_path}\"')
    
    def split_output(self, content):
        errors = content.split('\n')
        errors = errors[0:-1]
        return errors

class BanditImplementation( ):
    def get_name(self):
        return "Bandit"

    def scan_file(self, file_path, output_path):
        if not os.path.isfile(file_path):
            return
        os.popen('bandit \"' + file_path + '\" -f custom --msg-template "Line {line}: {test_id}. Severity: {severity} {msg}" -o \"' + output_path + '\"')

    def split_output(self, content):
        if content.__contains__('No issues identified.'):
            return []
        content = content.split('\n')
        content = content[0:-1]
        return content

        



