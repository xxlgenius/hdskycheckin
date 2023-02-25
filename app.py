# coding=utf-8
import os
#import re
#import pickle
import requests
#from requests import cookies
#import requests.utils
import captchaparse as cp
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logging.handlers import RotatingFileHandler
import argparse
import schedule
import mysmtp
#from time import sleep
import json

# imgpath = 'check_code.jpg'



def setLogger():
    FILE_SIZE = 10*1024*1024
    FILE_COUNT = 1
    logger = logging.getLogger("checkin")
    logger.setLevel(logging.INFO)
    #log_file = "{}.log".format(__file__)
    #os.makedirs("./data/checkin.log",exist_ok=True)
    logHandler = RotatingFileHandler("./data/checkin.log", maxBytes=FILE_SIZE, backupCount=FILE_COUNT, encoding='UTF-8')
    logHandler.setLevel(logging.INFO)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    consoleHandler.setFormatter(formatter)
    logHandler.setFormatter(formatter)
    # add
    logger.addHandler(logHandler)
    logger.addHandler(consoleHandler)
    return logger

def getCheckCode(imageHash, image_get_url):
    imgpath = imageHash + '.jpg'
    abs_imgpath = os.path.join(os.path.abspath('.'), imgpath)
    logger.info('abs_imgpath = '+abs_imgpath)
    im = requests.get(image_get_url)  # 获取验证码和cookies值
    with open(abs_imgpath, 'wb') as f:
        f.write(im.content)
    # img = Image.open('check_code.jpg')
    # img.show()
    '''
	codeBegin(imgpath)
	check_code = input("code:")
	'''
    check_code = cp.binary_captchar(abs_imgpath)

    os.remove(abs_imgpath)
    # logger.info("captcha: " + check_code)
    return check_code


'''
def login():
    files = os.listdir('.')
    cookie_name = 'open_cookies.txt'
    cookie_file_name = os.path.join(os.path.abspath('.'), cookie_name)
    logger.info(cookie_file_name)
    logger.info(files)
    if cookie_name in files:
        logger.info("startgetcookies")
        with open(cookie_file_name, 'rb') as f:
            cookies = 'c_secure_uid=OTc5MTU%3D; c_secure_pass=bc42097e5d35d2e87a097ea8ee73890b; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=eWVhaA%3D%3D; c_secure_login=bm9wZQ%3D%3D; UM_distinctid=17cd580f1cac7f-07e079df8ccf22-6373267-1fa400-17cd580f1cbc73; CNZZDATA5476511=cnzz_eid%3D1323648825-1635668847-https%253A%252F%252Fhdsky.me%252F%26ntime%3D1642041735; __cf_bm=jmmWOhHjXxOUMlZBnimsyppdd1aXE4VFtRh5yt3riIw-1642043850-0-ATxCJpV2g7floe/YYiB0qngMgdTcY4LV7DVYH0xUIwX742meTewF2X1pe9Hn8I7ZNAXjbLc+29w7q6T9pTO6GDZftyDYj8b8yjgQkTdFOWPZPrNMIRiONNTn1NXmWa9s5g=='
            # cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            bt_session = requests.session()
            bt_session.cookies = cookies
            logger.info("finishgetcookies")
        try:
            torrent_url = 'https://hdsky.me/torrents.php'
            test = bt_session.get(torrent_url)
            if test.status_code != 200 or test.url != torrent_url:
                print(
                    'Something wrong when login in. Delete the cookies and relogin plese.\n')
                return
        except:
            print("net error")
            return
    else:
        print("startlogininweb")
        username = input("Genius")
        password = input("Rm8YARZm")
        login_php = 'https://hdsky.me/login.php'
        try:
            bt_session = requests.Session()
            req = bt_session.get(login_php)
        except:
            print("net error")
            return
        # print(req.text)
        # <input name="imagehash" value="2cb98173c9a2fc28f0976f9a5b715db5">
        imageHash = re.findall(
            'name="imagehash" value="(.*?)" />', req.text)[0]
        print(imageHash)
        # image_get_url = 'https://**此处打码，使用前请自行替换为域名并检查url**/image.php?action=regimage&imagehash=' + imageHash
        check_code = getCheckCode(imageHash)
        login_post_url = 'https://hdsky.me/takelogin.php'
        login_datas = {
            'username': username,
            'password': password,
            'imagestring': check_code,
            'imagehash': imageHash
        }
        try:
            main_page = bt_session.post(login_post_url, login_datas)
            # print(main_page.text)
            if main_page.url != "https://hdsky.me/index.php":
                print("login error")
                return
            with open(cookie_file_name, 'wb') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(
                    bt_session.cookies), f)
            print('成功登陆')
        except:
            print("net error")
    return bt_session
'''

'''
def checkin(session,imageHash):
    print(getCheckCode(imageHash))
    check_code = getCheckCode(imageHash)

    checkin_datas = {
        'imagehash': imageHash,
        'imagestring': check_code
    }
    try:
        checkin_page = session.post(checkin_post_url, checkin_datas)
        print(checkin_page.json())

        if(checkin_page.json()['state'] == 'false' and checkin_page.json().has_key('msg')):
            checkin(session)
        elif(checkin_page.json()['state'] == 'success'):
            nowtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            str = nowtime + '\t签到成功\t连续签到：' + \
                checkin_page.json()['signindays'] + '天,\t获得魔力值：' + \
                checkin_page.json()['integral']
            print(str)
            logging.info(str)
        elif(checkin_page.json()['state'] == 'false' and not checkin_page.json().has_key('msg')):
            print('已经签到')

    except:
        print("net error")
'''

def job(userName:str,userPwd:str,headless:bool,web:str,webaddr:str):
    logger.info(time.ctime()+"/开始执行")
    loginurl = 'https://hdsky.me/login.php'
    indexurl = "https://hdsky.me/index.php"
    driver = None
    webOptions = None
    if web == "chrome":
        logger.info(time.ctime()+"/开始注册chrome"+"   /浏览器地址:"+webaddr )
        webOptions = webdriver.ChromeOptions()
        if(headless):
            logger.info(time.ctime()+"/无头模式启动")
            webOptions.add_argument('--headless')
            webOptions.add_argument("--disable-gpu")
        #driver = webdriver.Chrome(options=webOptions)
    elif web == "edge":
        logger.info(time.ctime()+"/开始注册edge"+"   /浏览器地址:"+webaddr )
        webOptions = webdriver.EdgeOptions()
        if(headless):
            logger.info(time.ctime()+"/无头模式启动")
            webOptions.add_argument('--headless')
            webOptions.add_argument("--disable-gpu")
        #driver = webdriver.ChromiumEdge(options=webOptions)
    elif web == "firefox":
        logger.info(time.ctime()+"/开始注册firefox"+"   /浏览器地址:"+webaddr)
        webOptions = webdriver.FirefoxOptions()
        if(headless):
            logger.info(time.ctime()+"/无头模式启动")
            webOptions.add_argument('--headless')
            webOptions.add_argument("--disable-gpu")
        #driver = webdriver.Firefox(options=webOptions)
        #driver = webdriver.Firefox(options=webOptions)       
    logger.info(time.ctime()+"/开始连接远程浏览器")
    driver = webdriver.Remote(command_executor=webaddr,options=webOptions)
    #driver = webdriver.Chrome()
    logger.info(time.ctime()+"/浏览器注册完成")


    driver.delete_all_cookies()
    # 打开网页
    driver.get(loginurl)
    logger.info(time.ctime()+"/打开目标网页")
    time.sleep(5)
    # cookies注入
    with open('./data/cookies.json',"r",encoding="utf-8") as f1:
        cookie = json.loads(f1.read())
        print( cookie)
        for c in cookie:
            driver.add_cookie(c)
    # 刷新页面
    driver.get(indexurl)
    '''
    logimgurl = driver.find_element(By.XPATH,'//*[@id="nav_block"]/form[2]/table/tbody/tr[4]/td[2]/img').get_attribute('src')
    imageHash = str(logimgurl).split('=')[-1]
    log_code = getCheckCode(imageHash, logimgurl)
    logger.info(time.ctime()+"/验证码解析完毕：" + log_code)
    driver.find_element(By.XPATH,'//*[@id="nav_block"]/form[2]/table/tbody/tr[1]/td[2]/input').send_keys(userName)
    driver.find_element(By.XPATH,'//*[@id="nav_block"]/form[2]/table/tbody/tr[2]/td[2]/input').send_keys(userPwd)
    driver.find_element(By.XPATH,'//*[@id="nav_block"]/form[2]/table/tbody/tr[5]/td[2]/input[1]').send_keys(log_code)
    driver.find_element(By.XPATH,'//*[@id="nav_block"]/form[2]/table/tbody/tr[10]/td/input[1]').click()
    logger.info(time.ctime()+"/完成登录")

    try:
        driver.find_element(By.XPATH,'//*[@id="showup"]').click()
    except:
        logger.warning(time.ctime()+'/未找到目标元素，已签到')
    '''  
    # 定位并获取验证码src
    try:
        # 查找并点击签到按钮
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="showup"]')))
        driver.find_element(By.XPATH, '//*[@id="showup"]').click()
        logger.info(time.ctime()+"点击签到按钮")
        imgurl = driver.find_element(By.XPATH,'//*[@id="showupimg"]').get_attribute('src')
    except:
        logger.error(time.ctime()+"/未找到目标签到图片元素")
        sendError(time.ctime()+"/未找到目标签到图片元素")
    else:
        # 获取imgurl按‘=’分割的倒数第一个字符串
        imageHash = str(imgurl).split('=')[-1]
        check_code = getCheckCode(imageHash, imgurl)
        logger.info(time.ctime()+"/签到验证码解析完毕："+check_code)
        #logger.info(check_code)
    try:
        driver.find_element(By.XPATH,'//*[@id="imagestring"]').send_keys(check_code)
        driver.find_element(By.XPATH,'//*[@id="showupbutton"]').click()
        #logger.info(time.ctime() +"/debug:输入验证码完毕并点击了提交")
    except:
        logger.error(time.ctime() +"/r签到失败，没找到提交面板")
        sendError(time.ctime() + "/r签到失败，没找到提交面板")
    else:
        logger.info(time.ctime()+"/签到成功")

    driver.quit()

#多个目的邮箱是string用逗号分割;mail_coding接收的类别为，明文传输（default，25端口）,SSL加密（SSL，465端口），SSL加密（SSL），STARTTLS加密（TLS，587端口）
def sendError(sendcontent:str):
    smtpjson = "./data/smtp.json"
    try:
        with open(smtpjson,'r',encoding='utf-8') as file:
            mymail = json.load(file)
            logger.info(time.ctime()+"/获取邮件配置文件成功")
        maildriver = mysmtp.Smtpmailserver(mymail)
    except:
        logger.warning(time.ctime()+"/未设定邮箱或邮箱格式出错")
        return
    maildriver.Sendmail(sendcontent)
    logger.info("通知邮件发送成功")
    
def do_schedule():
    logger.info("正在运行计划任务, 每天签到一次")

    while True:
        logger.info("距离下一次任务的时间: {:.1f}分钟".format(schedule.idle_seconds()))
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(30)


if __name__ == '__main__':
    global mymail   
    global logger
    logger = setLogger()
    logger.info("脚本已启动")
    #action_group = parser.add_mutually_exclusive_group()
    
    
    #时间计划
    #schedule.every(1).minutes.do(job)
    configpath = "./data/config.json"
    try:
        with open(configpath,'r',encoding='utf-8') as file:
            myconfig = json.load(file)
            logger.info(time.ctime()+"/获取配置文件成功")
    except:
        logger.error(time.ctime()+"/获取配置文件失败，ERROR")
        
    job(myconfig["usr"],myconfig["pwd"],myconfig["headless"],myconfig["browser"],myconfig["webaddr"])
    logger.info("签到时间:" + myconfig["time"])
    schedule.every().day.at(myconfig["time"]).do(job,myconfig["usr"],myconfig["pwd"],myconfig["headless"],myconfig["browser"],myconfig["webaddr"])
    do_schedule()
    


