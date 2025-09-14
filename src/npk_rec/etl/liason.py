from .pipeline import ETLPipeline
from .bucket_wrapper import BucketWrapper

class APILiason:
    '''
    Handles interfacing between AWS and npk_rec backend API
    '''
    def __init__(self, bucket, random=False):
        self.pipeline = ETLPipeline(random=random)
        self.bucket = bucket

    def get_data(self):
        return self.pipeline.load(self.bucket)