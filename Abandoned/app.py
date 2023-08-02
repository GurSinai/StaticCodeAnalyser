from flask import Flask, render_template
import db
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', projects=db.read_all_projects())

if __name__ == '__main__':
    app.run(debug=True)