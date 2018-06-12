from flask_wtf import FlaskForm  # importing the Forms module from Flask
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FloatField, HiddenField  # import fields to generate the form
from wtforms.validators import DataRequired  # the validator that will make sure that data is entered in the form field
from wtforms.fields.html5 import DateField  # DateField for will allow dates to be entered already formatted
from wtforms.ext.sqlalchemy.fields import QuerySelectField  # This field will query the database
from budget.models import db_query  # import the function from the database models


class PostForm(FlaskForm):
    """This class generates the form for Planned amounts"""
    title = HiddenField('Please enter the monthly Planned Amount details below:', default='Planned')
    category = SelectField('Category', choices=[('Savings', 'Savings'), ('Income', 'Income'), ('Expenses', 'Expense')], validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    planned_amount_month = FloatField('Planned Amount', validators=[DataRequired()])
    date_period = DateField('Planned Month', format='%Y-%m-%d')
    comments = TextAreaField('Comments (optional)')
    submit = SubmitField('Post')


class PostActualForm(FlaskForm):
    """This class generates the form for Actual amounts"""
    title_actual = HiddenField('Please enter the Actual Amount details below:', default='Actual')
    category_actual = SelectField('Category', choices=[('Savings', 'Savings'), ('Income', 'Income'), ('Expenses', 'Expense')], validators=[DataRequired()])
    actual_amount_name = QuerySelectField('Name', query_factory=db_query, allow_blank=False, get_label='name')
    actual_amount = FloatField('Actual Amount', validators=[DataRequired()])
    date_posted = DateField('Date of actual', format='%Y-%m-%d')
    comments = TextAreaField('Comments (optional)')
    submit = SubmitField('Post')
