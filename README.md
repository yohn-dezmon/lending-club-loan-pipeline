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

To explore the dataset I observed various features. To begin I started by printing the
columns in both the data dictionary and the dataset itself, and by reading the meaning of
each of the 145 columns. From there I observed the shape of the data dictionary and
the dataset, and found that there were several columns present in the data dictionary

One of my first observations was that the id and member_id columns were null. I was initially
planning to normalize the dataset into a relational model within a relational database like
PostgreSQL, however after realizing that there was no unique id, I decided that it would
make more sense to store the entire dataset in a single table in a NoSQL/Columnar database
like Amazon Redshift.

## Main Findings:

Some of the columns had >90% null values, when placed into a database, these could be kept in a 



## Data Processing:

I initially planned to use Apache Spark with Java on a 3 Node EC2 cluster to complete the data processing, however I ran into issues regarding dependency management and ran out of time to troubleshoot them.
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
