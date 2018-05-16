#!/usr/bin/python
import boto3
import sys
#import os

try:

    app_instances_quantity = sys.argv[1]
    try:
        filter_key = sys.argv[2]
        my_filter = [{'Name': 'tag:Name', 'Values': [filter_key]}]
    except IndexError:
        my_filter =  [{'Name': 'tag:Name', 'Values': ['vadim*']}]

except ValueError:
    raise "First argumet should be integer"

except IndexError:
    app_instances_quantity = 1
    my_filter = [{'Name': 'tag:Name', 'Values': ['vadim*']}]

# get my subnet name

client = boto3.client('ec2')
sub_responce = client.describe_subnets(Filters = my_filter)
subnet_id = sub_responce['Subnets'][0]['SubnetId']

# get security_groups

sec_responce = client.describe_security_groups(Filters = my_filter)

# VARS
app_instances_quantity = 1  # specify quantity of our application instances
db_private_ip = '10.10.0.115'
image_id = 'ami-43eec3a8'
instance_type = 't2.micro'
sec_group_id = sec_responce['SecurityGroups'][0]['GroupId']
subnet_id = sub_responce['Subnets'][0]['SubnetId']


# user_data_script = '''#!/bin/bash
#            sudo yum update -y
#            sudo yum install java-1.8.0-openjdk-devel'''
resource = boto3.resource('ec2')

db_machine = resource.create_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    MaxCount=1,
    MinCount=1,
    KeyName='VDMss',
    NetworkInterfaces=[
        {'SubnetId': subnet_id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group_id],
         'PrivateIpAddress': db_private_ip}],
    TagSpecifications=[
        {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value' : 'database'}]}
    ]
)

for i in range(app_instances_quantity):
    app_machine = resource.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MaxCount=1,
        MinCount=1,
        KeyName='VDMss',
        NetworkInterfaces=[
            {'SubnetId': subnet_id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group_id]}],
        TagSpecifications=[
            {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value' : 'application'}]}
            ]#,
        #UserData=user_data_script
    )

db_machine[0].wait_until_running()
app_machine[0].wait_until_running()

db_ipaddr = client.describe_instances(
    Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': 'tag:Name', 'Values': ['database']}])['Reservations'][0]['Instances'][0]['PublicIpAddress']
print(db_ipaddr)

app_ip_addresses = []
for i in range(app_instances_quantity):
    app_ip_addresses.append(client.describe_instances(
        Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['application']}])['Reservations'][i]['Instances'][0]['PublicIpAddress'])
print(app_ip_addresses)


def create_file(db_ip, app_ip):
    file = open('hosts', 'w')
    file.write('[DB_M]\n{}\n[APP_M]\n'.format(str(db_ip)))
    for ip in app_ip:
        file.write('%s\n' % (ip))
    file.close()

create_file(db_ipaddr, app_ip_addresses)