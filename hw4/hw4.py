import pandas as pd
import os
import glob

# use glob to get all the csv files
# in the folder
pos = os.path.join(os.getcwd(),"course_files_export", "Movie_Reviews", "pos", "*.txt")
neg = os.path.join(os.getcwd(),"course_files_export", "Movie_Reviews", "pos", "*.txt")


csv_files = glob.glob(pos)
print(len(csv_files))
li = []
col_names = ["reivew"]
for filename in csv_files:
    print("working on " + filename)
    df = pd.read_fwf(pos, names = col_names, lineterminator=':', index_col=None, header=None)
    li.append(df)

frame = pd.concat(li, sort=False, ignore_index=True)
len(frame.count())