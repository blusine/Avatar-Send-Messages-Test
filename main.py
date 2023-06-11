from flask import Flask, render_template, redirect, url_for, request, json
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, DateField, FieldList, FormField, BooleanField
#from wtforms import RadioField, TextAreaField, SelectField

from wtforms.validators import InputRequired, Email
from datetime import date as dt

from utils import read_data, fix_a_num, send_sms
import os

app = Flask('__name__')
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'Mysecret!'
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

filename = os.getcwd() + "/data/twilio_keys.json"
with open(filename) as test_file:
    twilio_keys = json.load(test_file)
print("twilio_keys, ", twilio_keys)
app.config['account_sid'] = twilio_keys["account_sid"]
app.config['TWILIO_AUTH_TOKEN'] = twilio_keys["TWILIO_AUTH_TOKEN"]

class LoginForm(FlaskForm):
  username = StringField('Zoom Email:', validators=[InputRequired("Input Required!"),  Email()] )
  password = PasswordField('Zoom Password:', validators=[InputRequired(),] )
  classroom = StringField('Class Code:', validators=[InputRequired(),] )

class RowForm(FlaskForm):
  student = StringField('Student')
  #attendance = BooleanField('Attendance')
  #homework = BooleanField('Homework')
  #performance = SelectField('Performance')
  sms = BooleanField('sms')
  #comments = StringField('Comments')
  phone = StringField('Phone')
  #Attendance	Homework	Academic Performance	Comments	Tardy - Send SMS


#class TableForm(FlaskForm):
#    rows = FieldList(FormField(RowForm))
  
class ReportForm(FlaskForm):
  date = DateField(description="Class Date")
  classroom = StringField('Class Code:', validators=[InputRequired(),] )
  teachername = StringField("Teacher's Name", validators=[InputRequired(),] )
  #difficultylevel = RadioField()
  rows = FieldList(FormField(RowForm))
  #general_comments = TextAreaField()
  #students = TableForm()
  #Student = namedtuple('Student', ['name', 'attenance', 'homework', 'performance', 'comments', 'sms'])
  

@app.route('/', methods = ["POST", "GET"])
def login():
  #form = LoginForm(username = "avatarmath.space.9@gmail.com", classroom = "v6sl7dl")
  form = LoginForm(username = "avatarmath.space.6@gmail.com", classroom = "pzlal6y")
  
  if form.validate_on_submit():
    df = read_data(form.username.data, form.password.data, form.classroom.data)
    if (df is not None) & (not df.empty):
      teachername = df["Teacher"].iloc[0]
      form2 = ReportForm(teachername = teachername, date = dt.today())
      df["Parent phone"] = df["Parent phone"].apply(lambda x: fix_a_num(x))
      df2 = df[["Student Name", "Parent phone"]]
      
      headings = ['Attendance', 'Homework', 'Academic Performance',
                  'Comments', 'Tardy - Send SMS']
      headings = ['Tardy - Send SMS']
      #return render_template('classreport.html', form = form2, headings = headings, data = df2)
      return render_template('smsreport.html', form = form2, headings = headings, data = df2)
    else:
      header_message = "Wrong Input"
      body_message = "Incorrect Email, Password or Class Code"
      return redirect(url_for('error_message', header_message=header_message , body_message=body_message))
  return render_template('login.html', form = form)

@app.route('/classreport', methods = ["GET", "POST"])
def classreport():
  form = ReportForm()
  if form.validate_on_submit():
    result = request.form.data
    print("sms2: ", result)
    #r2 = save_data(result)
    #header_message = "Thank you!"
    #body_message = "Avatar Learning Center Classroom Report Form has been submitted."
    redirect(url_for('submitted'))
    
  return render_template('classreport.html', form = form)

@app.route('/smsreport', methods = ["GET", "POST"])
def smsreport():
  form = request.form
  return render_template('smsreport.html', form = form)

@app.route('/submitted', methods = ["GET", "POST"])
def submitted():
  form = request.form
  to_sms = form.getlist("sms")
  phone_numbers = form.getlist("phone")
  student_names = form.getlist("student")
  for sms in to_sms:
    sms_int = int(sms)
    send_sms(student_names[sms_int], phone_numbers[sms_int], app.config['account_sid'], app.config['TWILIO_AUTH_TOKEN'])
  
  header_message="Thank you!"
  body_message="Avatar Learning Center Classroom Report Form has been submitted."
  return render_template("error.html", header_message=header_message, body_message=body_message)
  
@app.route('/error/<header_message>/<body_message>' , methods = ["GET", "POST"])
def error_message(header_message, body_message):
    return render_template("error.html", header_message=header_message, body_message=body_message)
  
if (__name__) == "__main__":
  csrf = CSRFProtect(app)
  app.run(host='0.0.0.0', port=8080, debug = True)