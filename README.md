# Lending Club Loan Pipeline

## Table of Contents

1. [Purpose](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#purpose)
2. [AWS Setup](https://github.com/github.com/yohn-dezmon/lending-club-loan-pipeline#aws-setup)


## Purpose:
The purpose of this project is to (1) explore the (lending club loan dataset)[https://www.kaggle.com/wendykan/lending-club-loan-data] from kaggle to extract the important
features for data analysis and (2) to create a pipeline that would ingest, process,
and store this data on a periodic basis to be placed into storage such that it could be easily accessed by a data warehouse application, or to be used for machine learning model creation.  


## AWS Setup:


### VPC and Subnet setup:

Go to your AWS console, and navigate to the VPC page.  
On the default tab find “VPC with a Single Public Subnet”, click Select.  
On “Step 2”, you’ll need to change a few bits of information:
```
IPv4 CIDR Block: 10.0.0.0/26
VPC Name: <name-of-vpc>
Public Subnet’s IPv4 CIDR: 10.0.0.0/28
```
Everything else can be left as the default
Then click “Create VPC”

### Security Groups:

You'll need to create two security groups, one for your Spark cluster
and another for your Database EC2 instance.

Go to the EC2 page on the AWS console, navigate to the security groups
sub page and click "Create Security Group".
Initially just open the SSH connection to both security groups.

Modify the in-bound rules for the Spark Cluster security group as follows:

| Type | Source | Description |
|-----------|---------|----------------|
| Redshift | <database-security-group> | loan-database |
| All traffic | <spark-security-group> | self |
| SSH | <local-ip> | office ip |

Leave the outbound as open to all traffic.

Modify the in-bound rules for the Database EC2 security group as follows:

| Type | Source | Description |
|-----------|---------|----------------|
| Redshift | <spark-security-group> | computing-spark-loan |
| All traffic | <database-security-group> | self |
| SSH | <local-ip> | office ip |

And the outbound rules as follows:

| Type | Source | Description |
|-----------|---------|----------------|
| Redshift | <spark-security-group> | computing-spark-loan |
| All traffic | <database-security-group> | self |




### Creating clusters

To create the clusters I downloaded the [Pegasus](https://github.com/InsightDataScience/pegasus) package from Insight and followed the instructions found on the readme. Please clone pegasus onto your local computer and follow the instructions for setting up the AWS command line tool and peg command line tool.

After installing pegasus, I created one cluster called 'kafka' consisting of three nodes. This assumes you have already set up security groups, subnets and a VPC on your AWS account.
Below is the .yml file I used by calling peg up kafka3.yml


```
purchase_type: on_demand
subnet_id: <subnet_id>
num_instances: <num_of_instances>
key_name: <keypair_filename>
security_group_ids: <security_group_ids>
instance_type: m4.large
tag_name: <cluster_name>
vol_size: 100
role: master
use_eips: true
```
