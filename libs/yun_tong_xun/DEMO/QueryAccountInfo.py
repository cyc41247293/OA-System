#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '您的主帐号';

#主帐号Token
accountToken= '您的主帐号Token';

#应用Id
appId='您的应用ID';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

 # 主帐号信息查询
def queryAccountInfo():
    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.queryAccountInfo()

    for k,v in result.iteritems(): 
        
        if k=='Account' :

                for k,s in v.iteritems(): 

                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
   
   
#queryAccountInfo()