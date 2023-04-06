from flask import Flask, render_template , url_for, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import requests
import json

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'hellosecretkey'

user_id = ''
    
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False,unique=True)
#     password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})
    
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Register")
    
def validate_username(self,username):
    existing_user_username = User.query.filter_by(
        username=username.data).first()
    if existing_user_username:
        raise ValidationError("That username already exists. Please choose a different one.")
    
class LoginForm(FlaskForm):
    
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Email"})
    
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")


class QueryForm(FlaskForm):
    
    title = StringField(validators=[ Length(min=4, max=20)], render_kw={"placeholder": "Title"})
    
    year = StringField(validators=[ Length(min=4, max=20)], render_kw={"placeholder": "Year"})
    
    artist = PasswordField(validators=[ Length(min=4, max=20)], render_kw={"placeholder": "Artist"})
    
    query = SubmitField("Search")
    
    
@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    try:
        response = requests.get('https://bey5u9j96k.execute-api.us-east-1.amazonaws.com/items/'+email)
        jsonResponse = response.json()  
        
        if jsonResponse['password']==password:
            print('here1')
            return redirect(url_for('dashboard'))
        else:
            print('here2')
            return render_template('login.html', msg='Invalid password', form=form)
    except:
        print('here3')
        return render_template('login.html', msg='Invalid email', form=form)
   
    

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    form = QueryForm()
    # print(user_id)
    
    # if user_id !='':
    #     print(user_id)
    #     subscription_list = requests.get(f"https://bey5u9j96k.execute-api.us-east-1.amazonaws.com/items/{user_id}")
    
    #     print(subscription_list.json())
    

    return (render_template('dashboard.html', form=form))

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return(render_template('login.html'))

@app.errorhandler(404)
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    # confirm = requests.get(f"https://bey5u9j96k.execute-api.us-east-1.amazonaws.com/items/{form.email.data}")
    # print(confirm.json())
    # if(form.email.data and form.username.data and form.password.data):
    #     new1 = {
    #         'email': form.email.data,
    #         'password': form.password.data,
    #         'username': form.username.data
    #     }
        
    #     response = requests.put("https://bey5u9j96k.execute-api.us-east-1.amazonaws.com/items", json =new1)
        
    # print(response.json())
    # # if (confirm.json() == 'true'):
    # #     return(render_template('dashboard.html',form=form))
    # # else:
    # return(render_template('register.html',form=form))
    msg = ''
    username= form.username.data
    password = form.password.data
    email = form.email.data
    try:
        x = requests.get('https://bey5u9j96k.execute-api.us-east-1.amazonaws.com/items/'+email)
        jsonResponse = x.json()
        print(jsonResponse+'---')
        if jsonResponse['email']==email or jsonResponse['user_name']==username:
            return render_template('register.html',msg="Email exists")
    except:
        url="https://bey5u9j96k.execute-api.us-east-1.amazonaws.com/items/"
       
        myobj = {'email': email,
         'user_name': username,
         'password': password
         }
        responce= requests.put(url, json = myobj)
        print(responce.json())
        return render_template('register.html',msg="Registration is successful",form=form)
        
        

if __name__ == '__main__':
    app.run(debug=True,port=5001)