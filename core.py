import boto3

def get_session(credentials):
    awsAccessKeyId, awsSecretAccessKey = credentials.get('awsAccessKeyId'), credentials.get('awsSecretAccessKey')
    return boto3.Session(
    aws_access_key_id=awsAccessKeyId,
    aws_secret_access_key=awsSecretAccessKey)

def get_client (resource, credentials):
    return get_session(credentials).client(resource, region_name=credentials.get('awsRegion'))

def get_account_id(credentials):
    cli = get_client('sts', credentials)
    return cli.get_caller_identity().get('Account')

def get_rds_snapshots(credentials):
    cli = get_client('rds',credentials)
    return cli.describe_db_snapshots(IncludeShared=False)


def get_rds_instances(credentials):
    cli = get_client('rds',credentials)
    return cli.describe_db_instances()


def get_rds_cluster_snapshots(credentials):
    cli = get_client('rds',credentials)
    return cli.describe_db_cluster_snapshots(IncludeShared=True)


def get_s3_acl(bucketName, credentials):
    cli = get_client('s3',credentials)
    return cli.get_bucket_acl(Bucket=bucketName)


def get_trails(credentials):
    cli = get_client('cloudtrail',credentials)
    return  cli.list_trails()['Trails']


def get_trails_ARNs(credentials):
    trails = get_trails(credentials)
    arns = []
    for trail in trails:
        arns.append(trail['TrailARN'])
    return arns


def get_ec2_snapshot_attribute(snapshot, attribute, credentials):
    cli = get_client('ec2',credentials)
    snapshotId = snapshot['SnapshotId']
    return cli.describe_snapshot_attribute(Attribute=attribute, SnapshotId=snapshotId)


def get_ebs_snapshots(credentials):
    cli = get_client('ec2',credentials)
    accountId = get_account_id(credentials)
    filters = [{'Name':'owner-id', 'Values':[accountId]}]
    return cli.describe_snapshots(Filters=filters)['Snapshots']


def permissive_policy(statement):
    return (statement['Effect'] == 'Allow' and
            statement['Principal'] == '*' or
            statement['Principal'].get('AWS') == '*' or
            statement['Principal'].get('CanonicalUser')=='*')


def get_kms_keys(credentials):
    cli = get_client('kms',credentials)
    return cli.list_keys()


def get_s3_buckets(credentials):
    cli = get_client('s3',credentials)
    return cli.list_buckets()
