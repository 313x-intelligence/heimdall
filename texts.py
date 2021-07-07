import gettext

t = gettext.translation('texts_i18n', 'locale', fallback=True)
_ = t.gettext

TRUE=_('\033[92mTrue\033[0m')
FALSE=_('\033[91mFalse\033[0m')
ENABLED=_('\033[92mEnabled\033[0m')
DISABLED=_('\033[91mDisabled\033[0m')
ENCRYPTED=_('\033[92mEncrypted\033[0m')
NOT_ENCRYPTED=_('\033[91mNot Encrypted\033[0m')
EXPOSED=_('\033[91mExposed\033[0m')
NOT_EXPOSED=_('\033[92mNot Exposed\033[0m')
NOT_LOGGING=_('\033[91mNot Logging\033[0m')
LOGGING=_('\033[92mLogging\033[0m')

ENTER_ACCESS_KEY=_('Enter Your AWS Access Key ID')
ENTER_SECRET_KEY=_('Enter Your AWS Secret Access Key')
ENTER_REGION=_('Enter you AWS Region')

HELP=_('''Visius Cloud 0.01 (visius.io)
USAGE:
  RUN: python main.py (options)
  Enter credentials
OPTIONS:
  -h: Show this helper
  -i: Check credentials.
  -c: Check crypto.
  -e: Check exposed.
  -l: Check Logs.
OPTIONS (long)
  --help: Same as -h 
  --credentials: Same as -i
  --crypto: Same as -c
  --exposed: Same as -e
  --logs: Same as -l
''')

CHECKING_CRYPTO=_('Checking Crypto')
CRYPTO_CLOUDTRAIL=_('Cloudtrail')
CRYPTO_S3=_('S3 Buckets')
CRYPTO_RDS=_('RDS Instances')

CHECKING_EXPOSED=_('Exposed Items')
EXPOSED_S3=_('S3 Buckets')
EXPOSED_RDS=_('RDS')
EXPOSED_RDS_SNAPSHOTS=_('RDS Snapshots')
EXPOSED_EBS=_('EBS')
EXPOSED_KMS=_('Exposed KMS')
EXPOSED_CLOUD_TRAIL_LOGS=_('Cloud Trail Logs')

CHECKING_CREDENTIALS=_('Checking Credentials')
CREDENTIALS_MFA=_('MFA')
PASSWORD_POLICY=_('Password Policy')
PASSWORD_LENGTH=_('Minimum Length')
PASSWORD_SYMBOL=_('Requires a symbol')
PASSWORD_LOWER_CASE=_('Requires a lower case letter')
PASSWORD_UPPER_CASE=_('Requires a upper case letter')
PASSWORD_NUMBER=_('Requires a number')

LOGS=_('Logs')
