from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired

class FileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    file = FileField('File', validators=[FileRequired()])
    folder = SelectField('Folder', coerce=str)
    submit = SubmitField('Submit')
