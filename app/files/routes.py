from app.files import bp
from app.extensions import db
from app.forms.file import FileForm
from werkzeug.utils import secure_filename
from flask import flash, redirect, url_for, render_template, send_file, request
import datetime
import bson
import os

instance_path = os.getcwd() + "/app/data/"
files = db['files']
folders = db['folders']

@bp.route('/')
def index():
    return render_template('files/file.html', files=files.find())

@bp.route('/new/', methods=['GET', 'POST'])
def add():
    try:
        form = FileForm()
        form.folder.choices = [(f['name']) for f in folders.find({})]
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                instance_path,form.folder.data,filename
            ))
            file = {
                "name": form.name.data,
                "file": filename,
                "path": instance_path + form.folder.data + "/" + filename,
                "created": datetime.datetime.utcnow(),
                "folder": form.folder.data,
                "folder_id": folders.find_one({"name": form.folder.data})['_id']
            }
            files.insert_one(file)
            flash('File created successfully', 'success')
            return redirect(url_for('files.index'))
        return render_template('files/new_file.html', form=form)
    except:
        flash('Error saving data', 'danger')
        return redirect(url_for('files.index'))
    
@bp.route('/edit/<file_id>', methods=['GET', 'POST'])
def edit(file_id):
    try:
        form = FileForm()
        form.folder.choices = [(f['name']) for f in folders.find({})]
        file = files.find_one({"_id": bson.ObjectId(file_id)})
        if form.validate_on_submit():
            os.system("mv " + instance_path + file['folder'] + "/" + file['file'] + " " + instance_path + form.folder.data + "/" + file['file'])
            files.update_one({"_id": bson.ObjectId(file_id)}, {"$set": {"name": form.name.data, "folder": form.folder.data}})
            flash('File updated successfully', 'success')
            return redirect(url_for('files.index'))
        elif request.method == 'GET':
            form.name.data = file['name']
            form.folder.data = file['folder']
        return render_template('files/edit_file.html', form=form, file=file)
    except:
        flash('Error updating data', 'danger')
        return redirect(url_for('files.index'))
    
@bp.route('/delete/<file_id>', methods=['GET', 'POST'])
def delete(file_id):
    try:
        file = files.find_one({"_id": bson.ObjectId(file_id)})
        os.system("rm " + instance_path + file['folder'] + "/" + file['file'])
        files.delete_one({"_id": bson.ObjectId(file_id)})
        flash('File deleted successfully', 'success')
        return redirect(url_for('files.index'))
    except:
        flash('Error deleting data', 'danger')
        return redirect(url_for('files.index'))
    
@bp.route('/download/<file_id>', methods=['GET', 'POST'])
def download(file_id):
    try:
        file = files.find_one({"_id": bson.ObjectId(file_id)})
        flash('File downloaded successfully', 'success')
        return send_file(instance_path + file['folder'] + "/" + file['file'], as_attachment=True)
    except:
        flash('Error downloading file', 'danger')
        return redirect(url_for('files.index'))
