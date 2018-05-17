import urllib
import json
import time
import boto3

# file = open('hosts', 'r')
# string = file.readlines()
#
# url = string[3] + '/manage/health'
# file.close()

res = boto3.resource('ec2')
instances = res.instances.filter(Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['application']}]))

for i in instances:
    url = i.public_ip_address + '/manage/health'
    for i in range(6):
        try:
            request = urllib.urlopen(url)
            data = json.loads(request.read())
            break

        except IOError:
            time.sleep(10)
            continue
    
    if data['status'] == 'UP':
        print "Service is up"
