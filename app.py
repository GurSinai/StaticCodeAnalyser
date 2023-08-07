from flask import Flask, render_template, request, redirect, jsonify
import db, os
from LLM.chat import scan_project, scan_file, get_normalized_path, Scan_basedir, OUT_Paths
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', projects=db.read_all_projects())


@app.route('/create_project', methods=['POST'])
def createproject():
    project_name = request.form.get('project_name')
    project_lang = request.form.get('project_lang')
    project_desc = request.form.get('project_desc')
    project_dir = request.form.get('project_dir')
    db.create_new_proj(proj_name=project_name, desc=project_desc, lang=project_lang, basedir=project_dir)
    return redirect('/')

@app.route('/viewproject/<project>')
def view_project(project):
    return render_template('project.html', project=db.get_project(project), files=db.get_project_files(project))

@app.route('/getscan/<project_name>/<file>')
def getfile(project_name, file):
    project = db.get_project(project_name)
    nor = get_normalized_path(project['basedir'] + '/' + file)
    output = ""
    for path in OUT_Paths:
        with open(path + '/' + nor) as f:
            output += f.read()
    return jsonify(output)

@app.route('/addfile', methods=['POST'])
def add_file():
    file = request.form.get('path')
    project_name = request.form.get('project_name')
    project = db.get_project(project_name)
    if file != "" and file is not None and os.path.isfile(file):
        db.add_file_to_project(project_name, file)
    if file != "" and file is not None and os.path.isfile(project['basedir'] +'/'+ file):
        db.add_file_to_project(project_name, file)
    return redirect('/viewproject/' + project_name)

@app.route('/removefile/<filename>/<projectname>')
def remove_file(filename, projectname):
    db.remove_file_from_project_no_slash(projectname, filename)
    return redirect('/viewproject/' + projectname)

@app.route('/scan/<proj_name>')
def scan_proj(proj_name):
    basedir = db.get_project(proj_name)['basedir']
    scan_project(basedir)
    return redirect('/viewproject/' + proj_name)

if __name__ == '__main__':
    app.run(debug=True)

