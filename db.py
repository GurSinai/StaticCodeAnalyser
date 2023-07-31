import os, json
DB_FILE = 'PROJECTS'

def create_new_proj(proj_name):
    saved = []
    if not os.path.isfile(DB_FILE):
        saved = read_projects(DB_FILE)
    with open(DB_FILE, 'w') as out:
        myJson = json.loads('{}')

"""
def write_user(file_name, username, psw, salt):
    saved=[]
    if os.path.isfile(file_name):
        saved = read_users(file_name)
    with open(file_name, 'w') as out:
        myJson = json.loads('{"name":"'+username+'", "password":"'+psw+'", "salt":"'+salt+'"}')
        saved.append(myJson)
        json.dump(saved, out, indent=1)
        out.close()

def read_users(file_name):
    if not os.path.isfile(file_name):
        return []
    with open(file_name, 'r') as openfile:
        read_data=openfile.read();
        # Opening a file, and checking if it is empty
        if (read_data == ''):
             return []
        json_obj=json.loads(read_data)
        return json_obj


### WRITING A NEW USER


### GETTING A SPESIFIC USER REGISTRY
def get_user(file_name, name_req):
    users=read_users(file_name)
    for user in users:
        if name_req == user['name']:
            return user
    return None
"""