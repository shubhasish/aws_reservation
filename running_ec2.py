import boto3
import calendar
import datetime
import csv


current_date = datetime.datetime.now()
current_month = calendar.month_name[current_date.month]

file_name = "%s_running.csv"%current_month
file = open(file_name,'w+')
writer = csv.writer(file,delimiter=',')

heading = ['Name','Environment','State','Instance_Type','Platform','Launch_Time','Public_DNS_Name']
writer.writerow(heading)

client = boto3.client('ec2')


instances = client.describe_instances()



for instance_key in  instances['Reservations']:
    instance = instance_key['Instances'][0]
    print instance
    public_dns = 'N.A'
    environment = 'N.A'
    platform = 'N.A'
    name = 'N.A'
    if 'PublicDnsName' in instance:
        public_dns = instance['PublicDnsName']
    state = instance['State']['Name']
    instance_type = instance['InstanceType']
    launch_time = instance['LaunchTime']
    if 'Tags' in instance:
        tags = instance['Tags']
        for tag in tags:
            if tag['Key'] == 'environment' :
                environment = tag['Value']
            if tag['Key'] == 'Name':
                name = tag['Value']
    if 'Platform' in instance:
        platform = instance['Platform']
    writer.writerow([name,environment,state,instance_type,platform,launch_time,public_dns])

file.close()