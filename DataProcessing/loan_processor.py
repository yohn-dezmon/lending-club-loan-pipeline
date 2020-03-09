import pandas as pd
import numpy as np
import boto3 # to connect to s3
import json
import xlrd
import os
from collections import defaultdict


class LoanProcessor(object):

    def __init__(self):
        pass

    def get_config_data(self):
        """Get configuration data for s3 and AWS"""
        try:
            with open('config.json') as json_data_file:
                try:
                    # individual configs can be accessed like, configs['key']
                    configs = json.load(json_data_file)
                    return configs
                except json.JSONDecodeError as jsonerr:
                    print(jsonerr)
        except FileNotFoundError as fnf_error:
            print("fnf error: "+str(fnf_error))


    def datadict_from_s3(self, configs):
        """Method to import datadict into a pandas dataframe.
        """
        # access content of excel file with Body keyword, convert to pandas df

        try:
            df = pd.read_excel("s3a://%s" % (configs['dictURL']))
        except xlrd.XLRDError as xlrderr:
            """This error returns when the file is not an excel file. """
            print("xlrderr: "+str(xlrderr))
        except FileNotFoundError as fnf_error:
            print("fnf error: "+str(fnf_error))
        except TypeError as bads3path:
            """ When an incorrect path is given. """
            print("bad s3 path: "+str(nonerr))
        else:
            print(df.head())
            return df

    def loan_chunk_process(self, loan_chunk, mapOfTypes):
        """Process each chunk of 500000 rows"""

        blnklist = []

        shape = df.shape
        if shape[1] != 145:
            print("Incorrect number of columns")

        # Type Checking

        map = defaultdict(list)
        # loan_chunk.dtypes is a Series
        for typ,index in loan_chunk.dtypes.items():
            map[str(typ)].append(index)

        for key in map:
            for column in map[key]:
                if column not in mapOfTypes[key]:
                    print(f"Data type mismatch or new column: {column},{key}")

        # split data into important and less important chunks

        return blnklist


    def get_lists_of_types(self):
        """ Get sets of columns for each type for type checkingn for future
        dataset ingestion"""

        absPath = os.path.abspath(__file__)
        srcPath = os.path.dirname(absPath)
        parentPath = os.path.dirname(srcPath)

        floatsDf = pd.read_csv(f"{parentPath}/DataExploration/floats.csv", names=['cols','vals'])
        set_of_floats = set(floatsDf['cols'])
        intsDf = pd.read_csv(f"{parentPath}/DataExploration/ints.csv", names=['cols','vals'])
        set_of_ints = set(intsDf['cols'])
        textDf = pd.read_csv(f"{parentPath}/DataExploration/text.csv", names=['cols','vals'])
        set_of_ints = set(intsDf['cols'])

        mapOfTypes['float64'] = set_of_floats
        mapOfTypes['int64'] = set_of_ints
        mapOfTypes['object'] = set_of_text
        return mapOfTypes


    def loan_dataset_s3(self, configs):
        """Method to import loan.csv dataset"""
        loan_chunk_list = []
        try:
            # read data into df as pandas chunk object of 500000 rows
            loan_chunk = pd.read_csv("s3a://%s" % (configs['loanURL']),
                                    chunksize=500000)

            processed_chunk = self.loan_chunk_process(loan_chunk)

            loan_chunk_list.append(loan_chunk_list)

            concatenated_chunks = pd.concat(loan_chunk_list)


        except TypeError as bads3path:
            """ When an incorrect path is given. """
            print("bad s3 path: "+str(bads3path))
        else:
            print(df.head())

            return concatenated_chunks



    def split_date_column(self, configs):
        """ Method to split issued date column into year and
        month columns"""
        pass

    """
    This code was used to test connection to s3 using boto3
    def connect_to_s3(self):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
    """

    def main(self):
        self.get_lists_of_types()

        """configs = self.get_config_data()
        # get data dictionary and loan dataset
        data_dict_df = self.datadict_from_s3(configs)
        loan_df = self.loan_dataset_s3(configs)"""







if __name__ == '__main__':

    loanProcessor = LoanProcessor()

    """if len(argv) == 4:
        input = argv[1]
        inactiv_period = argv[2]
        output = argv[3]
        try:
            os.remove(output)
        except:
            pass
    else:
        raise IncorrectCommandLine(argv)"""


# input, inactiv_period, output
    loanProcessor.main()
