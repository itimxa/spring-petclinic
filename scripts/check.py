import urllib
import json
import time
import boto3


res = boto3.resource('ec2')
instances = res.instances.filter(Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['application']}])

for i in instances:
    url =  'http://' + i.public_ip_address + ':8080/manage/health'
    for i in range(6):
        try:
            request = urllib.request.urlopen(url)
            data = json.loads(request.read().decode('utf-8'))
            break

        except IOError:
            time.sleep(10)
            continue
    
    if data['status'] == 'UP':
        print ("Service is up")
