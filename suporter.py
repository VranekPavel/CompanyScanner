import pandas as pd 
import numpy as np 

def num_converter(df):
    for column in df:
        df[column] = df[column].apply(lambda x : x.replace(',', ''))
    return df