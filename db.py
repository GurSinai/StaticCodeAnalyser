import os, json
DB_FILE = 'PROJECTS'

def overwrite_db(projects):
    with open(DB_FILE, 'w') as out:
        json.dump(projects, out, indent=1)

def create_new_proj(proj_name, lang=None, desc=None) -> bool:
    if get_project(proj_name) is not None:
        return False
    saved = []
    if os.path.isfile(DB_FILE):
        saved = read_all_projects()
    with open(DB_FILE, 'w') as out:
        if lang == None: lang=""
        if desc == None: desc=""
        myJson = json.loads('{"name":"' + proj_name + '", "files":[], "lang":"'+lang+'", "desc":"'+desc+'"}')
        saved.append(myJson)
        json.dump(saved, out, indent=1)
        out.close()
    return True

def read_all_projects() -> list:
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

def add_file_to_project(proj, path):
    projects = read_all_projects()
    for project in projects:
        if project['name'] == proj:
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

create_new_proj("Project 1", lang="Python", desc="Test project")
create_new_proj("Project 2", desc="Test project")
create_new_proj("Project 3", lang="Python")
create_new_proj("Project 4")
create_new_proj("Project 5", lang="Python", desc="Test project")
create_new_proj("Project 6", desc="Test project")
create_new_proj("Project 7", lang="Python")
create_new_proj("Project 8")
create_new_proj("Project 9", lang="Python", desc="Test project")
create_new_proj("Project 10", desc="Test project")
create_new_proj("Project 11", lang="Python")
create_new_proj("Project 12")
create_new_proj("Project 13", lang="Python", desc="Test project")
create_new_proj("Project 14", desc="Test project")
create_new_proj("Project 15", lang="Python")
create_new_proj("Project 16")