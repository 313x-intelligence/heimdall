import concurrent.futures
from core import get_client
import texts
from spinner import *

def run_credentials(credentials):
    print('===== {} ====='.format(texts.CHECKING_CREDENTIALS))
    try:
        password_policy(credentials)
        mfa(credentials)
    except Exception as e: 
        print(e)
        exit()

#### Password Policy ####

def password_policy(credentials):
    with Spinner(''):
        data = get_password_policy(credentials)
    password_length = data.get('MinimumPasswordLength')
    password_symbol = texts.TRUE if data['RequireSymbols'] else texts.FALSE
    password_lower_case = texts.TRUE if data['RequireUppercaseCharacters'] else texts.FALSE
    password_upper_case = texts.TRUE if data['RequireLowercaseCharacters'] else texts.FALSE
    password_number = texts.TRUE if data['RequireNumbers'] else texts.FALSE

    response = '''\
 == {0} ==
  {1}: {2}
  {3}: {4}
  {5}: {6}
  {7}: {8}
  {9}: {10}
'''
    return print(response.format(texts.PASSWORD_POLICY,
                            texts.PASSWORD_LENGTH,
                            password_length,
                            texts.PASSWORD_SYMBOL,
                            password_symbol,
                            texts.PASSWORD_LOWER_CASE,
                            password_lower_case,
                            texts.PASSWORD_UPPER_CASE,
                            password_upper_case,
                            texts.PASSWORD_NUMBER,
                            password_number
                            ))

def get_password_policy(credentials):

    cli = get_client('iam',credentials)
    return cli.get_account_password_policy()['PasswordPolicy']


#### MFA ####

def mfa(credentials):
    print(" == {} ==".format(texts.CREDENTIALS_MFA))
    with Spinner(''):
        root = root_multifactor_enabled(credentials)
        usersWithMfa, WildUsers = multifactor_check(credentials)
    
    root_mfa = texts.ENABLED if root else texts.DISABLED

    print('  Root: %s'%root_mfa)

    if usersWithMfa:
        for user in usersWithMfa:
            print('  {}: {}'.format(user, texts.ENABLED))
    if WildUsers:
        for user in WildUsers:
            print('  {}: {}'.format(user, texts.DISABLED))

def root_multifactor_enabled(credentials):
    cli = get_client('iam',credentials)
    if cli.get_account_summary()['SummaryMap']['AccountMFAEnabled']==1:
        return True
    else:
        return False

def get_login_profile(users, cli):
    usersWithConsolePasswd = []
    for user in users:
        try:
            consoleUser = cli.get_login_profile(UserName=user['UserName'])
            usersWithConsolePasswd.append(consoleUser)
        except:
            pass
    return usersWithConsolePasswd

def multifactor_check(credentials):
    cli = get_client('iam', credentials)
    users = cli.list_users()['Users']
    usersConsole =  get_login_profile(users, cli)
    mfaDevices = cli.list_virtual_mfa_devices()['VirtualMFADevices']
    usersWithMfa = []
    wildUsers = []
    if mfaDevices:
        try:
            data = list(map(lambda x: x['User']['UserName'],mfaDevices))
            usersWithMfa.append(data)
        except KeyError:
            pass
    usersWithoutMfa = list(filter(lambda x: x not in usersWithMfa, usersConsole))
    wildUsers = [i['LoginProfile']['UserName'] for i in usersWithoutMfa]
    return usersWithMfa, wildUsers

def get_mfa_status(credentials):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rootMFAFuture = executor.submit(root_multifactor_enabled, credentials)
        mfaFuture = executor.submit(multifactor_check, credentials)
        status ={
            "root":rootMFAFuture.result(),
             "other_users":mfaFuture.result(),
        }
        return status
