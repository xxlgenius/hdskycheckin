## HDSky自动签到脚本

这是一个可以自动登录HDSky并签到的python脚本

## 配置文件编写

在运行docker容器前需要先创建配置文件并保存

**config.json**

```json
{
    "usr":"登录用户名",
    "pwd":"登录密码",
    "time":"定时执行时间，如：01:00",
    "webaddr":"selenium运行地址和端口 http://127.0.0.1:4444",
    "browser":"firefox,chrome,edge",
    "headless":false，是否无头模式启动
}
```

**smtp.json**

发生错误时的邮件通知服务

多个目的邮箱是string用逗号分割;mail_coding接收的类别为，明文传输（default，25端口）,SSL加密（SSL，465端口），SSL加密（SSL），STARTTLS加密（TLS，587端口）

```json
{
    "mail_host":"smtp.office365.com",
    "mail_coding":"TLS",
    "mail_port":587,
    "mail_user":"youmail@mail.com",发送邮件
    "mail_pwd":"youpasswd",
    "mail_header":"签到脚本通知",邮件标题
    "send_name":"签到脚本",邮件用户名显示名称
    "receivers":"notification@mail.com",接受邮件
}
```



## Docker部署

`selenium`docker配置方法请参考[docker-selenium](https://github.com/SeleniumHQ/docker-selenium)

**容器启动**

```bash
docker run -v /yourdatafile:/app/data handsomegenius/hdskycheckin
```

## 鸣谢

[NexusPHP_checkin](https://github.com/TeraDew/NexusPHP_Checkin)
