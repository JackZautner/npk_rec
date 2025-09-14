import random
import pandas as pd

from io import BytesIO

from .scoop import Scoop

class ETLPipeline:
    '''Handles ETL pipeline from AWS'''
    def __init__(self, random=False):
        self.random = random # Random data generation

    def extract(self, bucket):
        if self.random:
            raise ValueError("Cannot extract data for random mode.")
        
        bucket_name = bucket.bucket_name
        object_key = bucket.object_key

        scoop = Scoop(bucket_name, object_key)
        raw_file_content = scoop.scoop()

        return raw_file_content

    def transform(self, bucket):
        # Intermediary transformation step if needed

        # Return in form of dataframe
        raw_content = self.extract(bucket)
        df = pd.read_csv(BytesIO(raw_content))
        return df

    def load(self, bucket):
        # If random, generate a random NPK ratio.
        if self.random:
            return '-'.join([str(random.randint(0, 10)) for _ in range(3)])
        else:
            return self.transform(bucket)