import boto3
import csv
import calendar
import datetime



class ReservedInstace:
    def __init__(self):

        self.heading = ["ReservedInstancesId",'OfferingType','InstanceType','InstanceCount','Start','End','FixedPrice','OfferingClass','ProductDescription']

        self.current_date = datetime.datetime.now()
        self.current_month = calendar.month_name[self.current_date.month]
        self.client = boto3.client('ec2')


    def getReservation(self):
        reserved_instance = self.client.describe_reserved_instances()
        return reserved_instance

    def getExpiringReservation(self):
        file_name = "%s_expiring_reservations.csv"%self.current_month
        file = open(file_name,'w+')
        writer = csv.writer(file,delimiter=',')

        writer.writerow(self.heading)

        ri = self.getReservation()
        for instances in ri['ReservedInstances']:
            if instances['State'] != "retired" :
                end_date = instances['End']
                if end_date.year == self.current_date.year:

                    if end_date.month == self.current_date.month:
                        writer.writerow([instances['ReservedInstancesId'],instances['OfferingType'],instances['InstanceType'],instances['InstanceCount'],instances['Start'],instances['End'],instances['FixedPrice'],instances['OfferingClass'],instances['ProductDescription']])

        file.close()

    def getTotalReservation(self):
        file_name = "total_reservations.csv"
        file = open(file_name,'w+')
        writer = csv.writer(file,delimiter=',')

        writer.writerow(self.heading)

        ri = self.getReservation()

        for instances in ri['ReservedInstances']:
            if instances['State'] != "retired":
                writer.writerow([instances['ReservedInstancesId'], instances['OfferingType'], instances['InstanceType'],instances['InstanceCount'], instances['Start'], instances['End'],instances['FixedPrice'], instances['OfferingClass'], instances['ProductDescription']])
        file.close()

