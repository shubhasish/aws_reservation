import boto3
import csv



class s3:
    def __init__(self):
        self.client = boto3.client('s3')

    def listBuckets(self):
        return self.client.list_buckets()

    def getTags(self,bucket):
        try:
            return self.client.get_bucket_tagging(Bucket=bucket)
        except Exception as e:
            return e.message

    def createTag(self,bucketName,environment):
        return self.client.put_bucket_tagging(Bucket=bucketName,Tagging={'TagSet':[{'Key':'environment','Value':environment}]})


s = s3()

buckets = s.listBuckets()['Buckets']
s3_file = open('s3_tag.csv','w+')
writer = csv.writer(s3_file,delimiter=',')
writer.writerow(['Name','Environment'])
# print len(buckets)
for bucket in buckets:
    name = bucket['Name']
    response = s.getTags(bucket['Name'])
    if "NoSuchTagSet" in response:
        writer.writerow([name,'N.A'])
        # if 'blue' in name:
        #     s.createTag(name,"blue5")
    elif "Access Denied" in response:
        writer.writerow([name,'Access Denied'])
    else:
        print response
        tags = response['TagSet']
        env = 'N.A'
        for tag in tags:
            if tag['Key'] == "environment" or tag['Key'] == 'Environment':
                env = tag['Value']
        writer.writerow([name,env])
#     print name,s.getTags(bucket['Name'])

# open_file = open('s3_tag.csv')
# csv_reader = csv.reader(open_file,delimiter=',')
#
#
# for row in csv_reader:
#     if "ios" in row[0] and row[1] == 'N.A':
#         print row[0]
#         s.createTag(row[0],'ios')
