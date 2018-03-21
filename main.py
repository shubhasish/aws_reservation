import csv
import datetime
import calendar
from cost_explorer import CostExplorer
import copy
from reserved_ec2 import ReservedInstace
from running_ec2 import Instances

class ReadCSV:

    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.current_month = calendar.month_name[self.current_date.month]
        self.running_instance_dict = dict()
        self.ri_instance_dict = dict()
        self.expiring_ri_dict = dict()
        self.reservation_coverage_dict = dict()
        self.environment_dict = dict()
        self.instance_env_mapper_dict = dict()
        self.reserveInstanceClass = ReservedInstace()
        self.runningInstanceClass = Instances()


    def readRunningCSV(self):
        # self.runningInstanceClass.getRunningInstanceSheet()
        self.running_file = "%s_running.csv"%self.current_month
        file = open(self.running_file,'rb')
        self.reader = csv.reader(file,delimiter=',')
        print "Hello"
        for row in self.reader:
            self.running_instance_counter(row[3])

        del self.running_instance_dict['Instance_Type']
        # print self.running_instance_dict

    def readReservationsCSV(self):
        self.reserveInstanceClass.getTotalReservation()
        self.riFile = "total_reservations.csv"
        file = open(self.riFile,'rb')
        self.reader = csv.reader(file,delimiter=',')
        for row in self.reader:
            self.ri_instance_counter(row[2],row[3])

        del self.ri_instance_dict['InstanceType']
        # return self.ri_instance_dict

    def expiringReservationsCSV(self):
        self.reserveInstanceClass.getExpiringReservation()
        self.expiringFile = "%s_expiring_reservations.csv"%self.current_month
        file = open(self.expiringFile,'rb')
        self.reader = csv.reader(file,delimiter=',')
        for row in self.reader:
            self.expring_ri_instance_counter(row[2],row[3])
        del self.expiring_ri_dict['InstanceType']
        # return self.expiring_ri_dict

    def getEnvironmentDictionary(self):
        file = open(self.running_file,'rb')

        self.reader = csv.reader(file,delimiter=',')
        for row in self.reader:
            if row[1] in self.environment_dict:
                pass
            else:
                self.environment_dict[row[1]] = 0

    def instanceEnvironmentMapper(self):
        file = open(self.running_file,'rb')
        self.reader = csv.reader(file,delimiter=',')
        for row in self.reader:
            if row[2] == "running":
                temp_dict = copy.deepcopy(self.environment_dict)
                if row[3] in self.instance_env_mapper_dict:
                    self.instance_env_mapper_dict[row[3]][row[1]] = self.instance_env_mapper_dict[row[3]][row[1]] + 1
                else:
                    self.instance_env_mapper_dict[row[3]] = temp_dict
                    self.instance_env_mapper_dict[row[3]][row[1]] = self.instance_env_mapper_dict[row[3]][row[1]] + 1

            else:
                continue




    def ri_instance_counter(self,instanceType,counter):
        if instanceType == "InstanceType":
            counter = 0
        if instanceType in self.ri_instance_dict:
            self.ri_instance_dict[instanceType] = int(self.ri_instance_dict[instanceType]) + int(counter)
        else:
            self.ri_instance_dict[instanceType] = int(counter)


    def running_instance_counter(self,instanceType):
        if instanceType in self.running_instance_dict:
            self.running_instance_dict[instanceType] = int(self.running_instance_dict[instanceType]) + 1
        else:
            self.running_instance_dict[instanceType] = 1

    def expring_ri_instance_counter(self,instanceType,counter):
        if instanceType == "InstanceType":
            counter = 0
        if instanceType in self.expiring_ri_dict:
            self.expiring_ri_dict[instanceType] = int(self.expiring_ri_dict[instanceType]) + int(counter)
        else:
            self.expiring_ri_dict[instanceType] = int(counter)

    def getCount(self,instanceType,dictionary):
        if instanceType in dictionary:
            return dictionary[instanceType]
        else:
            return 0

    def getCoverageHourPercentage(self,key):
        if key in self.reservation_coverage_dict:
            return self.reservation_coverage_dict[key]['CoverageHours']['CoverageHoursPercentage']
        else:
            return 'N.A'

    def getTotalrunningHours(self,key):
        if key in self.reservation_coverage_dict:
            return self.reservation_coverage_dict[key]['CoverageHours']['TotalRunningHours']
        else:
            return 'N.A'

    def getResrevedHours(self,key):
        if key in self.reservation_coverage_dict:
            return self.reservation_coverage_dict[key]['CoverageHours']['ReservedHours']
        else:
            return 'N.A'

    def getOnDemandHours(self,key):
        if key in self.reservation_coverage_dict:
            return self.reservation_coverage_dict[key]['CoverageHours']['OnDemandHours']
        else:
            return 'N.A'

    def getReservationCoverage(self):
        costExplorer =  CostExplorer()
        self.reservation_coverage_dict = costExplorer.getReservationCoverage()

    def getEnvRunningInstaceCount(self,instance,environment):
        if instance in self.instance_env_mapper_dict:
            return self.instance_env_mapper_dict[instance][environment]
        else:
            return 0



    def getCSV(self):
        print "Reading Running"
        self.readRunningCSV()
        print "Executing Environment Dictionary"
        self.getEnvironmentDictionary()
        print "Env Instance Mapper"
        self.instanceEnvironmentMapper()

        print "Read REservations "
        self.readReservationsCSV()

        print "Reade Expiring Reservations"
        self.expiringReservationsCSV()

        print "Reservation Coverage"
        self.getReservationCoverage()


        print "Creating Document"
        instance_set = set(self.running_instance_dict.keys()).union(set(self.ri_instance_dict.keys()))

        file_name = "%s_final_report.csv"%self.current_month
        file = open(file_name,'w+')
        csv_writer = csv.writer(file,delimiter=',')
        csv_writer.writerow(["Instance_Type","Running_Count","Prod","RC",'Dev',"blue5","sealab","factsheet","Total_Reserved","Reservations_Expiring","To_Be_Reserved","Coverage_Hours_Percentage","Total_Running_Hours_TillDate","Reserved_Hours","On_Demand_Hours"])

        for instance in instance_set:
            
            csv_writer.writerow([instance,self.getCount(instance,self.running_instance_dict),self.getEnvRunningInstaceCount(instance,'prodgamma4'),self.getEnvRunningInstaceCount(instance,'stagingdelta1'),self.getEnvRunningInstaceCount(instance,'devbeta1'),self.getEnvRunningInstaceCount(instance,'blue5'),self.getEnvRunningInstaceCount(instance,'sealab'),self.getEnvRunningInstaceCount(instance,'factset2'),self.getCount(instance,self.ri_instance_dict),self.getCount(instance,self.expiring_ri_dict),(self.getCount(instance,self.running_instance_dict)-self.getCount(instance,self.ri_instance_dict)+self.getCount(instance,self.expiring_ri_dict)),self.getCoverageHourPercentage(instance),self.getTotalrunningHours(instance),self.getResrevedHours(instance),self.getOnDemandHours(instance)])

        file.close()



c = ReadCSV()
c.getCSV()