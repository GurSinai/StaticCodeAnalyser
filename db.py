import os, json
DB_FILE = 'PROJECTS'

def create_new_proj(proj_name):
    saved = []
    if os.path.isfile(DB_FILE):
        saved = read_all_projects()
    with open(DB_FILE, 'w') as out:
        myJson = json.loads('{"name":"' + proj_name + '", "files":[]}')
        saved.append(myJson)
        json.dump(saved, out, indent=1)
        out.close()

def read_all_projects() -> list:
    if not os.path.isfile(DB_FILE):
        return []
    with open(DB_FILE, 'r') as openfile:
        read_data = openfile.read()
        if read_data == '':
            return []
        json_obj = json.loads(read_data)
        return json_obj

def get_project(name):
    projects = read_all_projects()
    for project in projects:
        if project['name'] == name:
            return project
        
def get_project_files(name):
    return get_project(name)['files']

def remove_project(name):
    projects = read_all_projects(name)
    for project in projects:
        if project['name'] == name:
            projects.remove(project)
"""
### GETTING A SPESIFIC USER REGISTRY
def get_user(file_name, name_req):
    users=read_users(file_name)
    for user in users:
        if name_req == user['name']:
            return user
    return None
"""
create_new_proj("Project 1")
print(get_project("prj3"))
