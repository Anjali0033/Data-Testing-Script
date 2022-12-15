import pandas as pd
import snowflake.connector
import csv

dataframe = []
Export_path = r'C:\Users\Anjali_SEQ\Desktop'

def next():

  return 0

def for_date(date):
  query="Select * from CITADEL_GLOBAL_EQUITIES.PUBLIC.MILLED WHERE LOADDATE like '2022-11-27%'"
  return query

def connect_to_snowflake(starting_Date,ending_Date):
  df = pd.DataFrame
  username = ''
  password = ''
  account = ''
  warehouse = ''
  database = ''
  stage_table = ''

  
  ctx = snowflake.connector.connect(user=username, password=password, account=account)
  
  def execute_query(ctx, query):
      cs = ctx.cursor()
      cs.execute(query)
      cs.close()
  sql = 'use {}'.format(database)
  execute_query(ctx, sql)
  sql = 'use warehouse {}'.format(warehouse)
  execute_query(ctx, sql)
  cs = ctx.cursor()
  for date in range(int(starting_Date.split("-")[-1]),int(ending_Date.split("-")[-1])+1):
    query = for_date(date)

    cs.execute(query)
    data = cs.fetch_pandas_all()
    # print(data)
    dataframe.append(data)

  milled = pd.concat(dataframe, axis = 0, ignore_index = True)
  file_startWith = "_"+starting_Date.split("-")[-1]+ "_" +starting_Date.split("-")[-2]+ "_" +starting_Date.split("-")[-3]
  file_endWith = ending_Date.split("-")[-1]+ "_" +starting_Date.split("-")[-2]+ "_" +starting_Date.split("-")[-3]+"_"
  milled.to_csv(f"{Export_path}/milled{file_startWith}to{file_endWith}.csv",index=False)




def start():
  starting_Date = "2022-11-28"
  ending_Date = "2022-11-31"
  connect_to_snowflake(starting_Date,ending_Date)
  
start()
# next()