import os, json
from LLM.chat import list_directory_recursive
DB_FILE = 'PROJECTS.JSON'

########## UTIL METHODS ##########
def overwrite_db(projects):
    with open(DB_FILE, 'w') as out:
        json.dump(projects, out, indent=1)

def is_alphanumeric_with_spaces(s):
    return all(c.isalnum() or c.isspace() for c in s)

def create_new_proj(proj_name, basedir, lang="", desc="", add_files=True, ignores = []) -> bool:
    """
    Args:
        proj_name (str): must be alphanumeric with spaces
        lang (str, optional): Defaults to "".
        desc (str, optional): Defaults to "".
        basedir (str): Must be a folder.
        add_files (bool, optional): Add files from basedir. Defaults to True.
        ignores (list, optional): List of patterns to ignore when adding files.
            '/path' will ignore every file beiginning with '/path',
            'str' will ignore every path containing 'str'
            Defaults to [].
    will add project according to parameters
    Returns:
        True of succsessful
    """
    if not is_alphanumeric_with_spaces(proj_name) or not os.path.isdir(basedir) or basedir == "":
        return False
    if get_project(proj_name) is not None:
        return False
    saved = []
    if len(ignores) == 1 and ignores[0] == '': # check if ignores is empty and make it array
        ignores == []
    
    basedir = basedir.replace('\\', '/') # translate backslashes into forwardslashes to allow for saving
    if os.path.isfile(DB_FILE):
        saved = read_all_projects()
    
    with open(DB_FILE, 'w') as out:
        myJson = json.loads('{"name":"'+proj_name+'", "files":[], "basedir":"'+basedir+'", "lang":"'+lang+'", "desc":"'+desc+'"}')
        saved.append(myJson)
        json.dump(saved, out, indent=1)
        out.close()

    if add_files:
        file_counter = 0
        files = list_directory_recursive(basedir)
        for file in files:
            file = file.replace('\\', '/').removeprefix(basedir)
            if file[-3:] == '.py' and not check_excluded(ignores, file):
                add_file_to_project(proj_name, file.replace('\\', '/').removeprefix(basedir))
                file_counter += 1
                if file_counter >= 500:
                    break;
    return True

def check_excluded(ignores, file):
    """
    Args:
        ignores (list of str): list of list to ignore
        file (path): files to check 
    Returns:
        True if and only if file should be ignored
    """
    for ignore in ignores:
        if ignore[0:1] == '/':
            if file[0:len(ignore)] == ignore:
                return True
        else:
            if file.__contains__(ignore):
                return True
    return False

def read_all_projects() -> list:
    """
    Returns:
        list: Project as dictionaries
    """
    if not os.path.isfile(DB_FILE):
        return []
    with open(DB_FILE, 'r') as openfile:
        read_data = openfile.read()
        if read_data == '':
            return []
        json_obj = json.loads(read_data)
        return json_obj

def get_project(name) -> json:
    projects = read_all_projects()
    for project in projects:
        if project['name'] == name:
            return project
    return None
        
def get_project_files(name) -> list:
    return get_project(name)['files']

def remove_project(name):
    temp = read_all_projects()
    projects = temp.copy()
    for project in temp:
        if project['name'] == name:
            projects.remove(project)
    overwrite_db(projects)

def add_file_to_project(proj_name, path):
    projects = read_all_projects()
    for project in projects:
        if project['name'] == proj_name:
            for file in project['files']:
                if file == path:
                    return False
            project['files'].append(path)
            with open(DB_FILE, 'w') as out:
                json.dump(projects, out, indent=1)
            return True
    return False

def remove_file_from_project(proj, path):
    projects = read_all_projects()
    for project in projects:
        if project['name'] == proj:
            for file in project['files']:
                if file == path:
                    project['files'].remove(file)
                    overwrite_db(projects)
                    return True
            return False
    return False