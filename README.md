# Lending Club Loan Pipeline

## Table of Contents

1. [Purpose](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#purpose)


## Purpose:
The purpose of this project is to (1) explore the (lending club loan dataset)[https://www.kaggle.com/wendykan/lending-club-loan-data] from kaggle to extract the important
features for data analysis and (2) to create a pipeline that would ingest, process,
and store this data on a periodic basis to be placed into storage such that it could be easily accessed by a data warehouse application, or to be used for machine learning model creation.  


## AWS Setup:

On the default tab, “VPC with a Single Public Subnet”, click Select. (The subnet is a subset of the whole AWS network that is available.)
On “Step 2”, you’ll need to change a few bits of information:
IPv4 CIDR Block: 10.0.0.0/26
VPC Name: my-name-vpc
Public Subnet’s IPv4 CIDR: 10.0.0.0/28
Everything else can be left as the default
Then click “Create VPC”
