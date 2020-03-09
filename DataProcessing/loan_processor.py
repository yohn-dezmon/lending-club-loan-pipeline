import pandas as pd
import numpy as np
import boto3 # to connect to s3
import json
import xlrd
import os
from collections import defaultdict


class LoanProcessor(object):
    """A class to validate the data from the loan dataset before ingesting into Redshift."""

    def __init__(self):
        pass

    def get_config_data(self):
        """Get configuration data for s3 and AWS."""
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
        """Process the large loan.csv file."""

        # check the dataframe to see if it has the correct number of columns
        shape = loan_chunk.shape
        if shape[1] != 145:
            print("Incorrect number of columns")

        # Type Checking
        map = defaultdict(list)
        # loan_chunk.dtypes is a Series
        for index,typ in loan_chunk.dtypes.items():
            map[str(typ)].append(index)

        # pdb.set_trace()
        for key in map:
            for column in map[key]:
                if column not in mapOfTypes[key]:
                    print(f"Data type mismatch or new column: {column},{key}")


        # split data into important and less important chunks

        return loan_chunk


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
        set_of_text = set(textDf['cols'])

        mapOfTypes = {}

        mapOfTypes['float64'] = set_of_floats
        mapOfTypes['int64'] = set_of_ints
        mapOfTypes['object'] = set_of_text
        return mapOfTypes


    def loan_dataset_s3(self, configs, mapOfTypes):
        """Method to import loan.csv dataset"""
        try:
            # read data into df as pandas chunk object of 500000 rows
            loan_large_csv = pd.read_csv("s3a://%s" % (configs['loanURL']))

        except TypeError as bads3path:
            """ When an incorrect path is given. """
            print("bad s3 path: "+str(bads3path))
        else:
            print(loan_large_csv.head())
            self.loan_chunk_process(loan_large_csv, mapOfTypes)
            return loan_large_csv


    def split_date_column(self, configs):
        """ Method to split issued date column into year and
        month columns"""
        pass



    def main(self):
        mapOfTypes = self.get_lists_of_types()
        # get aws and s3 configuration values
        configs = self.get_config_data()
        # get data dictionary and loan dataset
        data_dict_df = self.datadict_from_s3(configs)
        loan_df = self.loan_dataset_s3(configs, mapOfTypes)



if __name__ == '__main__':

    loanProcessor = LoanProcessor()

    """if len(argv) == 2:
        input = argv[0]
        output = argv[1]
        try:
            os.remove(output)
        except:
            pass
    else:
        raise IncorrectCommandLine(argv)"""


    loanProcessor.main()
