import requests
import win32api
import win32con
import re

wlanuserip_ = ""
wlanacip_ = "172.21.255.250"
user_id = ""
password = ""

def print_error(text = "Unhandled Exception"):
    print("*"*25)
    print(text)
    print("*"*25)
    return

def init_config():
    ip_pattern = r"^(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)$"
    user_id_pattern = r"^20\d{10}$"
    try:
        reg = win32api.RegCreateKeyEx(win32con.HKEY_CURRENT_USER,"SOFTWARE\\LogDormWiFi",win32con.WRITE_OWNER |win32con.KEY_WOW64_64KEY|win32con.KEY_WRITE)
        print("请输入申请校园网时的IP地址(xx.xx.xx.xx):",end='')
        wlanuserip = str(input())
        while(not(re.match(ip_pattern,wlanuserip))):
            print("请输入申请校园网时[被分配到]的IP地址(xx.xx.xx.xx)[0-255]:",end='')
            wlanuserip = str(input())
        reg = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,"SOFTWARE\\LogDormWiFi",0,win32con.KEY_WRITE)
        win32api.RegSetValueEx(reg,"wlanuserip",0, win32con.REG_SZ,wlanuserip)
        print("请输入你的学号(20xxxxxxxxxx):",end='')
        userid = str(input())
        while(not(re.match(user_id_pattern,userid))):
            print("请输入你的[12位]学号(20xxxxxxxxxx):",end='')
            userid = str(input())
        win32api.RegSetValueEx(reg,"user_id",0, win32con.REG_SZ,userid)
        print("请输入你的密码(默认为身份证后8位):",end='')
        password_ = str(input())
        win32api.RegSetValueEx(reg,"password",0, win32con.REG_SZ,password_)
        win32api.RegCloseKey(reg)
        global wlanuserip_,wlanacip_,user_id,password
        wlanuserip_ = tuple(wlanuserip)
        user_id = tuple(userid)
        password = tuple(password_)
    except Exception as E:
        print(E)
        if "Access is Denied" in str(E):
            print("初始化失败！\n")
        #win32api.RegSetValueEx (reg,"wlanuserip_", "", win32con.REG_SZ, keyValue)
    return

def init_read_config():
    try:
        reg = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,"SOFTWARE\\LogDormWiFi",0,win32con.KEY_READ)
        global wlanuserip_,wlanacip_,user_id,password
        wlanuserip_ = win32api.RegQueryValueEx(reg,"wlanuserip")
        user_id = win32api.RegQueryValueEx(reg,"user_id")
        password = win32api.RegQueryValueEx(reg,"password")
        win32api.RegCloseKey(reg)
    except Exception as Err:
        sErr = str(Err)
        if "The system cannot find the file specified." in sErr:
            print("似乎这是妮第一次使用\n我们需要先做一些配置:\n")
            init_config()
    return

init_read_config()
wlanacname_ = "WX6108E-slot7-AC"
vlan_id_ = "scut-student"
url = "https://s.scut.edu.cn:801/eportal/?c=ACSetting&a=Login&wlanuserip=" + wlanuserip_[0] + "&wlanacip=" + wlanacip_ + "&wlanacname=" + wlanacname_ + "&redirect=&session=&vlanid=" + vlan_id_ + "&port=&iTermType=1&protocol=https:"
data = {'DDDDD':user_id[0],'upass':password[0],'R1':'0','R2':'','R6':'0','para':'00','0MKKey':'123456'}
try:
    r = requests.post(url,data,timeout = 5).text
    if("成功" in r):
        print("-"*25 + "\n登录成功!\n" + "-"*25)
    elif ("已使用" in r):
        print("-"*35 + "\n已经成功连接WiFi!无需再次登录!\n" + "-"*35)
    else:
        print("-"*25 + "\n登录失败!\n" + "-"*25)
        print(r)
except requests.exceptions.HTTPError as e:
    print_error("建立连接失败!")
    exit(-1)
except requests.exceptions.ConnectTimeout as e:
    print_error("连接验证服务器超时!")
    exit(-1)
except requests.exceptions.RequestException as e:
    print_error(str(e))
    exit(-1)