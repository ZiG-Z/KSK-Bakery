from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from ksk.models import BreadSnack, Pizza, User
from flask_wtf.file import FileAllowed,FileField

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Update')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f'There is no account asssociated with {email.data}.')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')

class KSKPizzaUpdateForm(FlaskForm):
    type = StringField('Type',validators=[DataRequired()])
    image_file = FileField('Upload An Image',validators=[FileAllowed(['jpg','jpeg'])])
    product_detail = TextAreaField('About Your Product',validators=[DataRequired(),Length(min=1,max=100)])
    submit = SubmitField('Update')

class KSKBreadSnackUpdateForm(KSKPizzaUpdateForm):
    pass
        