import boto3
import datetime


class CostExplorer:

    def __init__(self):
        self.client = boto3.client('ce')
        self.reservation_coverage_dict = dict()

    def getReservationCoverage(self):
        current_date = datetime.datetime.now()
        start_date = "%s-0%s-01"%(current_date.year,current_date.month)
        end_date = "%s-0%s-%s" % (current_date.year, current_date.month,current_date.day)
        response = self.client.get_reservation_coverage(TimePeriod={'Start':start_date,'End':end_date},GroupBy=[{'Type':'DIMENSION','Key':'INSTANCE_TYPE'}])

        self.reservationSorter(response)


    def getReservationUtilization(self):
        current_date = datetime.datetime.now()
        start_date = "%s-0%s-01" % (current_date.year, current_date.month)
        end_date = "%s-0%s-%s" % (current_date.year, current_date.month, current_date.day)
        response = self.client.get_reservation_utilization(TimePeriod={'Start': start_date, 'End': end_date},GroupBy=[{'Type': 'DIMENSION', 'Key': 'SUBSCRIPTION_ID'}])
        print response
    def reservationSorter(self,response):
        instances = response['CoveragesByTime'][0]['Groups']

        for instance in instances:
            self.reservation_coverage_dict[instance['Attributes']['instanceType']] = instance['Coverage']





importer = CostExplorer()
importer.getReservationUtilization()

# client = boto3.client('ce')
#
# print client.get_reservation_coverage(TimePeriod={'Start':'2018-03-01','End':'2018-03-15'},GroupBy=[{'Type':'DIMENSION','Key':'INSTANCE_TYPE'}])

# print client.get_cost_and_usage(TimePeriod={'Start':'2018-03-01','End':'2018-03-15'},Granularity='MONTHLY',Metrics=['UnblendedCost'],GroupBy=[{'Type':'DIMENSION','Key':'SERVICE'}])