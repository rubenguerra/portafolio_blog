from .base import *

DEBUG = False

ADMINS = (
    ('Ruben', 'lcdorubenguerra@gmail.com'),
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {

    }
}

AWS_ACCESS_KEY_ID = 'AKIAZVIRZUBHHSK6S753'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'blogbackend'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'sa-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
