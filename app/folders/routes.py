from app.folders import bp
from flask import render_template
from app.extensions import db
from app.forms.folder import FolderForm
from flask import flash, redirect, url_for, render_template, request
import datetime
import bson
import os

instance_path = os.getcwd() + "/app/data/"
folders = db['folders']

@bp.route('/')
def index():
    return render_template('folders/folder.html', folders=folders.find())

@bp.route('/new/', methods=['GET', 'POST'])
def add():
    try:
        form = FolderForm()
        if form.validate_on_submit():
            os.system("mkdir -p " + instance_path + form.name.data)
            folder = {
                "name": form.name.data,
                "created": datetime.datetime.utcnow()
            }
            folders.insert_one(folder)
            flash('Folder created successfully', 'success')
            return redirect(url_for('folders.index'))
        return render_template('folders/new_folder.html', form=form)
    except:
        flash('Error saving data', 'danger')
        return redirect(url_for('folders.index'))
    
@bp.route('/edit/<folder_id>', methods=['GET', 'POST'])
def edit(folder_id):
    try:
        form = FolderForm()
        folder = folders.find_one({"_id": bson.ObjectId(folder_id)})
        if form.validate_on_submit():
            os.system("mv " + instance_path + folder['name'] + " " + instance_path + form.name.data)
            folders.update_one({"_id": bson.ObjectId(folder_id)}, {"$set": {"name": form.name.data}})
            flash('Folder updated successfully', 'success')
            return redirect(url_for('folders.index'))
        elif request.method == 'GET':
            form.name.data = folder['name']
        return render_template('folders/edit_folder.html', form=form, folder=folder)

    except: 
        flash('Error updating data', 'danger')
        return redirect(url_for('folders.index'))

@bp.route('/delete/<folder_id>', methods=['GET', 'POST'])
def delete(folder_id):
    try:
        folder = folders.find_one({"_id": bson.ObjectId(folder_id)})
        os.system("rm -rf " + instance_path + folder['name'])
        folders.delete_one({"_id": bson.ObjectId(folder_id)})
        return redirect(url_for('folders.index'))
    except:
        flash('Error deleting data', 'danger')
        return redirect(url_for('folders.index'))