from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class JobForm(FlaskForm):
    job_id = StringField('Job ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    category = StringField('Category', validators=[Optional()])
    skills_requested = StringField('Skills Requested', validators=[Optional()])
    deadline = DateField('Deadline', validators=[Optional()])
    expected_cost = FloatField('Expected Cost', validators=[Optional()])
    expected_earning = FloatField('Expected Earning', validators=[Optional()])
    client_rating = FloatField('Client Rating', validators=[Optional()])
    feasibility_score = FloatField('Feasibility Score', validators=[Optional()])
    link = StringField('Job Link', validators=[Optional()])
    stage = StringField('Stage', default='Open', validators=[Optional()])
    submit = SubmitField('Submit')