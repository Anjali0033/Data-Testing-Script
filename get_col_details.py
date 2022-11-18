import pandas as pd
df= pd.read_csv(r'C:\Users\Anjali_SEQ\Downloads\2022.09.27 06.49.21Z_SearCitadel.csv')

Total_count_of_0_col = df[df.columns[0]].count()
value = []
list_string = ""
column_names = df.columns
for i in column_names:
    percent = ((df[i].count())/Total_count_of_0_col) * 100
    value.append(float("%.2f"% percent)-5)
    list_string += i + ","

col_name = list_string[:-1]
colwise = dict(zip(column_names, value))

print("column_names : ",col_name,"\n\n","Column wise Percentage : ",colwise,"\n\n","Number of column : ",len(df.axes[1]))
