from time import time
from datetime import datetime,time
from dateutil.parser import parse
import pandas as pd
import json


# Data testing for flightclub_newRelease_neustreet

agent_name_input = "careers_aldi"
data_testing_file = pd.read_csv(r"C:\Users\Anjali_SEQ\Downloads\careers_aldi_20220920_084020.csv",encoding='utf-8-sig') #read input file
input_table_details = pd.read_csv(r"C:\Users\Anjali_SEQ\Downloads\Details_for_Automation - Citadel Survey Capital.csv", encoding= 'unicode_escape') #read input file
column_name = ["RunDate","RUNDATE","RUN_DATE","LoadDate","LOADDATE","SCRAPE_DATE","Run Date","Rundate","run_date","Date","scrape_date"]


def parsetolist(head):
    return head.split(',')

class DataTesting:

    def __init__(self,file):
        self.file = file
        self.csv = input_table_details[input_table_details.Agent_name == agent_name_input].iloc[0]
        self.agentOrganisation = self.csv['Agent_organisation']
        self.agentName = self.csv['Agent_name']
        self.ColumnsNames = self.csv['column_names(in correct sequence)']
        self.colCount = self.csv['column_count']
    ##    self.Rundate_format = self.csv['Rundate_format']
        self.nonNull = self.csv['Not_Null_columns']
        self.UniqueCol = self.csv['Unique_columns(if any)']
        self.colWiseCount = self.csv['column_wise_percentage']
        
        self.colNames = list(data_testing_file.head())


    def validateColumns(self):

        ColumnsNames = parsetolist(self.ColumnsNames)
        errors = []

        if len(self.file.columns) != int(self.colCount):
            errors.append("Column Count Is Incorrect")

        if list(self.file.columns) != ColumnsNames:
            errors.append("Sequence Is Incorrect")

        if len(errors):
            return errors

        return "Column Count And Sequence is Correct" 


    def validateDataTime(self):
    ##  # Validate RunDate Column
        try:
            Rundate = ''
            for file_col in self.file.columns.tolist():
                for list_col in column_name:
                    # print(file_col,list_col)
                    if file_col == list_col:
                        Rundate = file_col
                        break
            if Rundate is not None:
                runDateResult = ""

                for rundate in self.file[Rundate].unique():
                    if type(rundate) != str:
                        continue
                    
                    if datetime.strftime(parse(rundate).date(),"%Y-%m-%d") and time.strftime(parse(rundate).time(),'%H:%M:%S') and parse(rundate).tzinfo != None:    
                        runDateResult = f"Rundate Format is correct"
                    else:
                        runDateResult = f"{Rundate} Incorrect Rundate - {rundate}"
                        break
                    

                ## Validate RunTime Column
                runTimeResult = ""
                for DataFile in range(len(self.file)):
                   runtime = self.file[Rundate].iloc[DataFile]

                   if type(runtime) != str:
                       continue
                   
                   if datetime.strftime(parse(runtime).date(),"%d-%m-%Y") and time.strftime(parse(runtime).time(),'%H:%M:%S'):    
                        runTimeResult = "Runtime Format is correct"
                   else:
                        runTimeResult = "{} Incorrect Runtime - {}".format(Rundate,rundate)
                        break
        #       
                return runDateResult,runTimeResult + f" For : {Rundate}(column name)"

            else : 
                return f"Please update column_name of rundate for {agent_name_input} Agent.(To update this , You will find column_name list variable With in script.)"
        except:

            return "Some Unexpected Error in validateDataTime Function."


    def validateUniqueCol(self):
        try:
            notunique = []
            for col in parsetolist(self.UniqueCol):
                if self.file[col].is_unique:
                    pass
                else:
                    notunique.append(col)


                if len(notunique):
                    return f"These Fields Are Set To Be Unique, Still Containing dublicate Values : {notunique} ."
            
                return f"No Fields Are dublicate Which Are Set to be unique : {parsetolist(self.UniqueCol)}"  

        except:
            if type(self.nonNull) == float:
                return "{} Agent have no Unique fields .".format(agent_name_input)
            else:
                return "Some Unexpected error in validateUniqueCol function."


    def validateNonNullColumns(self):

        try:
            columnPerc = dict(self.file[self.file.columns[self.file.notnull().any()]].notnull().sum() * 100 / self.file.shape[0])
            
            # print(columnPerc.keys())
            null = []
            for col in parsetolist(self.nonNull):
                if columnPerc[col] != 100.0:
                    null.append(col)

            if len(null):
                return f"These Fields Are Set To Be Not Null, Still Containing Null Values : {null} ."
        
            return "No Fields Are Blank Which Are Set To Be Not Null "

        except:
            if type(self.nonNull) == float:
                return "{} Agent have no NotNull fields are available.".format(agent_name_input)
            else:
                return "Some unexpected error facing in validateNonNullColumns function."



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
                
            return "Category Wise Count is Correct "

        except:
            return "Some Unexpected Error in validateCategoryWiseCount function."


    def validateCompleteBlankCol(self):
        try:
            errors = []
            for col in self.colNames:
                result = False
                for row in data_testing_file[col]:
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

            return "No Completely Blank Columns Are Available ."

        except:
            return "Some unexceptected error in validateCompleteBlankCol Function."
        


datafile = DataTesting(data_testing_file)

Report = 70*'-' + f"\nData Testing report for {agent_name_input} agent\n"

# print(datafile.validateColumns())
# print(datafile.validateDataTime())
# print(datafile.validateUniqueCol()) 
# print(datafile.validateNonNullColumns())
# print(datafile.validateCategoryWiseCount())
# print(datafile.validateCompleteBlankCol())
#

Report = Report + f"1.{datafile.validateColumns()}\n2.{datafile.validateDataTime()}\n3.{datafile.validateNonNullColumns()}\n4.{datafile.validateCategoryWiseCount()}\n5.{datafile.validateCompleteBlankCol()}"
print(Report)