import pandas as pd
import numpy as np
import boto3 # to connect to s3
import json
import xlrd
import os
from collections import defaultdict
from loan_processor import LoanProcessor


class CSVSplitter(object):
    """Class to split CSV into smaller chunks and store them in S3
    """

    def __init__(self):
        pass

    def get_column_names(self, loan_lage_csv):
        pass

    """
    def split_csv(self):
        """ 'Split the CSV into smaller chunks'"""
        current_id = ''
        index = 0
        written_lines = 0
        max_lines = 400000

        try:
            with open('data.csv', 'r') as input_file:
                for line in input_file:
                    values = line.split(',')
                    if (current_id != values[0]) or (written_lines > max_lines):
                        index += 1
                        current_id = values[0]
                    with open('output_{:08d}.csv'.format(index), 'a') as output_file:
                        output_file.write(line)
                        written_lines += 1
        except:"""



    def main(self):
        lp = LoanProcessor()
        mapOfTypes = lp.get_lists_of_types()
        configs = lp.get_config_data()
        loan_large_csv = lp.loan_dataset_s3(configs, mapOfTypes)

        self.get_column_names(loan_large_csv)
