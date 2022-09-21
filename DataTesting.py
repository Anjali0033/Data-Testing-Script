from time import time
from datetime import datetime,time
from dateutil.parser import parse
import pandas as pd
import json




agent_name_input = "pcpartpicker"
data_file = pd.read_csv(r"C:\Users\Anjali_SEQ\Downloads\2022-09-19T22.45.35Z_pcpartpicker.csv",encoding='utf-8-sig') #read input file
table_details = pd.read_csv(r"C:\Users\Anjali_SEQ\Downloads\Details_for_Automation - Citadel Survey Capital.csv", encoding= 'unicode_escape') #read input file


def parsetolist(head):
    if "," in head:
        return head.split(',')
    else:
        list = [head]
        return list

def  correct_rundateCol():
    column_name = ["RunDate","RUNDATE","RUN_DATE","LoadDate","LOADDATE","SCRAPE_DATE","Run Date"]
    rundateCol = ""
    for File in range(len(data_file)):
        for column in column_name:
            try :
                data_file[column].iloc[File]            
                rundateCol = column
                break
            except:
                pass
    return rundateCol

class DataTesting:

    def __init__(self,file):
        self.file = file
        self.csv = table_details[table_details.Agent_name == agent_name_input].iloc[0]
        self.agentOrganisation = self.csv['Agent_organisation']
        self.agentName = self.csv['Agent_name']
        self.ColumnsNames = self.csv['column_names(in correct sequence)']
        self.colCount = self.csv['column_count']
    ##    self.Rundate_format = self.csv['Rundate_format']
        self.nonNull = self.csv['Not_Null_columns']
        self.UniqueCol = self.csv['Unique_columns(if any)']
        self.colWiseCount = self.csv['column_wise_percentage']
        
        self.colNames = list(data_file.head())

# ------------------------------------------------------------------------------
    def print_(self):
        print((type()))
        print(self.colWiseCount)
        print(type(json.loads(self.colWiseCount)))

# ------------------------------------------------------------------------------

    def validateColumns(self):
        #Providing column names of data file.
        try : 
            ColumnsNames = parsetolist(self.ColumnsNames)

            errors = []

            if len(self.file.columns) != int(self.colCount):
                errors.append("Column Count Is Incorrect")

            if list(self.file.columns) != ColumnsNames:
                errors.append("Sequence Is Incorrect")

            if len(errors):
                return errors

            return "Column Count And Sequence is Correct"

        except:

            return "ColumnsNames is not available in agent file"


    def validateDataTime(self):
    ##     # Validate RunDate Column
        Rundate = ""
        for file_col in ((self.file).columns).tolist():
            for list_col in column_name:
                if file_col == list_col:
                    Rundate = file_col
                    break
        print(Rundate)

        # runDateResult = ""
        # for rundate in self.file[Rundate].unique():
            # if type(rundate) != str:
                # continue
            # 
            # if datetime.strftime(parse(rundate).date(),"%Y-%m-%d") and time.strftime(parse(rundate).time(),'%H:%M:%S') and parse(rundate).tzinfo != None:    
                # runDateResult = "{} Format is correct",format(Rundate)
            # else:
                # runDateResult = "{} Incorrect - {}".format(Rundate,rundate)
                # break
# 
            # return(runDateResult)

        ## Validate RunTime Column
        #runTimeResult = ""
        #for DataFile in range(len(self.file)):
        #    runtime = self.file['rundate_time'].iloc[DataFile]
#
        #    if type(runtime) != str:
        #        continue
        #    
        #    if datetime.strftime(parse(runtime).date(),"%d-%m-%Y") and time.strftime(parse(runtime).time(),'%H:%M:%S'):    
        #        runTimeResult = "RunTime Format is correct"
        #    else:
        #        runTimeResult = "RunTime Incorrect"
        #        break
#
        #return [runDateResult,runTimeResult]

    def validateUniqueCol(self):
        try:
            null = []

            for col in parsetolist(self.UniqueCol):
                if self.file[self.UniqueCol].is_unique:
                    null.append(col)

            if len(null):
                return f"No Fields Are dublicate Which Are Set To Be Unique : {parsetolist(self.UniqueCol)}"
            return f"These Fields Are Set To Be Unique, but Still Containing dublicate Values : {null} ."

        except:

            return "Unique columns are not available in agent file"



    def validateNonNullColumns(self):
    
        try:
            columnPerc = dict(self.file[self.file.columns[self.file.notnull().any()]].notnull().sum() * 100 / self.file.shape[0])
            
            # print(columnPerc.keys())
            # print(parsetolist(self.nonNull))
            null = []
            for col in parsetolist(self.nonNull):
                if columnPerc[col] != 100.0:
                    null.append(col)
    # 
            if len(null):
                return f"These Fields Are Set To Be Not Null, Still Containing Null Values : {null} ."

            return "No Fields Are Blank Which Are Set To Be Not Null"
        
        except:
            
            return "Not Null columns are not available in agent file"


    def validateCategoryWiseCount(self):
        try:
            columnPerc = dict(self.file[self.file.columns[self.file.notnull().any()]].notnull().sum() * 100 / self.file.shape[0])
            colWiseCount = self.colWiseCount
            less = []
            for perc in colWiseCount:
                try:
                    if columnPerc[perc] < colWiseCount[perc]:
                        less.append(perc)
                except:
                    pass

            if len(less):
                return f"Category Wise Count Is Not Correct : {less} ."
                
            return "Category Wise Count is Correct"
        
        except:
            return "Category wise column is Not available"


    def validateCompleteBlankCol(self):
        try:
                
            errors = []
            for col in self.colNames:
                result = False
                for row in data_file[col]:
                    if type(row) != float:
                        result = True
                        break
                    else:
                        try:
                            if int(row):
                                result = True
                                break
                        except:
                            pass
                
                if not result:
                    errors.append(col)

            if len(errors):
                return f"These Are Completely Blank Columns : {errors}"

            return "No Completely Blank Columns Are Available in result file."
        
        except:

            return "complete blank column is Not available in agent"


datafile = DataTesting(data_file)

print(datafile.validateColumns())
# print(datafile.validateDataTime())
print(datafile.validateUniqueCol()) 
print(datafile.validateNonNullColumns())
print(datafile.validateCategoryWiseCount())
print(datafile.validateCompleteBlankCol())

# Report = f"1.{datafile.validateColumns()}\n\n3.{datafile.validateNonNullColumns()}\n4.{datafile.validateCategoryWiseCount()}\n5.{datafile.validateCompleteBlankCol()}"
# print(Report)
# 