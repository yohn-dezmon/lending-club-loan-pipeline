# Lending Club Loan Pipeline

## Table of Contents

1. [Purpose](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#purpose)
2. [Data Exploration](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#data-exploration)
3. [Data Processing](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#data-processing)
4. [Redshift Setup](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#redshift-setup)


## Purpose:
The purpose of this project is to (1) explore the (lending club loan dataset)[https://www.kaggle.com/wendykan/lending-club-loan-data] from kaggle to extract the important
features for data analysis and (2) to create a pipeline that would ingest, process,
and store this data on a periodic basis to be placed into storage such that it could be easily accessed by a data warehouse application, or to be used for machine learning model creation.

## Data Exploration:

To explore the dataset I observed various features. To begin

## Data Processing:

I initially planned to use Apache Spark with Java on a 3 Node EC2 cluster to complete the data processing, however I ran into issues regarding dependency management and ran out of
time to troubleshoot them.
Thus I decided ultimately to complete the processing using pandas in Python. To see the instructions I wrote on how to set up the AWS computing cluster, please see my commits prior to the commit "updated readme to plain python".


## Redshift setup:

I setup Redshift by following the instructions found (here)[https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html].
I had to create a IAM Role specifically for redshift which is covered in step 2.
To connect to Redshift from my local computer, I had to modify the security group's
inbound rules as follows:

[**Source is left blank as it will be specific to your AWS account**]

| Type | Source | Description |
|-----------|---------|----------------|
| Redshift | <local-ip> | local-ip |
| All traffic | <spark-security-group> | self |
