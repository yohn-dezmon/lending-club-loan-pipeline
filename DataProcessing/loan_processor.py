import pandas as pd
import numpy as np
import boto3 # to connect to s3


class LoanProcessor(object):

    def __init__(self):
        pass

    def connect_to_s3(self):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)

    def main(self):
        self.connect_to_s3()




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
