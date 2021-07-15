#!/usr/bin/python

import getopt
import sys

import texts
from credentials import run_credentials
from crypto import run_crypto
from exposed import run_exposed
from logs import run_logs


def main():
    argumentList = sys.argv[1:]
    if not argumentList:
        argumentList = ["-i", "-c", "-e", "-l"]
    options = "hciel"
    long_options = ["help", "credentials", "crypto", "exposed", "logs"]
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        print_logo()
        credentials = ask_credentials()

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                print("{}".format(texts.HELP))
                break
            if currentArgument in ("-i", "--credentials"):
                run_credentials(credentials)
            elif currentArgument in ("-c", "--crypto"):
                run_crypto(credentials)
            elif currentArgument in ("-e", "--exposed"):
                run_exposed(credentials)
            elif currentArgument in ("-l", "--logs"):
                run_logs(credentials)
    except getopt.error as err:
        print(str(err))


def ask_credentials():
    credentials = {}
    credentials["awsAccessKeyId"] = input("{}: ".format(texts.ENTER_ACCESS_KEY))
    credentials["awsSecretAccessKey"] = input("{}: ".format(texts.ENTER_SECRET_KEY))
    credentials["awsRegion"] = input("{}: ".format(texts.ENTER_REGION))
    return credentials


def print_logo():
    print(
        """\
    ..               .
    :-              -=
    -==.   .--.   .-=+                
    -=-=--==-=+=--====                
    .=+===---==++==+=.                
      -+==---====++-.                 
      :+=----====++-                  
      :++=-=-=+=+++-                  
      :+==-==+=-==+-                  
     -+++=======-+++-.                
   .=+++===+======+++=.               
  .=+++++========++++++.              
   .=++++++====++++++=:               
     .-=++++==++++=-.                 
         .:-==-:.    
Visius Heimdall - Watching the clouds
visius.io | v0.01
"""
    )


if __name__ == "__main__":
    main()
