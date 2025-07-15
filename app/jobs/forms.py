from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired

class JobForm(FlaskForm):
    job_id = StringField('Job ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    category = StringField('Category')
    skills_requested = StringField('Skills Requested')
    deadline = DateField('Deadline')
    expected_cost = FloatField('Expected Cost')
    expected_earning = FloatField('Expected Earning')
    client_rating = FloatField('Client Rating')
    feasibility_score = FloatField('Feasibility Score')
    link = StringField('Link')
    stage = StringField('Stage', default='Open')
    submit = SubmitField('Submit')
