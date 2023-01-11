import os
import pandas as pd

Datalist = []


Folder_name,Folder_path,folder_size,size_byte = [],[],[],[]

directory_list = list()
for root, dirs, files in os.walk(r'C:\Users\Anjali_SEQ\Documents\Sequentum Enterprise\Agents\test'): #Directory input path
    for name in dirs:
        directory_list.append(os.path.join(root, name))

for folder in directory_list:
    size = 0
    # get size
    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            
            size += os.stat(fp).st_size
    
    # display size       
    file_size = 0
    
    
    if (size > 1073741824):
        file_size = str(round(size/1073741824,2)) + ' GB'
        

    elif (size > 1000000) and (size < 1073741824):
        file_size = str(round(size/1000000,2)) + " MB"

    else:
        file_size = str(round(size/1000,2)) + " KB"   
    
    print(folder)
    Folder_name.append(folder.split("\\")[-1])
    Folder_path.append(folder)
    folder_size.append(file_size)
    size_byte.append(size)



product = ({'Folder_name':Folder_name,'Folder_path':Folder_path,'folder_size':folder_size,"folder_size_in_byte":size_byte})
excels = pd.DataFrame(product)
excels.to_excel('result_File.xlsx',index=False)

