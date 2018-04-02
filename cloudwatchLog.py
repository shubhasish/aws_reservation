import boto3


class CloudwatchLogs:

    def __init__(self):
        self.client = boto3.client('logs')

    def listLogGroup(self):
        logGroups = self.client.describe_log_groups()
        return logGroups

    def listTags(self,logGroupName):
        return self.client.list_tags_log_group(logGroupName=logGroupName)

    def createTag(self,logGroupName,environment):
        return self.client.tag_log_group(logGroupName=logGroupName,tags={'environment':environment})


cl = CloudwatchLogs()
response = cl.listLogGroup()
# print len(response['logGroups'])

for group in response["logGroups"]:
    logGroupName = group['logGroupName']
    print cl.listTags(logGroupName)['tags']
    # if len(cl.listTags(logGroupName)['tags']) == 0:
    #     env = logGroupName.split('/')[3]
    #     if "dev3" in env:
    #         cl.createTag(logGroupName,'devbeta1')
    #     elif "rc" in env:
    #         cl.createTag(logGroupName,'stagingdelta1')
    #     elif "research" in env:
    #         cl.createTag(logGroupName,'prodgamma4')
    #     else:
    #         cl.createTag(logGroupName,env)

#
# client = boto3.client('logs')
# print client.list_tags_log_group()