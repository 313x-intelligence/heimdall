from itertools import repeat

import texts
from core import get_client
from spinner import *


def run_logs(credentials):

    print("\n===== {} =====".format(texts.LOGS))
    try:
        with Spinner(""):
            logs = vpcFlowLogEnabled(credentials)
        if logs[0]:
            for log in logs[0]:
                print("{}: {}".format(log, texts.LOGGING))
        if logs[1]:
            for log in logs[1]:
                print("{}: {}".format(log, texts.NOT_LOGGING))
    except Exception as e:
        print(e)
        exit()


def getFlowLogs(vpcId, credentials):
    flowLogs = get_client("ec2", credentials).describe_flow_logs(
        Filters=[{"Name": "resource-id", "Values": [vpcId]}]
    )["FlowLogs"]
    if flowLogs:
        flowLogs = list(
            map(
                lambda x: {
                    "FlowLogStatus": x["FlowLogStatus"],
                    "VpcId": x["ResourceId"],
                },
                flowLogs,
            )
        )
        return flowLogs
    else:
        return {"FlowLogStatus": None, "VpcId": vpcId}


def vpcFlowLogEnabled(credentials):
    cli = get_client("ec2", credentials)
    vpcs = cli.describe_vpcs()["Vpcs"]
    vpcsIds = [i["VpcId"] for i in vpcs]
    flowLogs = list(map(getFlowLogs, vpcsIds, repeat(credentials)))
    logging, notLogging = [], []
    for id in flowLogs:
        if id["FlowLogStatus"] == None:
            notLogging.append(id["VpcId"])
        else:
            logging.append(id["VpcId"])

    return logging, notLogging
