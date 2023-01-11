import os
import shutil 
import pandas as pd


# print(remove(os.path.join(os.getcwd(),file))

def clear_dir(path):
        try:
            for base in os.listdir(path):
                os.remove(os.path.join(path,base)) if os.path.isfile(os.path.join(path,base)) else shutil.rmtree(os.path.join(path,base))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))



# folder_path = r"C:\Users\Anjali_SEQ\Desktop\Milled"
# clear_dir(folder_path)

df = pd.read_csv(r"C:\Users\Anjali_SEQ\Desktop\read.csv") #read input file
for col in range(len(df)):
    folder_paths = df['Folder_path'].iloc[col]
    print(folder_paths)
    clear_dir(folder_paths)

