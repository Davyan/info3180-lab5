from flask.ext.wtf import Form 
from wtforms.fields import TextField,PasswordField # other fields include PasswordField 
from wtforms.validators import Required, Email


class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     # evil, don't do this
     image = TextField('Image', validators=[Required(), Email()])

class LoginForm(Form):
     username = TextField('Username', validators=[Required()])
     password= PasswordField('Password', validators=[Required()])
    
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
