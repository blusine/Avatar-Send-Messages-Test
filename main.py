from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, DateField, RadioField
from wtforms.validators import InputRequired, Email
from datetime import date as dt
from utils import read_data

app = Flask('__name__')
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'Mysecret!'
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

class LoginForm(FlaskForm):
  username = StringField('Zoom Email:', validators=[InputRequired("Input Required!"),  Email()] )
  password = PasswordField('Zoom Password:', validators=[InputRequired(),] )
  classroom = StringField('Class Code:', validators=[InputRequired(),] )

class ReportForm(FlaskForm):
  date = DateField(description="Class Date")
  classroom = StringField('Class Code:', validators=[InputRequired(),] )
  teachername = StringField("Teacher's Name", validators=[InputRequired(),] )
  difficultylevel = RadioField()
  

@app.route('/', methods = ["POST", "GET"])
def login():
  form = LoginForm(username = "avatarmath.space.9@gmail.com", classroom = "v6sl7dl")
  if form.validate_on_submit():
    df = read_data(form.username.data, form.password.data, form.classroom.data)
    if (df is not None) & (not df.empty):
      teachername = df["Teacher"].iloc[0]
      form2 = ReportForm(teachername = teachername, date = dt.today())
      classroom = request.form.get('classroom')
      df2 = df["Student Name"]
      print("df2: ", df2)
      mycols = ['Attendance', 'Homework', 'Academic Performance', 'Comments?', 'Tardy - Send SMS']
      #df2 = df2.reindex(df2.columns.tolist() + mycols,axis=1)
      #df2 = df2.reindex(columns = [*df2.columns.tolist(), *mycols], fill_value=1)
      #df2[['Attendance', 'Homework', 'Tardy - Send SMS']] == 1

      #df2['Attendance'] = '<input type="checkbox" />'
      
      #df.insert(loc = 0,column = 'PPA',value = '<input type="checkbox" />')
      #df2['Academic Performance'] == 2
      #df2['Comments?'] == 3
      #headings = df2.columns.to_list()
      #df2 = df2.to_json(orient='records')
      #return redirect(url_for('classreport'))
      #df2 = df2.to_html(index=False)
      #print("df2: ", df2)
      return render_template('classreport.html', form = form2, data = df2)
      #return f'<h1> data </h1> <br><br> <h2> {df} </h2'
    else:
      header_message = "Wrong Input"
      body_message = "Incorrect Email, Password or Class Code"
      #return f'<h1> data </h1> <br><br> <h2> {df} </h2'
      return redirect(url_for('error_message', header_message=header_message , body_message=body_message))
  return render_template('login.html', form = form)

@app.route('/classreport', methods = ["GET", "POST"])
def classreport():
  form2 = ReportForm()
  return render_template('classreport.html', form = form2)

@app.route('/error/<header_message>/<body_message>', methods = ["GET", "POST"])
def error_message(header_message, body_message):
    return render_template("error.html", header_message=header_message, body_message=body_message)
  
if (__name__) == "__main__":
  import pandas as pd
  app.run(host='0.0.0.0', port=8080, debug = True)