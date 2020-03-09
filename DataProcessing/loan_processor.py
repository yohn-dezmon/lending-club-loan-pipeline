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
        with open('config.json') as json_data_file:

            try:
            # a dictionary
                configs = json.load(json_data_file)
                return configs
            except json.JSONDecodeError as jsonerr:
                print(jsonerr)


    def datadict_from_s3(self, configs):
        """Method to write data_dict to s3 as a csv file
        for later ingestion into PySpark.
        """
        # access content of excel file with Body keyword, convert to pandas df
        '''TODO: SET UP A TRY CATCH BLOCK FOR WHEN FILE IS NOT EXCEL '''

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
        print(df.head())



    def connect_to_s3(self):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)

    def main(self):
        self.connect_to_s3()
        configs = self.get_config_data()
        self.datadict_from_s3(configs)



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
