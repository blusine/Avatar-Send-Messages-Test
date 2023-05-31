from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

#import sys
#sys.path.insert(0, os.getcwd()+"/Static")    
#import utils.py
#from utils.py import read_data

app = Flask('__name__')
app.config['SECRET_KEY'] = 'Mysecret!'
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

class LoginForm(FlaskForm):
  username = StringField('username', validators=[InputRequired(),] )
  password = PasswordField('password', validators=[InputRequired(),] )
  classroom = StringField('classroom', validators=[InputRequired(),] )

@app.route('/', methods = ["GET", "POST"])
def login():
  form = LoginForm()
  #df = pd.DataFrame(utils.read_data())
  #print(df)
  
  if form.validate_on_submit():
    return f'<h1> Username: {form.username.data} Password: {form.password.data} Classroom: {form.classroom.data} </h1>'
    #return f'<h1> data </h1> <br><br> <h2> {df} </h2'
  
  return render_template('login.html', form = form)
  #else:
    #<a href="{{ url_for('page_not_found') }}">Go to home</a>

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
  
if (__name__) == "__main__":
  #import pandas as pd
  app.run(host='0.0.0.0', port=8080, debug = True)
