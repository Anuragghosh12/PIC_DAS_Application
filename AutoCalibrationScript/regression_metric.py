import pandas as pd
from time import gmtime, strftime
import numpy as np

def main():
    curr_time = str(strftime('%Y%m%d', gmtime()))+'_' + 'C002_' + '1' + '_P001_' + '1_data.csv'
    df= pd.read_csv()

if __name__ == '__main__':
    main()