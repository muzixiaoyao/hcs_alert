import os
from datetime import datetime

TDTIME = datetime.now().strftime("%y%m%d")
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGDIR = os.path.join(BASEDIR,"log")
LOGFILE = os.path.join(LOGDIR,'hcs.log')

# 企业微信j配置：接口地址，CorpID是企业号的标识, corpsecretSecret是管理组凭证密钥，和微信告警接收者
WECOM_BASEURL = "https://qyapi.weixin.qq.com/cgi-bin"
CORPID = ''
CORPSECRET = ''
WECHAT_USERS = ['','']

# hcs 北向 API 基础地址和北向接口的用户名密码
HCS_BASEURL = "https://oc.xxx.xxx:26335"
USERNAME = ""
PASSWORD = ""

# hcs 告警级别
ALERT_LEVEL = {
    '1': '紧急',
    '2': '重要',
    '3': '次要',
    '4': '通知'
}

# hcs 告警类型
ALERT_TYPE = {
    "1": "通信告警",
    "2": "设备告警",
    "3": "处理错误告警",
    "4": "业务质量告警",
    "5": "环境告警",
    "6": "完整性告警",
    "7": "操作告警",
    "8": "物理资源告警",
    "9": "安全告警",
    "10": "时间域告警",
    "11": "属性值改变",
    "12": "对象创建",
    "13": "对象删除",
    "14": "关系改变",
    "15": "状态改变",
    "16": "路由改变",
    "17": "保护倒换",
    "18": "越限",
    "19": "文件传输状态",
    "20": "备份状态",
    "21": "心跳",
}
