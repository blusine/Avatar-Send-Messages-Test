def read_data():
  import pandas as pd
  df = pd.read_csv('/data/ALC_Class_Report_Test.csv')
  return df

def clean_phone(phone):
  return list(map(lambda x: fix_a_num(x), phone))
      
def fix_a_num(anum):
  import re
  anum = ''.join(re.findall('\d', repr(str(anum))))
  if len(anum) > 10:
    anum = anum[len(anum) - 10:]
  return '+1' + anum