import pandas as pd
import numpy as np
import s3fs
import json
import boto3 # to connect to s3
from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession

class LoanProcessor(object):

    def __init__(self):
        pass

    def get_config_data(self):
        with open('config.json') as json_data_file:
            # a dictionary
            configs = json.load(json_data_file)

            return configs


    def start_pyspark(self, configs):
        sc = SparkContext()
        hadoopConf = sc._jsc.hadoopConfiguration()
        hadoopConf.set("fs.s3a.awsAccessKeyId", configs['accessKey'])
        hadoopConf.set("fs.s3a.awsSecretAccessKey", configs['secretKey'])
        hadoopConf.set("fs.s3a.endpoint", "https://lending-club-loan-pipeline.s3.amazonaws.com")
        hadoopConf.set("com.amazonaws.services.s3a.enableV4", "true")
        hadoopConf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

        spark = SparkSession(sc).builder.master(configs['master']).appName("LoanProcessor").getOrCreate()
        # %s order = access key | secret key | s3URL
        # DATA VALIDATION PLZ
        # loans = spark.read.csv("s3a://%s" % (configs['loanURL']))
        # loans.show()

        datadict = spark.read.csv("s3a://%s" % (configs['dictURLcsv']))
        # datadict = spark.read.csv("s3a://%s:%s@%s" % (configs['accessKey'], configs['secretKey'], configs['dictURLcsv']))
        datadict.show()

        # loans = spark.read.csv("s3a://%s:%s@%s" % (configs['accessKey'], configs['secretKey'], configs['loanURL']))




    def main(self):
        # get bucket name and bucket key from configs.json
        configs = self.get_config_data()
        # write datadict to s3

        # get s3_obj for csv file stored in s3
        # s3_objs = self.read_from_s3(configs)
        self.start_pyspark(configs)



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
