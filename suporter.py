import pandas as pd 
import numpy as np 
from datetime import datetime

def num_converter(df):
    for column in df:
        df[column] = df[column].apply(lambda x : x.replace(',', ''))
    return df

def to_datetime(series):
    series = series.apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
    return series