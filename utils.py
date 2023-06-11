def read_data(username, password, classcode):
  import pandas as pd
  import os
  x = os.getcwd()
  if username_validator(username, password):
    df = pd.read_csv(x + '/data/ALC_Class_Report_Test.csv')
    df = df[df['Zoom'] == username]
    df = df[df['ClassCode'] == classcode]
    
    cols = [
      'Parent Name', 'Parent email', 'Student Name', 'AvatarGrade', 'Teacher',
      'Zoom', 'Password', 'Parent phone', 'ClassCode'
    ]
    
    df = df[cols]
    df[cols] = df[cols].astype(str)
  else:
    df = pd.DataFrame()
  return df

def username_validator(username, password):
  import pandas as pd
  import os
  from werkzeug.security import check_password_hash
  x = os.getcwd()
  df = pd.read_csv(x + '/data/username_validator.csv')
  cols = ['username', 'password']
  df[cols] = df[cols].astype(str)
  df = df[df['username'] == username]
  if (not df.empty):
    #if (df['password'].iloc[0] == generate_password_hash(password)):
    if check_password_hash(df['password'].iloc[0], password):
      return True
    else:
      return False
    return False

def send_sms(name, num, account_sid, auth_token):
  from twilio.rest import Client
    
  # Find your Account SID and Auth Token at twilio.com/console
  # and set the environment variables. See http://twil.io/secure
  
  client = Client(account_sid, auth_token)
  
  message = client.messages \
      .create(
           body= f'Dear {name}, this is a test SMS sent from Flask WebApp.',
           from_='+18777432015',
           to=num
       )
  
  return print("Sent: ", message, "from: ", message.sid)


def fix_a_num(anum):
  import re
  anum = ''.join(re.findall('\d', repr(str(anum))))
  if len(anum) > 10:
    anum = anum[len(anum) - 10:]
  return '+1' + anum


def classcode_validator(username, classcode):
  import pandas as pd
  import os
  x = os.getcwd()
  df = pd.read_csv(x + '/data/classcode_validator.csv')
  df = df[df['username'] == username]
  if df & (df['classcode'][0] == classcode):
    return True
  else:
    return False

def save_data():
  from flask import request
  print("Here")
  result = request.form.getlist("sms")
  #r2 = save_data(result)
  print("sms2: ", result)  
  return f'<h1> result </h1> <br><br> <h2> {result} </h2'

def clean_phone(phone):
  return list(map(lambda x: fix_a_num(x), phone))