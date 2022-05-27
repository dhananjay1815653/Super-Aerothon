from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,DateField,SelectField
from wtforms.validators import Length,EqualTo,DataRequired,ValidationError
from app import Users

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user=Users.query.filter_by(username=username_to_check.data).first()
        if(user):
             raise ValidationError('OOPS !! Username already Exsists..Try another !')
    username = StringField(label='Username:',validators=[Length(min=5,max=25),DataRequired()])
    password = PasswordField(label='Password1:',validators=[Length(min=5,max=15),DataRequired()])
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password'),DataRequired()])
    submit=SubmitField(label='Create Account')


class SelectForm(FlaskForm):
    frontEnd = SelectField('FrontEnd',choices=[('Select','--select--'),('HTML','HTML'),('REACTJS','REACTJS'),('XML','XML')])
    backEnd = SelectField('BackEnd',choices=[('Select','--select--'),('JAVA','JAVA'),('PYTHON','PYTHON'),('NODEJS','NODEJS'),('KOTLIN','KOTLIN')])
    submit=SubmitField(label='Get BoilerPlate !')

class LoginForm(FlaskForm):
    def validate_username(self, username_to_check):
        user=Users.query.filter_by(username=username_to_check.data).first()

        if not user:
            raise ValidationError('OOPS ! User not Found!')

    username = StringField(label='Username:',validators=[Length(min=5,max=25),DataRequired()])
    password = PasswordField(label='Password:',validators=[Length(min=5,max=15),DataRequired()])
    submit=SubmitField(label='Sign In')

