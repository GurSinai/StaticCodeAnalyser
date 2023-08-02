from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', projects=db.read_all_projects())


@app.route('/create_project', methods=['POST'])
def createproject():
    project_name = request.form.get('project_name')
    project_lang = request.form.get('project_lang')
    project_desc = request.form.get('project_desc')
    db.create_new_proj(proj_name=project_name, desc=project_desc, lang=project_lang)
    return redirect('/')

@app.route('/viewproject/<project>')
def view_project(project):
    return render_template('project.html', project=db.get_project(project), files=db.get_project_files(project))


if __name__ == '__main__':
    app.run(debug=True)