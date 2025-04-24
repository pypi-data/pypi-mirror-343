import boto3
from dotenv import load_dotenv

load_dotenv()

ssm = boto3.client('ssm', region_name='us-east-1')

parameters = {
    'filepath': ['/home/ec2-user/log.txt'],
    'bucketname': ['srcsak-ssm-log-upload'],
    's3key': ['test.txt']
}

instance_ids = ['i-082f6f04ee1a2c19f'] 

response = ssm.send_command(
    InstanceIds=instance_ids,
    DocumentName='UploadToS3',
    Parameters=parameters
)

print("Command ID:", response['Command']['CommandId'])

