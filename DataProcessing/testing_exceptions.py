import pandas as pd
import xlrd

try:
    # df = pd.read_excel("test.csv")
    df2 = pd.read_excel("bobcat.excel")
except xlrd.XLRDError as xlrderr:
    print("xlrderr: "+str(xlrderr))
except FileNotFoundError as fnf_error:
    print("fnf error: "+str(fnf_error))
