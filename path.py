import os
import time
from numpy import datetime_data
import pandas as pd
import random
from pandas_profiling import ProfileReport
from datetime import  datetime, timedelta
from datetime import datetime

def main():
#   Working Directory
    dir = os.path.join('C:\\','Data')

#    Making Directory Path where output should be stored i.e, C:\\ProfileReport
    path = os.path.join('C:\\','ProfileReport')

#    If Output Directory Doesn't Exist...
    if not os.path.exists(path):
       os.mkdir(path)

    print("1 Data in Hours");print("2. Data in Days")
    choice = int(input("Enter Choice From Above :- "))
    if choice == 1:
        hour = int(input("how many hours of data is needed:- "))
    elif choice == 2:
        x = int(input("how many days data is needed:- "))
    else:
        pass

    for root,dirs,files in os.walk(dir): 
        if files != []: # If directory not Empty
            for file in files:
                data = None
                if file.endswith('.csv') or file.endswith('.xlsx'):
                    if file.endswith('.csv'):
                        data = pd.read_csv(f"{root}\{file}")
                    else: 
                        data = pd.read_excel(f"{root}\{file}")   
                    file_Datetime = time.ctime( os.path.getctime(f"{root}\{file}"))

                    if choice == 1:
                        current_datetime = datetime.now()
                        past_datetime = current_datetime - pd.DateOffset(hours=hour)
                        final_filedatetime = datetime.strptime(((datetime.strptime(str(file_Datetime), '%a %b  %d %H:%M:%S %Y')).strftime('%Y-%m-%d %H:%M:%S.%f')), '%Y-%m-%d %H:%M:%S.%f')
                        if final_filedatetime<current_datetime and final_filedatetime>past_datetime:
                            try:
                                # Creating Report
                                profile = ProfileReport(data)
                                # Output File Name
                                fileName = file.split(".")[0]
                                # Checking if Output File Already exist in Output Folder
                                if os.path.exists(f'{root}\{file}'):
                                   fileName = file.split(".")[0] + str(random.randint(1,100))
                                # Saving Output File to C:\\ProfileReport
                                profile.to_file(f"{path}\{fileName}.html")
                            except:
                                pass
                            
                    
                    elif choice == 2:
                        DatetimeList = file_Datetime.split()
                        fileDate = datetime.strptime(f"{DatetimeList[0]} {DatetimeList[1]} {DatetimeList[2]} {DatetimeList[4]}", "%a %b %d %Y").strftime("%Y-%m-%d")
                        fileDate2 = str(fileDate).split("-")
                        current_datetime = str(datetime.now()).split()[0].split("-")
                        Before = str(datetime.now() - timedelta(days=x)).split()[0].split("-") 
                     
                        File_Date = datetime(int(fileDate2[0]), int(fileDate2[1]), int(fileDate2[2]))
                        current_date = datetime(int(current_datetime[0]), int(current_datetime[1]), int(current_datetime[2]))
                        past_Date = datetime(int(Before[0]), int(Before[1]), int(Before[2]))

                        if File_Date >= past_Date and File_Date <= current_date:                            
                            try:
                                # Creating Report
                                profile = ProfileReport(data)
                                # Output File Name
                                fileName = file.split(".")[0]
                                # Checking if Output File Already exist in Output Folder
                                if os.path.exists(f'{root}\{file}'):
                                   fileName = file.split(".")[0] + str(random.randint(1,100))
                                # Saving Output File to C:\\ProfileReport
                                profile.to_file(f"{path}\{fileName}.html")
                            except:
                                pass
                    
                    
if __name__== "__main__":
  main()
