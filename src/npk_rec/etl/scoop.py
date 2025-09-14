import boto3
from .tokens import ACCESS_ID, ACCESS_KEY # Hidden

class Scoop:
    '''Retrieves a file from an S3 bucket.'''

    def __init__(self, bucket_name: str, object_key: str):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=ACCESS_ID,
            aws_secret_access_key=ACCESS_KEY
        )
        self.bucket_name = bucket_name
        self.object_key = object_key

    def scoop(self):
        print(f'{self.bucket_name=}')
        print(f'{self.object_key=}')
        '''Scoops the object out of the bucket and returns it'''
        response = self.s3.get_object(Bucket=self.bucket_name, Key=self.object_key)
        return response['Body'].read()
