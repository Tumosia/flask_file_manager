from app.main import bp
from app.extensions import db
from flask import render_template

files=db['files']

@bp.route('/')
def index():
    return render_template('files/file.html', files=files.find())

