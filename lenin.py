import pandas as pd

text = ""

with open(r'C:\Users\Anjali_SEQ\Downloads\sbd_paris_cl-2022_12_20-06_29_00.log') as f:
    lines = f.readlines()
    for i in lines:
        if " ," in i:
            text += i

print(text)

with open('my_file.csv', 'w') as out:
    out.write(text)