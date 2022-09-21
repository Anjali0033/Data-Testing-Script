import pandas as pd
df= pd.read_csv(r'C:\Users\Anjali_SEQ\Desktop\milled_Test_20220920_003504.csv')



value = []
list_string = ""
column_names = df.columns
for i in column_names:
    percent = ((df[i].count())/5744) * 100
    value.append("%.2f"% percent)
    list_string += i + ","

col_name = list_string[:-1]
colwise = dict(zip(column_names, value))

print("column_names : ",col_name,"\n","Column wise Percentage : ",colwise)
