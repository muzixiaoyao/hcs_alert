import urllib.request
import json
import sys
import os
from conf import settings

CORPID = settings.CORPID
CORPSECRET = settings.CORPSECRET
BASEURL = settings.WECOM_BASEURL

def gettoken(corp_id,corp_secret):
    gettoken_url = BASEURL + '/gettoken?corpid=' + corp_id + '&corpsecret=' + corp_secret
    try:
        token_file = urllib.request.urlopen(gettoken_url)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))

    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token


def senddata(access_token,user,subject,content):
    try:
        send_url = BASEURL + '/message/send?access_token=' + access_token
        send_values = {
            "touser": user,    #企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
            "msgtype":"text", #消息类型。
            "agentid":"1000003",    #企业号中的应用id。
            "text":{
                "content": subject + '\n' + content
            },
            "safe":"0"
            }

        send_data = json.dumps(send_values,ensure_ascii=False).encode(encoding='UTF8')
        send_request = urllib.request.Request(send_url, send_data)
        response = urllib.request.urlopen(send_request)
        msg = response.read()
        print("returned value : " + str(msg))
    except:
        print("returned value : " + str(msg))


def send(user,subject,content):
    os.environ['http_proxy']="http://172.190.10.204:3127/"
    os.environ['https_proxy']="http://172.190.10.204:3127/"
    user = str(user)     #SENDTO zabbix传过来的第一个参数
    subject = str(subject)  #SUBJECT zabbix传过来的第二个参数
    content = str(content)  #MESSAGE zabbix传过来的第三个参数
    accesstoken = gettoken(CORPID,CORPSECRET)
    senddata(accesstoken,user,subject,content)


def run():

    user = str(sys.argv[1])     #SENDTO zabbix传过来的第一个参数
    subject = str(sys.argv[2])  #SUBJECT zabbix传过来的第二个参数
    content = str(sys.argv[3])  #MESSAGE zabbix传过来的第三个参数
 
    accesstoken = gettoken(CORPID,CORPSECRET)
    senddata(accesstoken,user,subject,content)


if __name__ == '__main__':
    # run()
    send("test1","1212")
