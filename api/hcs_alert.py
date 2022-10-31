import warnings
import json
import requests
from conf import settings
from datetime import datetime
from email.encoders import encode_noop
import sys
from webbrowser import get
sys.path.append('..')
warnings.filterwarnings("ignore")

BASEURL = settings.HCS_BASEURL
USERNAME = settings.USERNAME
PASSWORD = settings.PASSWORD
BASEDIR = settings.BASEDIR
LOGFILE = settings.LOGFILE

TDTIME = str(settings.TDTIME)


def get_token() -> str:
    # 返回华为云 api user token，类型为str
    url = BASEURL + r"/rest/plat/smapp/v1/oauth/token"

    headers = {
        'Accept': 'application/json',
        'accept-charset': 'utf8',
        'Content-Type': 'application/json;charset=UTF-8'
    }

    data = {
        "grantType": "password",
        "userName": USERNAME,
        "value": PASSWORD,
    }

    data = json.dumps(data).encode("utf-8")

    response = requests.request(
        "PUT", url=url, headers=headers, data=data, verify=False)
    token = json.loads(response.text).get("accessSession")
    return token


def getlog() -> list:
    conf: dict
    with open(LOGFILE,'r',encoding='utf-8') as fr:
        conf = json.load(fr)

    if not TDTIME in conf:
        return 0
    csnslis = conf.get(TDTIME)
    return list(csnslis)


def savelog(csn: str):
    conf: dict
    with open(LOGFILE,'r',encoding='utf-8') as fr:
        conf = json.load(fr)

    if not TDTIME in conf:
        csnslis = [csn]
    else:
        csnslis = list(conf.get(TDTIME))
        csnslis.append(csn)
    dic = {TDTIME:csnslis}
    conf.update(dic)

    with open(LOGFILE, 'w', encoding="utf-8") as fw:
        json.dump(conf,fw)


def get_alert_csns(token) -> list:
    # 返回华为云所有告警流水号，类型为list
    url = BASEURL + "/rest/fault/v1/current-alarms/csns"
    payload = "{\r\n    \"query\":{}\r\n}"
    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
        'Accept-Charset': 'utf-8,q=1',
        'Content-Type': 'application/json;charset=UTF-8',
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False)
    res = json.loads(response.text).get("csns")
    res = list(res)
    return res


def get_alert_severity(token, csn) -> dict:
    # 根据告警流水号查询告警详细内容，返回类型为dict
    url = BASEURL + "/rest/fault/v1/current-alarms?csns=" + str(csn)
    payload = ""
    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
        'Accept-Charset': 'utf-8,q=1',
        'Content-Type': 'application/json,charset=UTF-8',
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, verify=False)
    res = json.loads(response.text)[0]
    # print(res)
    # print("-----------")
    alertinfo = dict()
    alertinfo = {'csn': '', 'severity': '', 'alarmName': '', 'mename': '', 'address': '', 'moi': '', 'latestOccurTime': '',
                 'logicalRegionName': '', 'eventType': '', 'clearTime': '', 'probableCause': '', 'additionalInformation': ''}
    # 流水号
    alertinfo["csn"] = res.get("csn")
    # 告警级别(1：紧急  2：重要  3：次要  4.提示)
    alertinfo["severity"] = res.get("severity")
    # 告警名称
    alertinfo["alarmName"] = res.get("alarmName")
    # 告警源
    alertinfo["mename"] = res.get("meName")
    # IP地址
    alertinfo["address"] = res.get("address")
    # 定位信息
    alertinfo["moi"] = res.get("moi")
    # 最近发生时间
    alertinfo["latestOccurTime"] = res.get("latestOccurTime")
    # 区域名称
    alertinfo["logicalRegionName"] = res.get("logicalRegionName")
    # 事件类型
    alertinfo["eventType"] = res.get("eventType")
    # 清除时间
    alertinfo["clearTime"] = res.get("clearTime")
    # 可能原因
    alertinfo["probableCause"] = res.get("probableCause")
    # 附加信息
    alertinfo["additionalInformation"] = res.get("additionalInformation")

    return alertinfo


if __name__ == '__main__':
    # token = get_token()
    # csn = get_alert_csns(token)[1]
    # get_alert_severity(token, csn)
    pass
