import pandas as pd
import numpy as np
import boto3 # to connect to s3
import json
import xlrd


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
            df = pd.read_excel("s3a://%s" % (configs['dictURL']), index=False)
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

    def import_loan_dataset_s3(self, configs):
        """Method to import loan.csv dataset"""
        try:
            df = pd.read_csv("s3a://%s" % (configs['loanURL']), index=False)

        except TypeError as bads3path:
            """ When an incorrect path is given. """
            print("bad s3 path: "+str(nonerr))
        else:
            print(df.head())

            shape = df.shape
            if shape[1] != 145:
                print("Incorrect number of columns")

            return df

    """
    This code was used to test connection to s3 using boto3
    def connect_to_s3(self):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
    """

    def main(self):
        self.connect_to_s3()
        configs = self.get_config_data()
        data_dict_df = self.datadict_from_s3(configs)
        loan_df = self.






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
