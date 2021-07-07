import concurrent.futures
from core import get_client
import texts
from spinner import *

def run_crypto(credentials):
    print('\n===== {} ====='.format(texts.CHECKING_CRYPTO))
    with Spinner(''):
        try:
            data = get_crypto_status(credentials)
        except Exception as e: 
            print('')
            print(e)
            exit()
    s3 = data['s3']
    cloudtrail = data['cloudtrail']
    rds = data['rds_instances']

    print('\n == {} =='.format(texts.CRYPTO_CLOUDTRAIL))
    if cloudtrail:
        for trail in cloudtrail:
            print('  {0}: {1}'.format(trail, texts.NOT_ENCRYPTED))

    print('\n == {} =='.format(texts.CRYPTO_S3))
    if s3[0]:
        for item in s3[0]:
            print('  {0}: {1}'.format(item, texts.ENCRYPTED))
    if s3[1]:
        for item in s3[1]:
            print('  {0}: {1}'.format(item, texts.NOT_ENCRYPTED))

    print('\n == {} =='.format(texts.CRYPTO_RDS))
    if rds[0]:
        for item in rds[0]:
            print('  {0}: {1}'.format(item, texts.ENCRYPTED))
    if rds[1]:
        for item in rds[1]:
            print('  {0}: {1}'.format(item, texts.NOT_ENCRYPTED))

def get_trails(credentials):
    cli = get_client('cloudtrail',credentials)
    return cli.describe_trails()['trailList']

def cloudtrail_encrypted(credentials):
    '''Ensure CloudTrail logs are encrypted at rest using KMS CMKs'''
    trails = get_trails(credentials)
    trails = list(map(lambda x:{'TrailARN':x['TrailARN'],'KmsKeyId':x.get('KmsKeyId')},trails))

    trailsWithNoEncryption = list(filter(lambda x: x['KmsKeyId']==None,trails))
    trailsWithNoEncryption = [i['TrailARN'] for i in trailsWithNoEncryption]
    return trailsWithNoEncryption

def s3_default_encryption_enabled(credentials):
    buckets = get_client('s3',credentials).list_buckets()
    bucketNames = list(map(lambda x: x['Name'], buckets['Buckets']))
    encryptedBuckets = []
    unencryptedBuckets = []
    for name in bucketNames:
        try:
            encryption = get_client('s3',credentials).get_bucket_encryption(Bucket=name)['ServerSideEncryptionConfiguration']
            for cipher in encryption['Rules']:
                if cipher['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']:
                    encryptedBuckets.append(name)
        except:
            unencryptedBuckets.append(name)
    return encryptedBuckets, unencryptedBuckets 
    
def rds_encrypted(credentials):
    cli = get_client('rds', credentials)
    rdsInstances = cli.describe_db_instances()['DBInstances']
    encryptedInstances = list(filter(lambda x: x['StorageEncrypted']==True,rdsInstances))
    encryptedInstances = [i['DBInstanceIdentifier'] for i in encryptedInstances]
    noCryptoInstances = list(filter(lambda x: x['StorageEncrypted']==False,rdsInstances))
    noCryptoInstances = [i['DBInstanceIdentifier'] for i in noCryptoInstances]
    return encryptedInstances, noCryptoInstances


def get_crypto_status(credentials):

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        s3CryptoFuture = executor.submit(s3_default_encryption_enabled, credentials)
        ctCryptoFuture = executor.submit(cloudtrail_encrypted, credentials)
        rdsCryptoFuture = executor.submit(rds_encrypted, credentials)
    status = {
        's3':s3CryptoFuture.result(),
        'rds_instances': rdsCryptoFuture.result(),
        'cloudtrail':ctCryptoFuture.result(),
    }
    return status
