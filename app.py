from flask import Flask, render_template, request, redirect, jsonify
import db
import os
from LLM.chat import scan_project, request_file_fix, scan_file
from LLM.chat import scan_summaries_dir, chat_fix_dir
from LLM.chat import get_normalized_path, read_all_db_json, read_all_db

app = Flask(__name__)


@app.route('/')
def index():
    """
    Returns:
        html: the apps main page, with all projects loaded in.
    """
    return render_template('index.html', projects=db.read_all_projects())

@app.route('/edit_project', methods=['POST'])
def edit_project():
    project_name = request.form.get('project_name')
    project_lang = request.form.get('project_lang')
    project_desc = request.form.get('project_desc')
    project_dir = request.form.get('project_dir')
    keep_files = request.form.get('keepfiles')
    get_new_files = request.form.get('getnewfiles')

    if get_new_files is not None:
        get_new_files = True
        
    current_project = db.get_project(request.form.get('current_name'))
    new_files = current_project['files']

    if project_dir != current_project['basedir'] and keep_files is not None:
        # CANNOT KEEP FILES IF THERE IS A NEW BASE DIRECTORY
        keep_files = False
        return render_template(
        'project.html',
        project=current_project,
        files=current_project['files'],
        alerts=['You cannot move to a new \
                            directory and maintain files with relative paths.'])
    if keep_files is None:
        new_files = []
    
    if (db.get_project(project_name) and project_name != current_project['name']) or project_dir == "":
        return render_template(
        'project.html',
        project=current_project,
        files=current_project['files'],
        alerts=['Something went wrong... Check if you have a project with that name or a bad folder-path']
        )
    db.remove_project(current_project['name'])
    result = db.create_new_proj(
        proj_name=project_name,
        desc=project_desc,
        lang=project_lang,
        basedir=project_dir,
        add_files=get_new_files
        )
    if not result:
        return render_template(
        'project.html',
        project=current_project,
        files=current_project['files'],
        alerts=['Something went wrong... Check if you have a project with that name or a bad folder-path']
        )
    for file in new_files:
        db.add_file_to_project(project_name, file)
        
    return redirect('/')


@app.route('/create_project', methods=['POST'])
def createproject():
    """
    Receives a form with the projects parameters, and creates a new projects
    with all .py files inside
    Returns:
        html: the apps main page, with all projects loaded in.
    """
    project_name = request.form.get('project_name')
    project_lang = request.form.get('project_lang')
    project_desc = request.form.get('project_desc')
    project_dir = request.form.get('project_dir')
    result = db.create_new_proj(
        proj_name=project_name,
        desc=project_desc,
        lang=project_lang,
        basedir=project_dir
        )
    if not result:
        return render_template(
            'index.html',
            projects = db.read_all_projects(),
            alerts=['Something went wrong... Check if you have a project with that name or a bad folder-path']
        )
    return redirect('/')

@app.route('/deleteproject/<project>')
def delete_project(project):
    db.remove_project(project)
    return redirect('/')

@app.route('/viewproject/<project>')
def view_project(project):
    """
    Args:
        project (string): the name of the requested projects.

    Returns:
        html: containing the projects view
    """
    return render_template(
        'project.html',
        project=db.get_project(project),
        files=db.get_project_files(project)
        )


@app.route('/getscan/<project_name>/<file>')
def get_file_scan(project_name, file):
    """
    Args:
        project_name (string): the project's name
        file (string): the file's relative path

    Returns:
        The scan results of 'file' under 'project'
    """
    project = db.get_project(project_name)
    nor = get_normalized_path(project['basedir'] + file)
    output = read_all_db(scan_summaries_dir + '/' + nor)
    for i, scan in enumerate(output):
        output[i] = scan.replace('\\', '/')
    return jsonify(output)


@app.route('/generatefix/<project_name>/<file>/<error_index>', methods=['GET'])
def generate_fix(project_name, file, error_index):
    """_summary_
    Args:
        project_name (string): the project's name
        file (string): the file's relative path
        error_index (int): the index of the error inside the scan summary
    Returns:
        Chat gpt's fix for the error
    """
    project = db.get_project(project_name)
    norm = get_normalized_path(project['basedir'] + file)
    request_file_fix(norm, error_index)
    return jsonify(read_all_db_json(chat_fix_dir + '/' + norm)[error_index])


@app.route('/getfixes/<project_name>/<file>')
def get_fixes(project_name, file):
    """_summary_
    Args:
        project_name (string)
        file (string): file name with all '/' replaced with '-' to allow for url parameters using GET
    Returns:
        A list of all errors
    """
    project = db.get_project(project_name)
    norm = get_normalized_path(project['basedir'] + file)
    return jsonify(read_all_db_json(chat_fix_dir + '/' + norm))


@app.route('/addfile', methods=['POST'])
def add_file_to_project():
    """Add a file to the projects
    receives a file and project name through form

    redirects back to /viewproject/<project name>
    """
    file = request.form.get('path')
    project_name = request.form.get('project_name')
    project = db.get_project(project_name)

    # CHECK if file received is a relatuve file path, and if it is, add it!
    if (file != "" and file is not None and
         os.path.isfile(project['basedir'] + '/' + file)):
        db.add_file_to_project(project_name, file)

    return redirect('/viewproject/' + project_name)


@app.route('/removefile/<filename>/<projectname>')
def remove_file(filename, projectname):
    """
    Args:
        filename (string) \n
        project name (string):
    remove file from project
    """
    db.remove_file_from_project_no_slash(projectname, filename)
    return redirect('/viewproject/' + projectname)


@app.route('/scan/<proj_name>')
def scan_proj(proj_name):
    """
    Args:
        proj_name (string)
    scans all project's files named
    """
    
    basedir = db.get_project(proj_name)['basedir']
    files = db.get_project(proj_name)['files']
    scan_project(basedir, files)
    return redirect("/viewproject/" + proj_name)

@app.route('/scanfile', methods=['POST'])
def request_scan_file():
    """
    scan the file specified and redirect 
    back to viewproject
    """
    project_name = request.form.get('projectname')
    basedir = db.get_project(project_name)['basedir']
    filename = request.form.get('filename')
    scan_file(basedir + filename)
    return redirect('/viewproject/' +project_name)

if __name__ == '__main__':
    app.run()
