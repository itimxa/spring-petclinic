import urllib
import json
import time
import boto3


res = boto3.resource('ec2')
instances = res.instances.filter(Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['application']}])

for i in instances:
    url =  'http://' + i.public_ip_address + ':8080/manage/health'
    for j in range(6):
        try:
            request = urllib.request.urlopen(url)
            data = json.loads(request.read().decode('utf-8'))
            break

        except IOError:
            time.sleep(10)
            continue
    try:
        if data['status'] == 'UP':
            print ("Service with ip %s is running" % (i.public_ip_address))

    except NameError:
        raise ConnectionError("No response from ip %s" % (i.public_ip_address))