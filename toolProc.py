from tkinter import *
from tkinter import messagebox
from threading import Timer
import threading
import os
import time
import getConfig
import toolAPI
import time
from threading import Lock
import openssh
import requests.exceptions as exceptions
import json
import requests
import traceback
import system
import base64
import matplotlib.pyplot as plt
import socket
import event
import math
from PIL import Image
import cv2
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.pyplot import MultipleLocator,plot,savefig
import alertAPI
'''
    1、创建一个state machine，有如下几种状态： idle，transfer，upgrade
    2、对于单台设备，上传fgapp采用串行的方式，一是考虑带宽的影响，二是避免上传出错
'''
lock = Lock()
fgappPath = './fgapp'
deviceIp = ''

#
bWorking = False  # 表示应用是否正在升级
imageNumber=0
bTransfer = False
bUpgrade = False
bReboot = False
fgTransferNub=0
appTransferNub=0
tempPercent=0
fgUpgradeNub=0
appUpgradeNub=0
progressJson={'data':{'Progress':0}}
tempProgress=0

# FGUpgrade process
bFGUpgradeProc = False
fgUpgradeState = 'idle'

# FGApp process
bFGAppProc = False
fgAppState = 'idle'



FGUpgradeTransFlag = False

configInfo = None
upgradeNum = 0  # 升级的fgapp的数量
upgradeList = []  # 升级的fgapp的列表




def thread_it(func, args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()



def sshDef(devip,text_cb,system,status):
    text_cb(devip+' ssh端口操作请求中......\n', 'detail')
    if not(re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", devip)):
        text_cb('请输入正确格式的IP !\n', 'fail')
    if not(system=="Delinux" or system=="Fglinux"):
        text_cb('请选择系统类型 !\n', 'fail')
    if not(status=="临时打开，重启后恢复" or status=="永久打开" or status=="临时关闭，重启后恢复" or status=="永久关闭"):
        text_cb('请选择操作类型 !\n', 'fail')
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", devip) and (system=="Delinux" or system=="Fglinux") and (status=="临时打开，重启后恢复" or status=="永久打开" or status=="临时关闭，重启后恢复" or status=="永久关闭"):
        #text_cb(devip, 'fail')
        #text_cb(system, 'fail')
        #text_cb(status, 'fail')
        try:
            flag=True
            result=openssh.main(devip,system,status)
            if json.loads(result)['code']==200:
                text_cb('\n'+result+'\n', 'pass')
            else:
                text_cb('\n'+result+'\n', 'fail')
        except exceptions.ConnectionError as e:
            flag=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag==False:
            text_cb(devip+' '+ErroResult+'   \n', 'fail')
def apiDef(devip,text_cb,url,method,body,token):
    print(body)
    text_cb(devip+' api调试请求中......\n', 'detail')
    if url=='':
        text_cb('请选择或输入URL !\n', 'fail')
        
    if (not(url=='')):
        try:
            flag=True
            if token=='token/l4t':
                rLogin=requests.post(url='http://'+devip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
                #print(rLogin.text)
                if method=='post':
                    result=requests.post(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
                elif method=='get':
                    result=requests.get(url='http://'+devip+url,
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
                elif method=='put':
                    result=requests.put(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
                elif method=='delete':
                    result=requests.delete(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            elif token=='token/l4ab':
                rLogin=requests.post(url='http://'+devip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
                #print(rLogin.text)
                if method=='post':
                    result=requests.post(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
                elif method=='get':
                    result=requests.get(url='http://'+devip+url,
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
                elif method=='put':
                    result=requests.put(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
                elif method=='delete':
                    result=requests.delete(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            elif token=='no':
                if method=='post':
                    result=requests.post(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8'})
                elif method=='get':
                    result=requests.get(url='http://'+devip+url,
                                         headers={'Content-Type':'application/json;charset=utf-8'})
                elif method=='put':
                    result=requests.put(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8'})
                elif method=='delete':
                    result=requests.delete(url='http://'+devip+url, json=json.loads(body),
                                         headers={'Content-Type':'application/json;charset=utf-8'})
            #print(result.text)
            
            if result.json()['code']==200 or result.json()['code']==200000 or result.json()['code']==0:
                result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                text_cb('\n'+result+'  \n', 'pass')
            else:
                #print(result.text)
                result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                text_cb('\n'+result+'  \n', 'fail')
        except exceptions.ConnectionError as e:
            flag=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag==False:
            text_cb(devip+' '+ErroResult+'   \n', 'fail')

def sysDef(devip,text_cb,user,Lname,storage):
    global imageNumber
    imageNumber=imageNumber+1
    text_cb(devip+' 系统监控请求中......\n', 'detail')
    code = os.popen('ping '+devip).read()
    if not ('TTL' in code):
        text_cb(devip+' 设备连接失败，请检查环境！\n', 'fail')
        return None
    else:
        if not(re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", devip)):
            text_cb('请输入正确格式的IP !\n', 'fail')
        if user=="" :
            text_cb('用户名/密码不能为空 !\n', 'fail')
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", devip) and not(user=="") :
            #text_cb(devip, 'fail')
            #text_cb(system, 'fail')
            #text_cb(status, 'fail')
            try:
                flag=True
                #system.login_run(devip,text_cb,user,Lname,storage,imageNumber)
                system.thread_it(system.login_run,[devip,text_cb,user,Lname,storage,imageNumber])
            except exceptions.ConnectionError as e:
                flag=False
                ErroResult='连接错误：'+str(e.args[0].reason)
            except exceptions.Timeout as e:
                flag=False
                ErroResult='请求超时：'+str(e.message)
            except exceptions.HTTPError as e:
                flag=False
                ErroResult='http请求错误:'+str(e.message)
            except Exception as e:
                flag=False
                ErroResult='请求错误:'+traceback.format_exc()
            if flag==False:
                text_cb(devip+' '+ErroResult+'   \n', 'fail')
            return None
def sysStopDef(devip,text_cb):
    global imageNumber
    #text_cb(devip+' 监控关闭中......\n', 'detail')
    system.thread_it(system.login_stop,[imageNumber])
    #system.login_stop(imageNumber)
    text_cb(devip+' 监控关闭已触发，请稍等片刻。\n', 'detail')
def toBase64Def(path,text_cb):
    text_cb('图像转base64中......\n', 'detail')
    try:
        with open(path, 'rb') as f:
            imageEncode= base64.b64encode(f.read())
            imageEncode_str= imageEncode.decode()
            #text_cb(imageEncode_str+'\n', 'detail')
            file=path.split('/')[-1].split('.')[0]
            codePath='./base64/'+file+'.txt'
            with open(codePath, 'wb') as ff:
                ff.write(imageEncode)
                text_cb('图像转base64完成，base64编码保存路径为：'+codePath+'。   \n', 'pass')
                ff.close()            
            f.close()
    except Exception as e:
        text_cb('运行错误:'+traceback.format_exc()+'   \n', 'fail')
def base64toDef(path,text_cb):
    text_cb('base64转图像中......\n', 'detail')
    try:
        with open(path, 'rb') as f:
            imageEncode= f.read()
            imageEncode_str=base64.b64decode(imageEncode)
            #imageEncode_str= str(imageEncode, encoding="utf-8")
        file=path.split('/')[-1].split('.')[0]
        imagePath='./base64/'+file+'.jpg'
        #if  not os.path.exists(imagePath):
        #   os.makedirs(imagePath)
        with open(imagePath,mode='wb') as f:
            f.write(imageEncode_str)
            f.close()
        text_cb('base64转图像完成，图片保存路径为：'+imagePath+'。  \n', 'pass')
    except Exception as e:
        text_cb('运行错误:'+traceback.format_exc()+'   \n', 'fail')
def dataOpenApi(devip,text_cb):
    text_cb(devip+' 打开event接口......\n', 'detail')

    try:
        flag=True
        hostname = socket.gethostname()
        addrs = socket.getaddrinfo(socket.gethostname(),None)
        for item in addrs:
            if (':' not in item[4][0]) and (item[4][0].split('.')[0]==devip.split('.')[0]) and (item[4][0].split('.')[1]==devip.split('.')[1]) :
                ipaddr=item[4][0]
        if ':' in devip:
            rLogin=requests.post(url='http://'+devip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            result=requests.put(url='http://'+devip+'/api/system/config/eventserver', json={"enabled":True,"server":"http://"+ipaddr+":8888","user":"haomuL","passwd":"abc@Dgsh"},
                                headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        else :
            rLogin=requests.post(url='http://'+devip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result=requests.put(url='http://'+devip+'/api/system/config/eventserver', json={"enabled":True,"server":"http://"+ipaddr+":8888","user":"haomuL","passwd":"abc@Dgsh"},
                                headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        if result.json()['code']==200000:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'pass')
        else:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'fail')
    except exceptions.ConnectionError as e:
        flag=False
        ErroResult='连接错误：'+str(e.args[0].reason)
    except exceptions.Timeout as e:
        flag=False
        ErroResult='请求超时：'+str(e.message)
    except exceptions.HTTPError as e:
        flag=False
        ErroResult='http请求错误:'+str(e.message)
    except Exception as e:
        flag=False
        ErroResult='请求错误:'+traceback.format_exc()
    if flag==False:
        text_cb(devip+' '+ErroResult+'   \n', 'fail')
def dataCloseApi(devip,text_cb):
    text_cb(devip+' 关闭event接口......\n', 'detail')

    try:
        flag=True
        hostname = socket.gethostname()
        addrs = socket.getaddrinfo(socket.gethostname(),None)
        for item in addrs:
            if (':' not in item[4][0]) and (item[4][0].split('.')[0]==devip.split('.')[0]) and (item[4][0].split('.')[1]==devip.split('.')[1]) :
                ipaddr=item[4][0]
        if ':' in devip:
            rLogin=requests.post(url='http://'+devip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            result=requests.put(url='http://'+devip+'/api/system/config/eventserver', json={"enabled":False,"server":"http://"+ipaddr+":8888","user":"haomuL","passwd":"abc@Dgsh"},
                                headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        else :
            rLogin=requests.post(url='http://'+devip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result=requests.put(url='http://'+devip+'/api/system/config/eventserver', json={"enabled":False,"server":"http://"+ipaddr+":8888","user":"haomuL","passwd":"abc@Dgsh"},
                                headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        if result.json()['code']==200000:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'pass')
        else:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'fail')
    except exceptions.ConnectionError as e:
        flag=False
        ErroResult='连接错误：'+str(e.args[0].reason)
    except exceptions.Timeout as e:
        flag=False
        ErroResult='请求超时：'+str(e.message)
    except exceptions.HTTPError as e:
        flag=False
        ErroResult='http请求错误:'+str(e.message)
    except Exception as e:
        flag=False
        ErroResult='请求错误:'+traceback.format_exc()
    if flag==False:
        text_cb(devip+' '+ErroResult+'   \n', 'fail')
def dataCapture(devip,faceFlag,pedestrianFlag,vehicleFlag,bicycleFlag,path,num,text_cb):
    text_cb(devip+' 采集参数送达中......\n', 'detail')
    hostname = socket.gethostname()
    addrs = socket.getaddrinfo(socket.gethostname(),None)
    flag0=1
    for item in addrs:
        if (':' not in item[4][0]) and (item[4][0].split('.')[0]==devip.split('.')[0]) and (item[4][0].split('.')[1]==devip.split('.')[1]) :
            ipaddr=item[4][0]
    try:
        result=requests.post(url='http://'+ipaddr+':8888/api/aa', json={'eventType':3333})
        result=requests.post(url='http://'+ipaddr+':8888/api/aa', json={'eventType':1111,'faceFlag': faceFlag, 'pedestrianFlag':pedestrianFlag,'vehicleFlag':vehicleFlag, 'bicycleFlag':bicycleFlag,'path': path, 'flag':1})
        if result.json()['code']==200000:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'pass')
        else:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'fail')
    except exceptions.ConnectionError as e:
        flag0=False
        ErroResult='连接错误：'+str(e.args[0].reason)
    except exceptions.Timeout as e:
        flag0=False
        ErroResult='请求超时：'+str(e.message)
    except exceptions.HTTPError as e:
        flag0=False
        ErroResult='http请求错误:'+str(e.message)
    except Exception as e:
        flag0=False
        ErroResult='请求错误:'+traceback.format_exc()
    if flag0==False:
        text_cb(devip+' '+ErroResult+'   \n', 'fail')
    text_cb(devip+' 数据收集中......\n', 'detail')
    startTime = datetime.now()
    drun=0
    #text_cb(devip+' 数据收集中1......\n', 'detail')
    while drun<(float(num)*60):
        endTime = datetime.now()
        drun = (endTime-startTime).seconds
        flag2=True
        try:
            result=requests.post(url='http://'+ipaddr+':8888/api/aa', json={'eventType':2222})
            resultJson=result.json()
            if resultJson['code']==200000:
                result=json.dumps(resultJson, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                results='face:'+str(resultJson['faceNum'])+'   pedestrian:'+str(resultJson['pedestrianNum'])+'   vehicle:'+str(resultJson['vehicleNum'])+'   bicycle:'+str(resultJson['bicycleNum'])
                text_cb(' '+results+'     \n', 'detail')
            else:
                result=json.dumps(result, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                text_cb(' '+result+'    \n', 'fail')
        except exceptions.ConnectionError as e:
            flag2=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag2=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag2=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag2=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag2==False:
            text_cb(devip+' '+ErroResult+'   \n', 'fail')
        #text_cb(devip+' 数据收集中2......\n', 'detail')
        time.sleep(30)
    #text_cb(devip+' 数据收集中3......\n', 'detail')
    flag3=True
    try:
        result=requests.post(url='http://'+ipaddr+':8888/api/aa', json={'eventType':1111,'faceFlag': faceFlag, 'pedestrianFlag':pedestrianFlag,'vehicleFlag':vehicleFlag, 'bicycleFlag':bicycleFlag,'path': path, 'flag':0})
        if result.json()['code']==200000:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'pass')
        else:
            result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            text_cb('\n'+result+'\n', 'fail')
    except exceptions.ConnectionError as e:
        flag3=False
        ErroResult='连接错误：'+str(e.args[0].reason)
    except exceptions.Timeout as e:
        flag3=False
        ErroResult='请求超时：'+str(e.message)
    except exceptions.HTTPError as e:
        flag3=False
        ErroResult='http请求错误:'+str(e.message)
    except Exception as e:
        flag3=False
        ErroResult='请求错误:'+traceback.format_exc()
    if flag3==False:
        text_cb(devip+' '+ErroResult+'   \n', 'fail')
    text_cb(devip+' 数据收集完成   \n', 'pass')

def face(path,flag,text_cb):
    types=flag.split('_')[0]
    flags=flag.split('_')[1]
    text_cb(flag+'参数排序开始......\n', 'detail')
    try:
        with open(path+'/data/'+types+'List.txt', 'r', encoding='utf-8') as f:
            dataStr=f.read()
            dataStr=dataStr.replace('\'','\"')
            #text_cb(dataStr, 'pass')
            dataStr='['+dataStr.replace(';\n',',')[0:-1]+']'
            dataJson=json.loads(dataStr)
            f.close()
        data={}
        for i in dataJson:
            for j in i.keys():
                data[j]=i[j][flags]
        if types=='face':
            width_i = 100
            height_i = 100
        elif types=='pedestrian':
            width_i = 100
            height_i = 200
        elif types=='vehicle':
            width_i = 150
            height_i = 100
        elif types=='bicycle':
            width_i = 100
            height_i = 200
        line_row_max=math.ceil( math.sqrt(len(data.keys())))
        pathBase=os.path.dirname(path)

        dataSort=sorted(data.items(),key=lambda x:x[1])
        #print(dataSort)
        toImage = Image.new('RGBA',(width_i*line_row_max,height_i*line_row_max))
        index=0
        for ii in dataSort:
            #print(path+'/face/'+ii[0])
            img0=cv2.imread(path+'/'+types+'/'+ii[0])
            #print(img0)
            xx=index%line_row_max
            yy=int(index/line_row_max)
            img1 = cv2.resize(img0, (width_i,height_i), interpolation=cv2.INTER_AREA)
            font = cv2.FONT_HERSHEY_SIMPLEX
            img2 = cv2.putText(img1, str(round(ii[1],5)), (2,15), font,0.5, (0,255,0), 1)
            loc = (int((xx%line_row_max)*width_i),int((yy%line_row_max)*height_i))
            img2 = Image.fromarray(cv2.cvtColor(img2,cv2.COLOR_BGR2RGB))
            toImage.paste(img2,loc)
            index=index+1
        if not os.path.exists(path+'/result/'+types+'/'):
            os.makedirs(path+'/result/'+types+'/')
        toImage.save(path+'/result/'+types+'/'+types+'_'+flags+'.png')
        text_cb(flag+'参数排序完成，排序图片保存路径为：'+path+'/result/'+types+'/'+types+'_'+flags+'.png  \n', 'pass')
    except Exception as e:
        text_cb('运行错误:'+traceback.format_exc()+'   \n', 'fail')
def face2(path,flag,text_cb):
    types=flag.split('_')[0]
    flag1=flag.split('_')[1]
    flag2=flag.split('_')[2]
    text_cb(flag+'参数排序开始......\n', 'detail')
    try:
        with open(path+'/data/'+types+'List.txt', 'r', encoding='utf-8') as f:
            dataStr=f.read()
            dataStr=dataStr.replace('\'','\"')
            #text_cb(dataStr, 'pass')
            dataStr='['+dataStr.replace(';\n',',')[0:-1]+']'
            dataJson=json.loads(dataStr)
            f.close()
        datax=[]
        datay=[]
        for i in dataJson:
            for j in i.keys():
                datax.append(float(i[j][flag1]))
                datay.append(float(i[j][flag2]))
                
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus']=False
                             
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.grid()
        ax1.set_title(flag)
        ax1.set_xlabel(flag1)
        ax1.set_ylabel(flag2)
        ax1.scatter(datax, datay, s=40,c='g', marker='.')
        #x_major_locator=MultipleLocator(1)
        #y_major_locator=MultipleLocator(1)
        ax=plt.gca()
        #ax.xaxis.set_major_locator(x_major_locator)
        #ax.yaxis.set_major_locator(y_major_locator)
        #plt.show()
        if not os.path.exists(path+'/result/'+types+'/'):
            os.makedirs(path+'/result/'+types+'/')
        savefig(path+'/result/'+types+'/'+types+'_'+flag+'.png')
        #toImage.save(path+'/result/'+types+'/'+flags+'.png')
        text_cb(flag+'参数关系绘制完成，图片保存路径为：'+path+'/result/'+types+'/'+types+'_'+flag+'.png    \n', 'pass')
    except Exception as e:
        text_cb('运行错误:'+traceback.format_exc()+'   \n', 'fail')
def alert(path,devip,flag,num,text_cb):
    alertAPI.alert(path,devip,flag,num,text_cb)
    #text_cb(flag+'参数关系绘制完成，图片保存路径为：'+path+'/result/'+types+'/'+flag+'.png    \n', 'pass')
def channel(ip,channelID,method,num,text_cb):
    if method=='批量修改':
        text_cb(ip+' 通道批量修改开始......\n', 'detail')

        try:
            flag=True
            if ':' in ip:
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            else :
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result0=requests.get(url='http://'+ip+'/api/channel/'+str(channelID), headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            config=result0.json()['data']["config"]
            results=requests.get(url='http://'+ip+'/api/channel?pageSize=99', headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            for channel in results.json()['data']:
                body={
                    "model":channel["model"],
                    "subModel":channel["subModel"],
                    "name":channel["name"],
                    "id":channel["id"],
                    "longitude":channel["longitude"],
                    "latitude":channel["latitude"],
                    "description":channel["description"],
                    "enabled":channel["enabled"],
                    "config":
                    {
                        "url":channel["config"]["url"],
                        "userName":channel["config"]["userName"],
                        "password":channel["config"]["password"],
                        "detectFrames":config["detectFrames"],
                        "trackSeconds":config["trackSeconds"],
                        "face":config["face"],
                        "pedestrian":config["pedestrian"],
                        "vehicle":config["vehicle"],
                        "nonmotor":config["nonmotor"],
                        "skeleton":config["skeleton"],
                        "multiFace":config["multiFace"],
                        "remain":config["remain"],
                        "cover":config["cover"],
                        "smogFire":config["smogFire"]
                        }
                    }
                result=requests.put(url='http://'+ip+'/api/channel/'+channel['id'], json=body,headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']}) 
                if result.json()['code']==200000:
                    text_cb('通道 '+channel['name']+' 修改成功  \n', 'pass')
                else:
                    result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                    text_cb('\n'+result+'\n', 'fail')
            text_cb(ip+' 通道批量修改完成！  \n', 'pass')
        except exceptions.ConnectionError as e:
            flag=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag==False:
            text_cb(ip+' '+ErroResult+'   \n', 'fail')
    if method=='批量增加':
        text_cb(ip+' 通道批量新建开始......\n', 'detail')

        try:
            flag=True
            if ':' in ip:
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            else :
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result0=requests.get(url='http://'+ip+'/api/channel/'+str(channelID), headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            data=result0.json()['data']
            config=result0.json()['data']["config"]
            for i in range(0,int(num)):
                body={
                    "model":data["model"],
                    "subModel":data["subModel"],
                    "name":data["name"]+"_"+str(i+1),
                    "longitude":data["longitude"],
                    "latitude":data["latitude"],
                    "description":data["description"],
                    "enabled":data["enabled"],
                    "config":
                    {
                        "areas":config["areas"],
                        "url":config["url"],
                        "userName":config["userName"],
                        "password":config["password"],
                        "detectFrames":config["detectFrames"],
                        "trackSeconds":config["trackSeconds"],
                        "face":config["face"],
                        "pedestrian":config["pedestrian"],
                        "vehicle":config["vehicle"],
                        "nonmotor":config["nonmotor"],
                        "skeleton":config["skeleton"],
                        "multiFace":config["multiFace"],
                        "remain":config["remain"],
                        "cover":config["cover"],
                        "smogFire":config["smogFire"]
                        }
                    }
                result=requests.post(url='http://'+ip+'/api/channel', json=body,headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']}) 
                if result.json()['code']==200000:
                    text_cb('通道 '+data["name"]+"_"+str(i+1)+' 新建成功  \n', 'pass')
                else:
                    result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                    text_cb('\n'+result+'\n', 'fail')
            text_cb(ip+' 通道批量新建完成！  \n', 'pass')
        except exceptions.ConnectionError as e:
            flag=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag==False:
            text_cb(ip+' '+ErroResult+'   \n', 'fail')
def task(ip,taskID,text_cb):
    text_cb(ip+' 任务批量修改开始......\n', 'detail')
    try:
        flag=True
        if ':' in ip:
            rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
        else :
            rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
        result0=requests.get(url='http://'+ip+'/api/channel/'+str(taskID)+'/task', headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        task0=result0.json()['data']
        result1=requests.get(url='http://'+ip+'/api/vehicleRepo?pageSize=99', headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        vehicleRepo=result1.json()['data']
        result2=requests.get(url='http://'+ip+'/api/faceRepo?pageSize=99', headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        faceRepo=result2.json()['data']
        results=requests.get(url='http://'+ip+'/api/task?pageSize=99', headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        index=0
        for task in results.json()['data']:
            body={
                "id":task["id"],
                "effectTime":task0["effectTime"],
                "alertThresholdMode":task0["alertThresholdMode"],
                "lowAlertThreshold":task0["lowAlertThreshold"],
                "highAlertThreshold":task0["highAlertThreshold"],
                "faceRepos":[{"id":faceRepo[index]["id"]}],
                "vehicleAlertMode":task0["vehicleAlertMode"],
                "vehicleRepos":[{"id":vehicleRepo[index]["id"]}],
                "channelID":str(task["id"]),
                "abnormalFilter":task0["abnormalFilter"]
                }
            index=index+1
            result=requests.put(url='http://'+ip+'/api/channel/'+str(task["id"])+'/task', json=body,headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']}) 
            if result.json()['code']==200000:
                text_cb('任务 '+str(task["id"])+' 修改成功  \n', 'pass')
            else:
                result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                text_cb('\n'+result+'\n', 'fail')
        text_cb(ip+' 任务批量修改完成！  \n', 'pass')
    except exceptions.ConnectionError as e:
        flag=False
        ErroResult='连接错误：'+str(e.args[0].reason)
    except exceptions.Timeout as e:
        flag=False
        ErroResult='请求超时：'+str(e.message)
    except exceptions.HTTPError as e:
        flag=False
        ErroResult='http请求错误:'+str(e.message)
    except Exception as e:
        flag=False
        ErroResult='请求错误:'+traceback.format_exc()
    if flag==False:
        text_cb(ip+' '+ErroResult+'   \n', 'fail')

def repo(ip,repoFaceId,repoVehicleId,method,num,text_cb):
    pass
    '''
    if method=='批量修改':
        text_cb(ip+' 通道批量修改开始......\n', 'detail')

        try:
            flag=True
            if ':' in ip:
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            else :
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result0=requests.get(url='http://'+ip+'/api/channel/'+str(channelID), headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            config=result0.json()['data']["config"]
            results=requests.get(url='http://'+ip+'/api/channel?pageSize=99', headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            for channel in results.json()['data']:
                body={
                    "model":channel["model"],
                    "subModel":channel["subModel"],
                    "name":channel["name"],
                    "id":channel["id"],
                    "longitude":channel["longitude"],
                    "latitude":channel["latitude"],
                    "description":channel["description"],
                    "enabled":channel["enabled"],
                    "config":
                    {
                        "url":channel["config"]["url"],
                        "userName":channel["config"]["userName"],
                        "password":channel["config"]["password"],
                        "detectFrames":config["detectFrames"],
                        "trackSeconds":config["trackSeconds"],
                        "face":config["face"],
                        "pedestrian":config["pedestrian"],
                        "vehicle":config["vehicle"],
                        "nonmotor":config["nonmotor"],
                        "skeleton":config["skeleton"],
                        "multiFace":config["multiFace"],
                        "remain":config["remain"],
                        "cover":config["cover"],
                        "smogFire":config["smogFire"]
                        }
                    }
                result=requests.put(url='http://'+ip+'/api/channel/'+channel['id'], json=body,headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']}) 
                if result.json()['code']==200000:
                    text_cb('通道 '+channel['name']+' 修改成功  \n', 'pass')
                else:
                    result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                    text_cb('\n'+result+'\n', 'fail')
            text_cb(ip+' 通道批量修改完成！  \n', 'pass')
        except exceptions.ConnectionError as e:
            flag=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag==False:
            text_cb(ip+' '+ErroResult+'   \n', 'fail')
    if method=='批量增加':
        text_cb(ip+' 通道批量新建开始......\n', 'detail')

        try:
            flag=True
            if ':' in ip:
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            else :
                rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result0=requests.get(url='http://'+ip+'/api/channel/'+str(channelID), headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
            data=result0.json()['data']
            config=result0.json()['data']["config"]
            for i in range(0,int(num)):
                body={
                    "model":data["model"],
                    "subModel":data["subModel"],
                    "name":data["name"]+"_"+str(i+1),
                    "longitude":data["longitude"],
                    "latitude":data["latitude"],
                    "description":data["description"],
                    "enabled":data["enabled"],
                    "config":
                    {
                        "areas":config["areas"],
                        "url":config["url"],
                        "userName":config["userName"],
                        "password":config["password"],
                        "detectFrames":config["detectFrames"],
                        "trackSeconds":config["trackSeconds"],
                        "face":config["face"],
                        "pedestrian":config["pedestrian"],
                        "vehicle":config["vehicle"],
                        "nonmotor":config["nonmotor"],
                        "skeleton":config["skeleton"],
                        "multiFace":config["multiFace"],
                        "remain":config["remain"],
                        "cover":config["cover"],
                        "smogFire":config["smogFire"]
                        }
                    }
                result=requests.post(url='http://'+ip+'/api/channel', json=body,headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']}) 
                if result.json()['code']==200000:
                    text_cb('通道 '+data["name"]+"_"+str(i+1)+' 新建成功  \n', 'pass')
                else:
                    result=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
                    text_cb('\n'+result+'\n', 'fail')
            text_cb(ip+' 通道批量新建完成！  \n', 'pass')
        except exceptions.ConnectionError as e:
            flag=False
            ErroResult='连接错误：'+str(e.args[0].reason)
        except exceptions.Timeout as e:
            flag=False
            ErroResult='请求超时：'+str(e.message)
        except exceptions.HTTPError as e:
            flag=False
            ErroResult='http请求错误:'+str(e.message)
        except Exception as e:
            flag=False
            ErroResult='请求错误:'+traceback.format_exc()
        if flag==False:
            text_cb(ip+' '+ErroResult+'   \n', 'fail')
    '''
