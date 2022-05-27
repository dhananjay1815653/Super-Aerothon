from flask import Flask, send_file,render_template , request, redirect, url_for, flash ,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY']='3994554a25feb26b70c86faa'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///datastore.db'

db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
FRONTL=["HTML","XML","REACTJS"]
BACKL=["JAVA","PYTHON","NODEJS","KOTLIN"]


class Users(db.Model):
           id = db.Column(db.Integer(),primary_key=True)
           public_id = db.Column(db.Integer())
           username = db.Column(db.String(length=50),nullable=False,unique=True)
           password_hash = db.Column(db.String(length=50),nullable=False)

           @property
           def password(self):
                return self.password

           @password.setter
           def password(self, plain_text_password):
                self.password_hash= bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

           def verify_password(self,password):
               return bcrypt.check_password_hash(self.password_hash,password)

from forms import RegisterForm,SelectForm,LoginForm

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token= request.cookies.get('token')
        if not token :
            return redirect(url_for('index'))
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms='HS256')
            current_user = Users.query.filter_by(username=data['username']).first()
        except:
            return redirect(url_for('index'))

        return f(current_user ,*args ,**kwargs)
    return decorator



@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=['GET',"POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user.verify_password(form.password.data):
            token =  jwt.encode({'username':request.form.get("username"),'exp':datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('token', token,httponly=True)
            return resp
        if not user.verify_password(form.password.data):
            flash(f'Incorrect Password')
    if form.errors !={} :
        for err_msg in form.errors.values():
            flash(f' Error :{err_msg}',category="danger")

    return render_template("login.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user=Users(username= form.username.data,password=form.password.data,public_id=str(uuid.uuid4()))
        db.session.add(create_user)
        db.session.commit()
        return redirect(url_for('index'))
    if form.errors !={} :
        for err_msg in form.errors.values():
            flash(f'An error occured while creating User:{err_msg}',category="danger")
    return render_template("register.html",form=form)


@app.route("/homepage",methods=["GET","POST"])
@token_required
def home(current_user):
    user=Users.query.filter_by(username=current_user.username).first()
    return render_template("homepage.html",user=user)

@app.route("/logout",methods=["GET"])
@token_required
def logout(current_user):
    token = ''
    resp = make_response(render_template("logout.html"))
    resp.set_cookie('token', token)
    return resp

@app.route("/get_boiler",methods=["GET","POST"])
@token_required
def get_boiler(current_user):
    eform = SelectForm()

    if eform.validate_on_submit():
        frontEnd =eform.frontEnd.data
        backEnd =eform.backEnd.data

        if frontEnd not in FRONTL:
            flash(f'Please select another language')
            return redirect(url_for('get_boiler'))
        if backEnd not in BACKL:
            flash(f'Please select another language')
            return redirect(url_for('get_boiler'))
        if (frontEnd=="HTML" and backEnd=="JAVA"):
            p="HTML-JAVA.zip"

        if (frontEnd=="HTML" and backEnd=="PYTHON"):
            p="HTML-PYTHON.zip"

        if (frontEnd=="HTML" and backEnd=="NODEJS"):
            p="HTML-NODEJS.zip"

        if (frontEnd=="XML" and backEnd=="KOTLIN"):
            p="XML-KOTLIN.zip"

        if (frontEnd=="REACTJS" and backEnd=="NODEJS"):
            p="REACTJS-NODEJS.zip"

        if (frontEnd=="XML" and backEnd=="PYTHON") or (frontEnd=="XML" and backEnd=="JAVA") or (frontEnd=="REACTJS" and backEnd=="PYTHON") or (frontEnd=="REACTJS" and backEnd=="JAVA") or (frontEnd=="XML" and backEnd=="NODEJS") or (frontEnd=="REACTJS" and backEnd=="KOTLIN") or (frontEnd=="HTML" and backEnd=="KOTLIN"):
            flash(f'Please select another combination')
            return redirect(url_for('get_boiler'))

        return send_file(p,as_attachment=True)

    if eform.errors !={} :
        for err_msg in eform.errors.values():
            flash(f'Error:{err_msg}', category="danger")



    return render_template("get_boiler.html",eform=eform,user=current_user)


@app.route("/failure",methods=["GET"])
@token_required
def failure(current_user):

    return render_template("failure.html")



if  __name__ == '__main__':
     app.run(debug=True)
