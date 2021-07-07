import concurrent.futures
import core
import texts
import json
from spinner import *

def run_exposed(credentials):
    print('\n===== {} ====='.format(texts.CHECKING_EXPOSED))
    with Spinner(''):
        try:
            data = get_exposed_status(credentials)
        except Exception as e: 
            print('')
            print(e)
            exit()
    if data['s3'] != ([],[]):
        print(' == {} =='.format(texts.EXPOSED_S3))
        if data['s3'][0]:
            for i in data['s3'][0]:
                print('  {}: {}'.format(i, texts.NOT_EXPOSED))
        if data['s3'][1]:
            for i in data['s3'][1]:
                print('  {}: {}'.format(i, texts.EXPOSED))

    if data['rds_instances'] != ([],[]):
        print('\n == {} =='.format(texts.EXPOSED_RDS))
        if data['rds_instances'][0]:
            for i in data['rds_instances'][0]:
                print('  {}: {}'.format(i, texts.NOT_EXPOSED))
        if data['rds_instances'][1]:
            for i in data['rds_instances'][1]:
                print('  {}: {}'.format(i, texts.EXPOSED))

    if data['rds_snapshots'] != ([],[]):
        print('\n == {} =='.format(texts.EXPOSED_RDS_SNAPSHOTS))
        if data['rds_snapshots'][0]:
            for i in data['rds_snapshots'][0]:
                print('  {}: {}'.format(i, texts.NOT_EXPOSED))
        if data['rds_snapshots'][1]:
            for i in data['rds_snapshots'][1]:
                print('  {}: {}'.format(i, texts.EXPOSED))

    if data['ebs'] != ([],[]):
        print('\n == {} =='.format(texts.EXPOSED_EBS))
        if data['ebs'][0]:
            for i in data['ebs'][0]:
                print('  {}: {}'.format(i, texts.NOT_EXPOSED))
        if data['ebs'][1]:
            for i in data['ebs'][1]:
                print('  {}: {}'.format(i, texts.EXPOSED))

    if data['kms'] != ([], []):
        print('\n == {} =='.format(texts.EXPOSED_KMS))
        if data['kms'][0]:
            for i in data['kms'][0]:
                print('  {}: {}'.format(i, texts.NOT_EXPOSED))
        if data['kms'][1]:
            for i in data['kms'][1]:
                print('  {}: {}'.format(i, texts.EXPOSED))

    if data['cloud_trail_logs'] != ([], []):
        print('\n == {} ==').format(texts.EXPOSED_CLOUD_TRAIL_LOGS)
        if data['cloud_trail_logs'][0]:
            for i in data['cloud_trail_logs'][0]:
                print('  {}: {}'.format(i, texts.NOT_EXPOSED))
        if data['cloud_trail_logs'][1]:
            for i in data['cloud_trail_logs'][1]:
                print('  {}: {}'.format(i, texts.EXPOSED))
    
def bucket_is_public(ACL):
    for grant in ACL['Grants']:
        uri = grant['Grantee'].get('URI',False)
        if uri and 'global/AllUsers' in uri:
            return True
        else:
            return False

def cloud_trail_logs_not_public(credentials):
    ''' Ensure the S3 bucket CloudTrail
    logs to is not publicly accessible'''

    cloudTrailClient = core.get_client('cloudtrail', credentials)
    trailBuckets =  cloudTrailClient.describe_trails(trailNameList=core.get_trails_ARNs(credentials))['trailList']
    notExposed = []
    exposed = []
    if trailBuckets:
        for trail in trailBuckets:
            try:
                bucketName = trail['S3BucketName']
                bucketACL = core.get_s3_acl(bucketName, credentials)
                if  bucket_is_public(bucketACL):
                    notExposed.append(bucketName)
                else:
                    exposed.append(bucketName)
            except:
                pass
    return notExposed, exposed

def ebs_not_public(credentials):
    ebsSnapshots =  core.get_ebs_snapshots(credentials)
    snapshotStatus = []
    exposed = []
    notExposed = []
    for snapshot in  ebsSnapshots:
        if snapshot is not None:
            snapshotAttribute =  core.get_ec2_snapshot_attribute(snapshot, 'createVolumePermission', credentials )
            for group in snapshotAttribute['CreateVolumePermissions']:
                if  group['Group'] == 'all':
                    notExposed.append(snapshot['SnapshotId'])
                else:
                    exposed.append(snapshot['SnapshotId'])
            return notExposed, exposed
    return EBS_SNAPSHOT_NOT_FOUND

def rds_snapshot_is_public(snapshot, credentials):
    cli = core.get_client('rds',credentials)
    snapshotIdentifier = snapshot['DBSnapshotIdentifier']
    snapshotAttributes = cli.describe_db_snapshot_attributes(DBSnapshotIdentifier=snapshotIdentifier)
    for attribute in snapshotAttributes['DBSnapshotAttributesResult']['DBSnapshotAttributes']:
        if 'all' in attribute['AttributeValues'] and attribute['AttributeName'] == 'restore':
            return True
        else:
            return False

def rds_snapshot_not_public(credentials):
    '''Check if RDS Snapshots are public'''
    snapshots = core.get_rds_snapshots(credentials)['DBSnapshots']
    exposed = []
    notExposed = []
    if snapshots:
        for snapshot in snapshots:
            if rds_snapshot_is_public(snapshot, credentials):
                notExposed.append(snapshot['DBSnapshotArn'])
            else:
                exposed.append(snapshot['DBSnapshotArn'])
    return notExposed, exposed

def rds_instance_not_public(credentials):
    instanceStatus = []
    instances = core.get_rds_instances(credentials)['DBInstances']
    exposed = list(filter(lambda x: x['PubliclyAccessible']==True,instances))
    exposed = [i['DBInstanceIdentifier'] for i in exposed]
    notExposed = list(filter(lambda x: x['PubliclyAccessible']==False,instances))
    notExposed = [i['DBInstanceIdentifier'] for i in notExposed]

    return notExposed, exposed

def rds_cluster_snapshot_is_public(snapshot,credentials):
    cli = core.get_client('rds',credentials)
    snapshotIdentifier = snapshot['DBClusterSnapshotIdentifier']
    snapshotAttributes = cli.describe_db_cluster_snapshot_attributes(
        DBClusterSnapshotIdentifier=snapshotIdentifier)
    for attribute in snapshotAttributes['DBClusterSnapshotAttributesResult']['DBClusterSnapshotAttributes']:
        if 'all' in attribute['AttributeValues'] and attribute['AttributeName'] == 'restore':
            return True
        else:
            return False

def rds_cluster_not_public(credentials):
    ''' Check if RDS cluster Snapshots are public '''
    clusterSnapshots = core.get_rds_cluster_snapshots(credentials)['DBClusterSnapshots']
    exposed = []
    notExposed = []
    if clusterSnapshots:
        for snapshot in clusterSnapshots:
            if rds_cluster_snapshot_is_public(snapshot,credentials):
                notExposed.append(snapshot['DBClusterSnapshotsIdentifier'])
            else:
                exposed.append(snapshot['DBClusterSnapshotsIdentifier'])
    return notExposed, exposed

def exposed_kms_keys(credentials):
    '''Check exposed KMS keys'''
    keys = core.get_kms_keys(credentials)['Keys']
    exposed = []
    notExposed = []
    if keys:
        keyIds = list(map(lambda x: x['KeyId'], keys))
        policies = list(map(lambda x: core.get_client('kms',credentials)
        .get_key_policy(KeyId=x, PolicyName='default'), keyIds))
        for policy in policies:
            policy = json.loads(policy['Policy'])
            permissivePolicies = list(filter(core.permissive_policy, policy['Statement']))
            notPermissivePolicies = list(filter(lambda x: not core.permissive_policy(x), policy['Statement']))
            permissiveSid =  list(map(lambda x: x['Sid'], permissivePolicies))
            notPermissiveSid =  list(map(lambda x: x['Sid'], notPermissivePolicies))
            if permissivePolicies:
                exposed.append(permissiveSid)
            else:
                notExposed.append(notPermissiveSid)
        return notExposed, exposed
    else:
        return KMS_KEYS_NOT_FOUND

def s3Public(credentials):
    buckets = core.get_s3_buckets(credentials)
    bucketsNames = list(map(lambda x: x['Name'], buckets['Buckets']))
    bucketStatus = []
    notExposed = []
    exposed = []
    s3Cli = core.get_client('s3',credentials)
    for name in bucketsNames:
        try:
            policy = s3Cli.get_bucket_policy_status(Bucket=name)
            if policy['PolicyStatus']['IsPublic']:
                exposed.appent(name)
            else:
                notExposed.append(name)

        except s3Cli.exceptions.from_code('NoSuchBucketPolicy'):
            try:
                response = s3Cli.get_public_access_block(Bucket=name)
                if response['PublicAccessBlockConfiguration']['BlockPublicAcls'] and response['PublicAccessBlockConfiguration']['BlockPublicPolicy']:
                    notExposed.append(name)
                else:
                    exposed.appent(name)

            except s3Cli.exceptions.from_code('NoSuchPublicAccessBlockConfiguration'):
                response = s3Cli.get_bucket_acl(Bucket=name)
                for grant in response['Grants']:
                    if grant['Grantee']['Type'] == 'Group' and 'AllUsers' in grant['Grantee']['URI']:
                        exposed.appent(name)
                    else:
                        notExposed.append(name)

        except:
            response = s3Cli.get_public_access_block(Bucket=name)['PublicAccessBlockConfiguration']
            if response['BlockPublicAcls'] and response['BlockPublicPolicy']:
                exposed.appent(name)
            else:
                notExposed.append(name)

        return notExposed, exposed
    return S3_BUCKETS_NOT_FOUND

def get_exposed_status(credentials):
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        s3Future = executor.submit(s3Public,credentials)
        rdsFuture = executor.submit(rds_instance_not_public, credentials)
        ebsFuture = executor.submit(ebs_not_public, credentials)
        kmsFuture = executor.submit(exposed_kms_keys, credentials)
        ctFuture = executor.submit(cloud_trail_logs_not_public, credentials)
        rdsClusterFuture = executor.submit(rds_cluster_not_public, credentials)
        rdsSnapshotFuture = executor.submit(rds_snapshot_not_public, credentials)
    status = {
        "s3":s3Future.result(),
        "rds_instances":rdsFuture.result(),
        "ebs":ebsFuture.result(),
        "kms":kmsFuture.result(),
        "rds_cluster":rdsClusterFuture.result(),
        "cloud_trail_logs":ctFuture.result(),
        "rds_snapshots":rdsSnapshotFuture.result()
    }
    return status

