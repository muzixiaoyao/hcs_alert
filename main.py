
from api import hcs_alert
from lib import wechat_alerts
from datetime import datetime
from conf import settings
import os

users= settings.WECHAT_USERS

alert_level = settings.ALERT_LEVEL
alert_type = settings.ALERT_TYPE


def datelog():
    date = datetime.date

def get_alert_list(token):
    # 返回级别为紧急和重要的告警流水号
    
    csnlis1 = hcs_alert.get_alert_csns(token)
    csnlis2 = list()
    for csn in csnlis1:

        severity = hcs_alert.get_alert_severity(token, csn).get("severity")
        if int(severity) <= 2:
            csnlis2.append(csn)
    return csnlis2


def format_alert(csn):
    token = hcs_alert.get_token()
    res = hcs_alert.get_alert_severity(token, csn)
    latestOccurTime = str(res.get("latestOccurTime"))[:-3]
    ltime = datetime.fromtimestamp(float(latestOccurTime))
    text = "告警流水号: " + str(res.get("csn")) + "\n"
    text += "告警名称: " + res.get("alarmName") + "\n"
    text += "告警级别: "+alert_level.get(str(res.get("severity"))) + "\n"
    text += "告警源: " + res.get("mename") + "\n"
    text += "IP地址: " + res.get("address") + "\n"
    text += "定位信息: " + res.get("moi") + "\n"
    text += "最近发生时间" + str(ltime) + "\n"
    text += "区域名称: " + res.get("logicalRegionName") + "\n"
    text += "事件类型: " + alert_type.get(str(res.get("eventType"))) + "\n"
    if str(res.get("clearTime")) != "0" and str(res.get("clearTime")) != None:
        text += "清除时间: " + str(res.get("clearTime")) + "\n"
    if res.get("probableCause") != "":
        text += "可能原因: " + res.get("probableCause") + "\n"
    if res.get("additionalInformation") != "":
        text += "附加信息: " + str(res.get("additionalInformation")) + "\n"

    return text

def sendusers(content):
    os.environ['http_proxy']="http://172.190.10.204:3127/"
    os.environ['https_proxy']="http://172.190.10.204:3127/"
    for user in users:
        wechat_alerts.send(user,"HCS Alert(sh-dev1) ",content)
    del os.environ['http_proxy']
    del os.environ['https_proxy']



def run():
    token = hcs_alert.get_token()
    alert_lis=get_alert_list(token)
    print(alert_lis)
    for csn in alert_lis:
        if not str(csn) in str(hcs_alert.getlog()):
            text = format_alert(csn)
            print(text)
            sendusers(text)
            hcs_alert.savelog(str(csn))


if __name__ == "__main__":
    run()
