import boto3


tags = ('application', 'database')
instances_ids = []
resource = boto3.resource('ec2')

for name in tags:
    instances = resource.instances.filter(Filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': [name]}])
    for inst in instances:
        instances_ids.append(inst.id)


resource.instances.filter(InstanceIds=instances_ids).terminate()
