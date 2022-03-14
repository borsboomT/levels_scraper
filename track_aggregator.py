import glob
from operator import index
import os
import pandas as pd
from pandas.errors import EmptyDataError

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

track_name='Software%20Engineer_YOE'
track = "Track{}*".format(track_name)

file_list = glob.glob('./data/{}'.format(track))

df = pd.DataFrame()
for file in file_list:
    try:
        temp_df = pd.read_csv(file,header=0,index_col=False)
        if not temp_df.empty:
            df = pd.concat([df,temp_df])
    except EmptyDataError as e:
        print(e)
        print(file)
        continue

track_name_clean = track_name.replace("%20",'').replace("_YOE",'')
df.to_csv("./data/{}_completeCSV.csv".format(track_name_clean),index=False)