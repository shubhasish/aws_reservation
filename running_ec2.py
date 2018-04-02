import boto3
import calendar
import datetime
import csv






class Instances:
    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.current_month = calendar.month_name[self.current_date.month]

    def getRunningInstanceSheet(self):
        file_name = "%s_running.csv"%self.current_month
        file = open(file_name,'w+')
        writer = csv.writer(file,delimiter=',')
        heading = ['Name','Environment','State','Instance_Type','Instance_Id','Platform','Launch_Time','Public_DNS_Name']
        writer.writerow(heading)
        client = boto3.client('ec2')
        instances = client.describe_instances()

        for instance_key in  instances['Reservations']:
            instance = instance_key['Instances'][0]

            public_dns = 'N.A'
            environment = 'UNTAGGED'
            platform = 'Linux'
            name = 'N.A'
            if 'PublicDnsName' in instance:
                public_dns = instance['PublicDnsName']
                state = instance['State']['Name']
                instance_type = instance['InstanceType']
                instance_id = instance['InstanceId']
                launch_time = instance['LaunchTime']
                if 'Tags' in instance:
                    tags = instance['Tags']
                    for tag in tags:
                        if tag['Key'] == 'environment' or tag['Key'] == 'Environment':
                            environment = tag['Value']
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                        if 'Platform' in instance:
                            platform = instance['Platform']
            writer.writerow([name,environment,state,instance_type,instance_id,platform,launch_time,public_dns])

        file.close()

inst = Instances()

inst.getRunningInstanceSheet()
