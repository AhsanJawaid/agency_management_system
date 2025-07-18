from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Email, Optional

class FreelancerForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact = StringField('Contact')
    title = StringField('Title', validators=[Optional()])
    hourly_rate = DecimalField('Hourly Rate', validators=[Optional()])
    milestone_rate = StringField('Milestone Rates', validators=[Optional()])
    connects_balance = DecimalField('Connects Balance', validators=[Optional()])
    upwork_profile = StringField('Upwork Profile', validators=[Optional()])
    is_active = BooleanField('Active')
    manager_email = StringField('Manager Email', validators=[Optional(), Email()])
    submit = SubmitField('Save')