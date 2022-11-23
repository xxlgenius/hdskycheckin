import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
#from lib.singleton import *

#@singleton
class Smtpmailserver:

    #def __new__(cls, *args, **kwargs):
    #    return object.__new__(cls)

    def __init__(self,smtpdata:dict) -> None:#传入json数据/字典
        self.__smtp_all_data = smtpdata
        #self.smtpjson = "./smtp.json"
        #try:
        #    with open(self.smtpjson,'r',encoding='utf-8') as jsonfile:
        #        self.smtp_all_data = json.load(jsonfile)
        #except FileNotFoundError:
        #    self.log.error("邮件服务初始化：打开smtpjson文件失败")
        #    exit()

    def _format_addr(self,s):
        name,addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def Sendmail(self,sendtext:str):
        from_addr_pwd = self.__smtp_all_data["mail_pwd"]
        from_addr = self.__smtp_all_data["mail_user"]
        to_addr = self.__smtp_all_data["receivers"]
        msg = MIMEText(sendtext, 'plain', 'utf-8')
        msg['From'] = self._format_addr(self.__smtp_all_data["send_name"]+"<%s>"%from_addr)
        msg['To'] = self._format_addr('admin<%s>'%to_addr)
        msg['Subject'] = Header(self.__smtp_all_data["mail_header"],'utf-8').encode()
        encode = self.__smtp_all_data["mail_coding"]
        
        if encode == "SSL":
            server = smtplib.SMTP_SSL(self.__smtp_all_data["mail_host"],self.__smtp_all_data["mail_port"])
        elif encode == "default":
            server = smtplib.SMTP(self.__smtp_all_data["mail_host"],self.__smtp_all_data["mail_port"])        
        elif  encode == "TLS":
            server = smtplib.SMTP(self.__smtp_all_data["mail_host"],self.__smtp_all_data["mail_port"])
            server.starttls()
        else:
            exit()
        #server.set_debuglevel(1)
        server.login(from_addr,from_addr_pwd)
        server.sendmail(from_addr,[to_addr],msg.as_string())
        server.quit()
