import re

from urllib.request import urlretrieve
from zipfile import ZipFile
from itertools import chain

import pandas as pd


##Global Variables

file_address = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00395/PARKINSON_HW.zip'
pattern = re.compile('.+\/.+[CPH]+.+\.txt$')
column_names = ['X' , 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp', 'Test ID']

##Data Reading Functions

def retrieve_uci_data(file = file_address, name = 'parkinsons.zip',pattern = pattern, group = 'control'):

	''' get zip file and extract parkinsons data into the control and parkinsons groups

	file: string; the zip file from the public UCI repository
	name: string; name to feed into urlretrieve function
	pattern: string; first pattern (regex) for identifying relevant files in zip
	group: string; used for regex string. Should only be 'control' or 'parkinson'
	
	'''
    
	zip_retrieved = urlretrieve(file,name)
	zip_get = ZipFile(zip_retrieved[0],'r')

	list_of_texts = sorted(list(set(chain.from_iterable([re.findall(pattern,i) for i in zip_get.namelist()]))))

	group_pattern = r'.*\/{}\/.*\.txt$'.format(group)

	group_files = sorted(list(chain.from_iterable([re.findall(group_pattern,i) for i in list_of_texts])))

	return group_files

def normalize_df(df):
    
    '''Take the numeric columns of DataFrame and normalize for scaled evaluation of distributions
    
    df: pandas DataFrame; for transformation, non-numeric columns will be moved to end'''
    
    assert isinstance(df,pd.DataFrame), "please use a Pandas DataFrame"
    
    non_number = df.select_dtypes(exclude=['number'])
    
    df = df.drop(list(non_number.columns),axis=1)
    
    df = df.apply(lambda x: (x - x.mean())/x.std(),axis=0)
    
    df = pd.concat([df,non_number],axis=1)
    
    return df

def make_combined_df(filelist, rolling =  True, periods = 1, window = 100, columns = column_names,normalize = False):

    df_list = [pd.read_csv(filelist[i],';',names=columns) for i,v in enumerate(filelist)]

    combined_df = pd.DataFrame()

    for i, df in enumerate(df_list):
        
        for x in list(df['Test ID'].unique()):
            new_df = df[df['Test ID'] == x]
            new_df['Subject'] = i
            new_df['ZeroedTimestamp'] = new_df['Timestamp'] - new_df['Timestamp'].min()

        if rolling:
            new_df['X_diff'] = new_df['X'].diff(periods)
            new_df['Y_diff'] = new_df['Y'].diff(periods)
            new_df['X_diff_avg_{}'.format(window)] = new_df['X_diff'].rolling(window).mean()
            new_df['Y_diff_avg_{}'.format(window)] = new_df['Y_diff'].rolling(window).mean()
        	
            combined_df = combined_df.append(new_df,ignore_index=True)
        
        if normalize:
            combined_df = normalize(combined_df)
            
    return combined_df