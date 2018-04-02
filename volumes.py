import boto3
import csv


class Volumes:
    def __init__(self):

        self.client = boto3.client('ec2')
        self.resource = boto3.resource('ec2')
        self.file = open("untagged_volumes.csv",'w+')
        self.writer = csv.writer(self.file,delimiter=',')
        self.instace_env_map_dict = dict()

    def getInstanceEnvMapper(self):
        read_file = open('March_running.csv','rb+')
        self.reader = csv.reader(read_file,delimiter=',')
        for row in self.reader:
            self.instace_env_map_dict[row[4]]=row[1]
        return self.instace_env_map_dict

    def describeVolumes(self):
        # self.writer.writerow(['Volume_Id','Instance_Id'])
        volumes = self.client.describe_volumes()
        for volume in volumes['Volumes']:
            env = None
            volume_id = volume['VolumeId']
            instance_id = None
            attachments = volume['Attachments']
            if volume['State'] == "in-use":
                for attachment in attachments:
                    instance_id = attachment['InstanceId']

            if 'Tags' in volume:
                tags = volume['Tags']
                for tag in tags:
                    if tag['Key'] == "environment" or tag['Key'] == "Environment":
                        env = tag['Value']


            if env:
                continue
            else:

                self.writer.writerow([volume_id, instance_id])

    def createTag(self,volume_id,env):
        if env != "UNTAGGED":
            try:

                volume = self.resource.Volume(volume_id)
                volume.create_tags(Tags=[{'Key':'environment','Value':env}])
                return "Tagging successfule"
            except Exception as e:
                return e.message
            # print volume_id,env




volume = Volumes()
volume.describeVolumes()
# instance_env_dict = volume.getInstanceEnvMapper()
# untaggedFile = open('untagged_volumes.csv','rb')
# file_reader = csv.reader(untaggedFile,delimiter=',')
# for row in file_reader:
#     if row[1] in instance_env_dict:
#         volume_id = row[0]
#         instance_env = instance_env_dict[row[1]]
#         print volume.createTag(volume_id,instance_env)
#
#     else:
#         continue

# volume.createTag("vol-0773dc5e757acaa78")