from flask import Flask, render_template, request, redirect, jsonify
import db
import os
from LLM.chat import scan_project, request_file_fix, scan_file, delete_scans
from LLM.chat import scan_summaries_dir, chat_fix_dir, OUT_Paths
from LLM.chat import get_normalized_path, read_all_db_json, read_all_db

app = Flask(__name__)


@app.route('/')
def index():
    """
    Returns:
        html: the apps main page, with all projects loaded in.
    """
    return render_template('index.html', projects=db.read_all_projects())

########## PROJECTs HANDELING ##########

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
    ignores = request.form.get('project_ignore')    
    result = db.create_new_proj(
        proj_name=project_name,
        desc=project_desc,
        lang=project_lang,
        basedir=project_dir,
        ignores=ignores.split(', ')
        )
    if not result:
        return render_template(
            'index.html',
            projects = db.read_all_projects(),
            alerts=['Something went wrong... Check if you have a project with that name or a bad folder-path']
        )
    return redirect('/')

@app.route('/edit_project', methods=['POST'])
def edit_project():
    """_summary_
    Receives via form all new project properties
    and option to keep or remove current files
    
    """
    ## GET PROPERTIES FROM FORM
    project_name = request.form.get('project_name')
    project_lang = request.form.get('project_lang')
    project_desc = request.form.get('project_desc')
    project_dir = request.form.get('project_dir')
    ignores = request.form.get('project_ignore')   
    current_project = db.get_project(request.form.get('current_name'))
    
    ### POSSIBLE ERRORS: CHANGE NAME TO EXISTING NAME / SET NEW BASE DIRECTORY AS EMPTY
    if (db.get_project(project_name) and project_name != current_project['name']) or project_dir == "" or not os.path.isdir(project_dir):
        return render_template(
        'project.html',
        project=current_project,
        files=current_project['files'],
        alerts=['Something went wrong... Check if you have a project with that name or a bad folder-path']
        )
    ### Remove current project and re-create it with new properties
    db.remove_project(current_project['name'])
    result = db.create_new_proj(
        proj_name=project_name,
        desc=project_desc,
        lang=project_lang,
        basedir=project_dir,
        ignores=ignores.split(', ')
        )
    if not result:
        return render_template(
        'project.html',
        project=current_project,
        files=current_project['files'],
        alerts=['Something went wrong... Check if you have a project with that name or a bad folder-path']
        )
    return redirect('/')

@app.route('/deleteproject/<project>/<deletescans>')
def delete_project(project, deletescans):
    if deletescans == '1':
        delete_project_scans(project)   
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

@app.route('/removefile', methods=['POST'])
def remove_file():
    """
    remove file from project.
    Choose if to remove scans or not.
    """
    filename = request.form.get('filename')
    projectname = request.form.get('projectname')
    project_dir = db.get_project(projectname)['basedir']
    del_scans = request.form.get('rmscans')
    if del_scans == '1':
        delete_scans(project_dir, filename)    
    db.remove_file_from_project(projectname, filename)
    return redirect('/viewproject/' + projectname)

########## SCANs HANDELING ##########
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
def get_fixes_for_file(project_name, file):
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

@app.route('/deletescans/<projectname>')
def delete_project_scans(projectname):
    project = db.get_project(projectname)
    files =  project['files']
    dir = project['basedir']
    for file in files:
        delete_scans(dir, file)
    return redirect('/viewproject/' + projectname)

@app.route('/deleteallscans')
def delete_all_scans():
    """_summary_
    Go over all scan and fixes folders, and remove everything.
    """
    for path in OUT_Paths:
        files = os.listdir(path)
        for file in files:
            os.remove(path + '/' + file)
    scans = os.listdir(scan_summaries_dir)
    fixes = os.listdir(chat_fix_dir)
    for scan in scans:
        os.remove(scan_summaries_dir + '/' + scan)
    for fix in fixes:
        os.remove(chat_fix_dir + '/' + fix)
    
    return redirect('/')
   
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

########## ERROR HANDLERS ##########
@app.errorhandler(404)
def page_not_found(e):
    return render_template('ErrorPage.html', error_title="Page not found 404")

@app.errorhandler(Exception)
def generic_error_handler(error):
    return render_template('ErrorPage.html', error_title="Something Went wrong... Please try again.")

if __name__ == '__main__':
        app.run()
