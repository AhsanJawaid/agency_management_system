from flask_wtf import FlaskForm
from wtforms import TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProposalForm(FlaskForm):
    bid_amount   = FloatField(
                      'Your Bid Amount (USD)', 
                      validators=[DataRequired(), NumberRange(min=0)]
                   )
    cover_letter = TextAreaField('Cover Letter', validators=[DataRequired()])
    submit       = SubmitField('Submit Proposal')