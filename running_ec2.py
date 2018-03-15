import boto3


client = boto3.client('ec2')

instances = client.describe_instances()

print instances['Reservations'][0]