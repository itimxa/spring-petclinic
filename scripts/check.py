import urllib
import json
import time
import boto3
import warnings


res = boto3.resource('ec2')
instances = res.instances.filter(Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['application']}])

counter = 0
working_apps = []
down_apps = []
for i in instances:
    url =  'http://' + i.public_ip_address + ':8080/manage/health'
    counter += 1
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
            working_apps.append(i.public_ip_address)

    except NameError:
        down_apps.append(i.public_ip_address)

if len(working_apps) == counter:
    print('All applications are working properly.\nList of instances:\n' + '\n'.join(working_apps))
elif not working_apps:  # Check if this list is empty
    raise TimeoutError ("No response from application on all hosts:\n" + '\n'.join(down_apps))
else:
    warnings.warn("No response from application on hosts:\n" + '\n'.join(down_apps))
    print('Next applications are working properly:\n' + '\n'.join(working_apps))
