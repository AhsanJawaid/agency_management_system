from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    job_id = SelectField('Job', coerce=str)
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    status = StringField('Status', default='Planning')
    submit = SubmitField('Submit')
