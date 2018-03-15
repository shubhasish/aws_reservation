import boto3
import csv

march = open('march.csv','w+')
may = open('may.csv','w+')
sep = open('sep.csv','w+')
nov = open('nov.csv','w+')

march_writer = csv.writer(march,delimiter=',')
may_writer = csv.writer(may)
sep_writer = csv.writer(sep)
nov_writer = csv.writer(nov)

heading = ["ReservedInstancesId",'OfferingType','InstanceType','InstanceCount','Start','End','FixedPrice','OfferingClass','ProductDescription']

march_row = []
may_row = []
sep_row = []
nov_row = []

march_row.append(heading)
may_row.append(heading)
sep_row.append(heading)
nov_row.append(heading)
# may_writer.writerows(['ReservedInstancesId','OfferingType','InstanceType','InstanceCount','Start','End','FixedPrice','OfferingClass','ProductDescription'])
# sep_writer.writerows(['ReservedInstancesId','OfferingType','InstanceType','InstanceCount','Start','End','FixedPrice','OfferingClass','ProductDescription'])
# nov_writer.writerows(['ReservedInstancesId','OfferingType','InstanceType','InstanceCount','Start','End','FixedPrice','OfferingClass','ProductDescription'])

client = boto3.client('ec2')

reserved_instance = client.describe_reserved_instances()

for instances in reserved_instance['ReservedInstances']:
    if instances['State'] != "retired" :
        end_date = instances['End']
        if end_date.year == 2018:
            if end_date.month == 3:
                march_row.append([instances['ReservedInstancesId'],instances['OfferingType'],instances['InstanceType'],instances['InstanceCount'],instances['Start'],instances['End'],instances['FixedPrice'],instances['OfferingClass'],instances['ProductDescription']])
            elif end_date.month == 5:
                may_row.append([instances['ReservedInstancesId'],instances['OfferingType'],instances['InstanceType'],instances['InstanceCount'],instances['Start'],instances['End'],instances['FixedPrice'],instances['OfferingClass'],instances['ProductDescription']])
            elif end_date.month == 9:
                sep_row.append([instances['ReservedInstancesId'],instances['OfferingType'],instances['InstanceType'],instances['InstanceCount'],instances['Start'],instances['End'],instances['FixedPrice'],instances['OfferingClass'],instances['ProductDescription']])
            elif end_date.month == 11:
                nov_row.append([instances['ReservedInstancesId'],instances['OfferingType'],instances['InstanceType'],instances['InstanceCount'],instances['Start'],instances['End'],instances['FixedPrice'],instances['OfferingClass'],instances['ProductDescription']])


march_writer.writerows(march_row)
may_writer.writerows(may_row)
sep_writer.writerows(sep_row)
nov_writer.writerows(nov_row)

march.close()
may.close()
sep.close()
nov.close()