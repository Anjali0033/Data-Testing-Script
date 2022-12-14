import os
import pandas as pd

SRC = r'C:\Users\Anjali_SEQ\Desktop\sally' #path of folder contain CSV


def merge_csv():

    data = pd.DataFrame()
    # append all files together
    for file in os.listdir(SRC):
        temp = pd.read_csv(f"{SRC}/{file}")
        data = pd.concat([data, temp])

    data.to_csv(f"{SRC}/sallybeauty_20221213_044124.csv",index=False) #result file name - "Indeed.csv"


merge_csv()
