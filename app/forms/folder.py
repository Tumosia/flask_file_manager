from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class FolderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Submit')
