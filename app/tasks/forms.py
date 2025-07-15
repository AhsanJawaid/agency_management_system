from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    job_id = SelectField('Job', coerce=str)
    project_id = SelectField('Project', coerce=int)
    assigned_to_email = SelectField('Assign To', coerce=str)
    deadline_datetime = DateField('Deadline')
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

