import boto3
import pandas as pd
import xlrd
import s3fs
from loan_processor import LoanProcessor

def datadict_to_s3():
    """Method to write data_dict to s3 as a csv file
    for later ingestion into PySpark.
    """
    lp = LoanProcessor()
    configs = lp.get_config_data()
    # access content of excel file with Body keyword, convert to pandas df
    df = pd.read_excel("s3a://%s" % (configs['dictURL']), index=False)
    print(df.head())
    # write data as csv to s3 using s3fs behind the scenes
    df.to_csv("s3a://%s" % (configs['dictURLcsv']), index=False)


    """
    def read_from_s3(self, configs):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
        s3Objs = {}
        s3Objs['loan_csv'] = s3.get_object(Bucket=configs['bucketName'], Key=configs['loanKey'])
        s3Objs['dataDict'] = s3.get_object(Bucket=configs['bucketName'], Key=configs['dataDictKey'])
        return s3Objs
    """


if __name__ == '__main__':


    datadict_to_s3()
