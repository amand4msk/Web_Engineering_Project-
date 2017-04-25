from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])
    author = StringField('author')
    number = IntegerField('number')
    time = SelectField('time', choices=[(1,'days'),(2,'weeks'),(3,'months'),(4,'years')])
    stemmed  = BooleanField('Active')
    syn  = BooleanField('Active')
    title = BooleanField('Active')