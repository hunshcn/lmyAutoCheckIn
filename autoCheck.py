import datetime
import hashlib
import hmac
import json
import time

import requests

md5 = "9579D1CB25BADE7F8A3EB479DD0A2AC3"


# config.json读取
def read_config():
    """"读取配置"""
    with open("config.json", 'rb') as json_file:
        config = json.load(json_file)
    return config


#
def displayClazzInfo(ClazzList):
    print("所有课程信息")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for clazz in ClazzList:
        print(clazz)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# 登录蓝墨云
def login(name, pwd):
    try:
        loginUrl = "http://api.mosoteach.cn/mssvc/index.php/passport/login"
        headers = {
            "Accept-Encoding": "gzip;q=0.7,*;q=0.7", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; MI 9 Build/QKQ1.190933.005)", "Date": "", "X-mssvc-signature": "",
            "X-app-id": "MTANDROID", "X-app-version": "3.1.8", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        loginFormdata = {
            "account_name": "", "app_id": "MTANDROID", "app_version_name": "5.1.8",
            "app_version_number": "118", "device_code": device_code,
            "device_pn_code": device_code, "device_type": "ANDROID", "dpr": "2.75",
            "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmQVJFfoyV3ewxIjlCambLMFfJLlToOhoSV31qVieZYwz6kI3JywW2OEORSqZn9w1UkSkCMRjI5szT1fKe8XA93M8ZjKsnRrFt4U7VRyWpBYrVKiLuY7mukU7wumoEgi6ILTT1BECAbBQFF21vnpJnkfPwzKiAV825FnzRCINanQIDAQAB",
            "system_version": "10", "user_pwd": ""
        }
        loginFormdata["account_name"] = name
        loginFormdata["user_pwd"] = pwd
        headers["Date"] = getDate()
        headers["X-mssvc-signature"] = getLoginSignature(loginUrl, getDate(), loginFormdata)
        r = requests.post(loginUrl, headers=headers, data=loginFormdata)
        return r.json()
    except:
        print("login wrong!")
        return None


# 获得所有已经加入的班级信息
def getAllClazzInfo(userInfo):
    try:
        getAllClazzUrl = "https://api.mosoteach.cn/mssvc/index.php/clazzcourse/my_cc"
        headers = {
            "Accept-Encoding": "gzip;q=0.7,*;q=0.7", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; MI 9 Build/QKQ1.190933.005)",
            "Date": "", "X-device-code": device_code, "X-mssvc-signature": "",
            "X-mssvc-access-id": userInfo['access_id'], "X-app-id": "MTANDROID", "X-app-version": "5.1.8", "X-mssvc-sec-ts": userInfo['last_sec_update_ts_s'],
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        getAllClazzFormdata = {"dpr": "2"}
        headers["Date"] = getDate()
        headers["X-mssvc-signature"] = getSignature(getAllClazzUrl, userInfo['user_id'], getDate(), userInfo['access_secret'], getAllClazzFormdata)
        r = requests.post(getAllClazzUrl, headers=headers, data=getAllClazzFormdata);
        return r.json()
    except:
        print("getAllClazzInfo wrong!")
        return None


# 发送检测签到是否开启的请求
def checkIsOpen(userInfo, clazzId):
    try:
        checkOpenUrl = "https://api.mosoteach.cn/mssvc/index.php/checkin/current_open"
        headers = {
            "Accept-Encoding": "gzip;q=0.7,*;q=0.7", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; MI 9 Build/QKQ1.190933.005)",
            "Date": "", "X-device-code": device_code, "X-mssvc-signature": "",
            "X-mssvc-access-id": userInfo['access_id'], "X-app-id": "MTANDROID", "X-app-version": "5.1.8", "X-mssvc-sec-ts": userInfo['last_sec_update_ts_s'],
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        checkOpenFormdata = {"clazz_course_id": clazzId}
        headers["Date"] = getDate()
        headers["X-mssvc-signature"] = getSignature(checkOpenUrl, userInfo['user_id'], getDate(), userInfo['access_secret'], checkOpenFormdata)
        r = requests.post(checkOpenUrl, headers=headers, data=checkOpenFormdata)
        return r.json()
    except:
        print("checkIsOpen wrong!")
        return None


# 发送签到请求
def checkIn(userInfo, checkId, location):
    checkInUrl = "https://checkin.mosoteach.cn:19528/checkin"
    headers = {
        "Accept-Encoding": "gzip;q=0.7,*;q=0.7", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; MI 9 Build/QKQ1.190933.005)",
        "Date": "", "X-device-code": device_code, "X-mssvc-signature": "",
        "X-mssvc-access-id": userInfo['access_id'], "X-app-id": "MTANDROID", "X-app-version": "5.1.8", "X-mssvc-sec-ts": userInfo['last_sec_update_ts_s'],
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    checkOpenFormdata = {"checkin_id": checkId, "report_pos_flag": "Y", "lat": location['lat'], "lng": location['lng']}
    headers["Date"] = getDate()
    headers["X-mssvc-signature"] = getSignature(checkInUrl, userInfo['user_id'], getDate(), userInfo['access_secret'], None)
    r = requests.post(checkInUrl, headers=headers, data=checkOpenFormdata)
    return r.json()


# 获得格式化后的日期字符串
def getDate():
    times = datetime.datetime.utcnow()
    formatDate = times.strftime("%a, %d %b %Y-%m-%d %H:%M:%S GMT+00:00")
    return formatDate


def getMD5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()


def getMacSHA1(data1, data2):
    hmacSha1 = hmac.new(data1.encode('utf-8'), data2.encode('utf-8'), hashlib.sha1)
    return hmacSha1.hexdigest()


def getLoginSignature(url, gmtTime, formdata):
    global md5
    str1 = "%s|%s" % (url, gmtTime)
    for name in formdata:
        str1 = str1 + "|%s=%s" % (name, formdata[name])
    return getMacSHA1(md5, str1)


def getSignature(url, user_id, gmtTime, access_secret, formdata):
    if formdata == None or len(formdata) == 0:
        str1 = "%s|%s|%s" % (url, user_id, gmtTime)
        return getMacSHA1(access_secret, str1)
    else:
        str1 = ""
        for name in formdata:
            str1 = str1 + "%s=%s|" % (name, formdata[name])
        str1 = str1[0:len(str1) - 1]
        str1 = "%s|%s|%s|%s" % (url, user_id.upper(), gmtTime, getMD5(str1).upper())
        return getMacSHA1(access_secret, str1)


def send_message(message):
    if token:
        url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % token
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        requests.post(
            url,
            json.dumps({
                "msgtype": "text",
                "text": {
                    "content": f"\n{t}\n{message}"
                }
            }), headers={'Content-Type': 'application/json'})


# 开始签到程序
def startAtuoCheckIn(config):
    loginInfo = login(config['username'], config['password'])
    if not loginInfo:
        print("登陆失败")
    elif loginInfo['result_code'] == 1007:
        print("用户名或密码错误！")
    else:
        userInfo = loginInfo['user']
        print(userInfo['full_name'] + " 登陆成功!")
        clazzInfo = getAllClazzInfo(userInfo)['data']
        for i in clazzInfo:
            if i['status'] == 'OPEN':
                print({k: i[k] for k in i if k in ['id', 'course_name', 'create_time', 'creater_full_name']})
        clazzList = []
        for i in config['class']:
            clazz = list(filter(lambda x: x['id'] == i['id'], clazzInfo))
            if len(clazz) == 0:
                print('未找到课程id')
                return
            clazz = clazz[0]
            clazzList.append(
                {
                    'clazz_id': clazz['id'], 'clazz_name': clazz['course_name'], 'flag': 1, 'days': i['days'], 'start': i['start'], 'end': i['end'],
                    'location': (i['location'] if 'location' in i else location)
                })
        if not clazzList:
            print('没有签到任务')
            return
        print('签到任务：')
        displayClazzInfo(clazzList)
        while True:
            clazz = None
            a = datetime.datetime.now()
            for i in clazzList:
                if datetime.datetime.today().isoweekday() in i['days'] and i['start'] < [a.hour, a.minute] < i['end']:
                    clazz = i
            if clazz is None:
                for i in clazzList:
                    i['flag'] = 1
                time.sleep(sleep_time)
                continue
            if clazz['flag'] == 0:
                time.sleep(sleep_time)
                continue
            msg = checkIsOpen(userInfo, clazz['clazz_id'])
            print(msg)
            print('正在检测签到' + "." * 3, end='\r')
            if msg is not None and msg['result_msg'] == "OK" and clazz['flag'] == 1:
                print("正在签到 " + clazz['clazz_name'])
                checkInMsg = checkIn(userInfo, msg['id'], clazz['location'])
                if checkInMsg is not None and checkInMsg['result_code'] == 2409:
                    print(datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S") + " " + clazz['clazz_name'] + " 重复签到!")
                    send_message(clazz['clazz_name'] + "已经签到")
                    clazz['flag'] = 0
                elif checkInMsg is not None and checkInMsg['result_msg'] == 'OK':
                    clazz['flag'] = 0
                    send_message(clazz['clazz_name'] + "签到成功")
                    print(datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S") + " " + clazz['clazz_name'] + " 签到成功!")
            time.sleep(sleep_time)


config = read_config()
# 位置信息  可以自行添加经纬度信息   默认使用empty,教师端显示未获取位置
location = {"lat": config['lat'], "lng": config['lng']}
token = config['dingding'] if 'dingding' in config else ''
sleep_time = config['sleep_time'] if 'sleep_time' in config else 30
device_code = config['device_code']
startAtuoCheckIn(config)
