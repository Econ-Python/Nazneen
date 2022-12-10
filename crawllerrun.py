# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 18:19:51 2022

@author: nazne

Instruction -  save all these python file or directly save this folder in one folder for easy analysis in spyder
"""
# Part-1 fetching Data from the  DEPARTMENT OF CONSUMER AFFAIRS website for Feb, March, April

import os
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta

os.getcwd()

from prices import PricesSpider
from scrapy.crawler import CrawlerProcess

in_path = os.getcwd()
#making a folder where all the data downloaded will be saved
# do not change this folder name
folder_name = "ISB_data"
# data output path
out_path = in_path + "\\" + folder_name
os.makedirs(out_path)

os.chdir(out_path)

#date ps name after each execution otherwise reaction error will persist
ps = CrawlerProcess()  
ps.crawl(PricesSpider)
ps.start()  


#Part-1 cleaning data and coverting it in panel data format

# make a new folder in the path 

"""
1. get working directory
2. read all the file download file from scrapy in that directory
3. categories data based on center and date
4. append all data in one file
"""

dir_list = os.listdir(out_path) 
print("Files and directories in '", out_path, "' :") 
# prints all files
print(dir_list)

# reading all the files in the directory
df_final = pd.DataFrame()
for file in dir_list:
 
    df = pd.read_csv(file)
    df.head()
    df.columns
    df_new = df.copy()
    df_new = df_new[2:]
    df_new = df_new.iloc[:-9]
    df_new.columns = df_new.iloc[0]
    df_new.drop(df_new.index[0], inplace =True)
    print(df_new.columns)
    
    name = re.findall(r"[\w]+", file)
    name = name[0].split("_")
    Date = name[1]+ "/" + name[2] + "/" + name[3]
    
    df_new["Date"] = datetime.strptime(Date, "%d/%m/%Y")
    #ust10 = m4_data.loc[:, ["Date2", "UST10Y"]].set_index("Date2")
    df_new2 = df_new.set_index("Date")
    # change this list based on commodities name list printed in column name printing above
    df_new2 = df_new2[['Centre','Rice', 'Wheat','Atta (Wheat)', 'Gram Dal','Tur/Arhar Dal',  'Urad Dal','Moong Dal', 'Masoor Dal', 'Sugar',  'Milk @',
           'Groundnut Oil (Packed)','Mustard Oil (Packed)','Vanaspati (Packed)','Soya Oil (Packed)',
    'Sunflower Oil (Packed)', 'Palm Oil (Packed)', 'Gur', 'Tea Loose','Salt Pack (Iodised)', 'Potato','Onion', 'Tomato']]
   
    df_final = df_final.append(df_new2)

df_final.to_csv(r'./final_output_panel_data.csv')
# Treatment of final output for blank and NR rows

df_final.dropna(inplace = True)
#dat2 = dat.replace(r'^([A-Za-z]|[0-9]|_)+$', np.NaN, regex=True)
df_final1 = df_final.replace("NR", np.NaN) 
df_final1["Date_2"] = df_final1.index
#df.insert(0, 'New_ID', range(880, 880 + len(df)))
df_final1.insert(0, "ID", range(1, 1+len(df_final1)))
# drop rows with all values in commodities column as NaN

df_final_filter = df_final1[['ID','Rice', 'Wheat','Atta (Wheat)', 'Gram Dal','Tur/Arhar Dal',  'Urad Dal','Moong Dal', 'Masoor Dal', 'Sugar',  'Milk @',
       'Groundnut Oil (Packed)','Mustard Oil (Packed)','Vanaspati (Packed)','Soya Oil (Packed)',
'Sunflower Oil (Packed)', 'Palm Oil (Packed)', 'Gur', 'Tea Loose','Salt Pack (Iodised)', 'Potato','Onion', 'Tomato']]

df_final_filter = df_final_filter.set_index("ID")
df_final_filter2 = df_final_filter.dropna(thresh =1)
df_final_filter2["New_ID"] = df_final_filter2.index

df_final1.rename(columns = {"ID" :"New_ID"}, inplace=True)
df_meta = df_final1[["New_ID", "Centre", "Date_2"]]
# merge with old data to get centre name again in the filtered data
cleaned_data2 = df_final_filter2.merge(df_meta, on = "New_ID", how = "left")

# arrage column order
cleaned_data2 = cleaned_data2[[ 'Date_2', 'Centre','Rice', 'Wheat', 'Atta (Wheat)', 'Gram Dal', 'Tur/Arhar Dal',
       'Urad Dal', 'Moong Dal', 'Masoor Dal', 'Sugar', 'Milk @',
       'Groundnut Oil (Packed)', 'Mustard Oil (Packed)', 'Vanaspati (Packed)',
       'Soya Oil (Packed)', 'Sunflower Oil (Packed)', 'Palm Oil (Packed)',
       'Gur', 'Tea Loose', 'Salt Pack (Iodised)', 'Potato', 'Onion', 'Tomato']]

# exporting final output in cleaned Panel Data Format
cleaned_data2.to_csv(r'./cleaned_output_panel_data_4.csv', index= False)



