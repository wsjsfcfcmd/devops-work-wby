### Devops作业
- [1-环境部署](#1-环境部署)
- [2-ddns](#2-ddns)
- [3-版本更新](#3-版本更新)

####1-环境部署(CloudFormation + Manual)

系统架构图
![image](https://github.com/wsjsfcfcmd/devops-work-wby/blob/master/image/architecture.png?raw=true)

####2-ddns
利用阿里云sdk，每次判断前，先删除@记录，再次添加所有需要更新的@的A记录
[python ddns代码](https://github.com/wsjsfcfcmd/devops-work-wby/blob/master/ddns.py) 
```
# Main logic
def lambda_handler(event, context):
    RR = "@"
    Type = "A"
    domain = os.environ["domain"]
    albdomain = os.environ["alb"]
    
    dns_del(domain, RR)
    loadblancer = albdomain
    values = GetIpFromDomain(loadblancer)
    for value in values:
        dns_add(domain, RR, Type, value)
```
###3-版本更新

通过ansible远程控制来更新系统

#### 更新版本1
```
ansible-playbook distribute.yml --extra-vars="ver=ver1"
```
![image](https://github.com/wsjsfcfcmd/devops-work-wby/blob/master/image/web_ver1.png?raw=true)


#### 更新版本3
```
ansible-playbook distribute.yml --extra-vars="ver=ver3"
```
![image](https://github.com/wsjsfcfcmd/devops-work-wby/blob/master/image/web_ver3.png?raw=true)

