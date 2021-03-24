from tkinter import *
from tkinter import messagebox
import requests
import requests.exceptions as exceptions
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import os

'''
    升级三部曲：
    1、首先升级FGUpgrade，防止添加了新的功能，但是老版本的FGUpgrade不支持；
    2、比较升级工具内的版本和设备当前的版本，如果版本不同，则将升级工具内的版本上传到设备上（/home/deepglint/PKG/.preinstall/目录[预安装方式]；/home/deepglint/PKG/目录[直接安装方式]）
    3、调用Reboot接口重启设备
'''

percent=0
fileSize=1

def getDevInfo(devip):
    header = {'Content-Type': 'application/json'}
    url = 'http://' + devip + ':9000/api/GetDeviceInfo'

    try:
        response = requests.get(url, headers=header)
    except exceptions.ConnectionError as e:
        messagebox.showwarning(message='连接错误：'+str(e.args[0].reason))
    except exceptions.Timeout as e:
        messagebox.showwarning(message='请求超时：'+str(e.message))
    except exceptions.HTTPError as e:
        messagebox.showwarning(message='http请求错误:'+str(e.message))
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showwarning(
                message='请求错误：'+str(response.status_code)+' '+str(response.reason))
            return None


def getDevInfo4Reboot(devip):
    header = {'Content-Type': 'application/json'}
    url = 'http://' + devip + ':9000/api/GetDeviceInfo'

    try:
        response = requests.get(url, headers=header,timeout=0.4)
    except exceptions.ConnectionError as e:
        return None
    except exceptions.Timeout as e:
        return None
    except exceptions.HTTPError as e:
        return None
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            return response.json()
        else:
            return None


def fileUpload(devip, filename):
    global fileSize
    url = 'http://' + devip + ':9000/api/TransferFile'

    # readFile = open('./fgapp/'+filename, "rb")  # 将要上传的文件读取上来
    #readData = readFile.read()

    # 直接升级文件存放方式
    # payload = {"File": (filename, readData),
    #           "FileName": (None, filename)}
    path='./fgapp/'+filename
    e = MultipartEncoder(
    fields={'File': ('filename', open(path, 'rb')),
    "FileName": (None, filename)
    }
    )
    fileSize=os.path.getsize(path)
    m = MultipartEncoderMonitor(e, my_callback)

    # 预安装文件存放方式
    # if('FGUpgrade' in filename):
    #     payload = {"File": (filename, readData),
    #                "FileName": (None, filename)}
    # else:
    #     payload = {"File": (filename, readData),
    #                "FileName": (None, '/home/deepglint/PKG/.preinstall/' + filename)}

    try:
        response = requests.post(url, data=m, headers={
                                 'Content-Type': m.content_type})
        #response = requests.post(url, files=payload, timeout=100)
    except exceptions.ConnectionError as e:
        messagebox.showwarning(message='连接错误：'+str(e))
        # readFile.close()
        return False
    except exceptions.Timeout as e:
        messagebox.showwarning(message='请求超时：'+str(e.message))
        # readFile.close()
        return False
    except exceptions.HTTPError as e:
        messagebox.showwarning(message='http请求错误:'+str(e.message))
        # readFile.close()
        return False
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            # readFile.close()
            return True
        else:
            messagebox.showwarning(
                message='请求错误：'+str(response.status_code)+' '+str(response.reason))
            # readFile.close()
            return False


def doUpgrade(devip, filename):
    header = {'Content-Type': 'application/json'}
    url = 'http://' + devip + ':9000/api/DoUpgrade'
    data = {
        "FileFullPath": '/home/deepglint/PKG/' + filename
    }

    try:
        response = requests.post(url, headers=header, json=data)
    except exceptions.ConnectionError as e:
        messagebox.showwarning(message='连接错误：'+str(e.args[0].reason))
        return None
    except exceptions.Timeout as e:
        messagebox.showwarning(message='请求超时：'+str(e.message))
        return None
    except exceptions.HTTPError as e:
        messagebox.showwarning(message='http请求错误:'+str(e.message))
        return None
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            jsonData = response.json()
            return jsonData['data']['JobID']
        else:
            messagebox.showwarning(
                message='请求错误：'+str(response.status_code)+' '+str(response.reason))
            return None


def doUpgradeV2(devip):
    header = {'Content-Type': 'application/json'}
    url = 'http://' + devip + ':9000/api/DoUpgradeV2'
    data = {}
    try:
        response = requests.post(url, headers=header, json=data)
    except exceptions.ConnectionError as e:
        messagebox.showwarning(message='连接错误：'+str(e.args[0].reason))
        return None
    except exceptions.Timeout as e:
        messagebox.showwarning(message='请求超时：'+str(e.message))
        return None
    except exceptions.HTTPError as e:
        messagebox.showwarning(message='http请求错误:'+str(e.message))
        return None
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            jsonData = response.json()
            return jsonData['data']['JobID']
        else:
            messagebox.showwarning(
                message='请求错误：'+str(response.status_code)+' '+str(response.reason))
            return None


def getUpgradeProgress(devip, jobid):
    header = {'Content-Type': 'application/json'}
    url = 'http://' + devip + ':9000/api/UpgradeProgress'
    data = {
        "JobID": jobid
    }

    try:
        response = requests.get(url, headers=header, json=data)
    except exceptions.ConnectionError as e:
        messagebox.showwarning(message='连接错误：'+str(e.args[0].reason))
    except exceptions.Timeout as e:
        messagebox.showwarning(message='请求超时：'+str(e.message))
    except exceptions.HTTPError as e:
        messagebox.showwarning(message='http请求错误:'+str(e.message))
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showwarning(
                message='请求错误：'+str(response.status_code)+' '+str(response.reason))
            return None


def reboot(devip):
    header = {'Content-Type': 'application/json'}
    url = 'http://' + devip + ':9000/api/Reboot'
    data = {}
    try:
        response = requests.post(url, headers=header, json=data)
    except exceptions.ConnectionError as e:
        messagebox.showwarning(message='连接错误：'+str(e.args[0].reason))
        return False
    except exceptions.Timeout as e:
        messagebox.showwarning(message='请求超时：'+str(e.message))
        return False
    except exceptions.HTTPError as e:
        messagebox.showwarning(message='http请求错误:'+str(e.message))
        return False
    else:
        # 通过status_code判断请求结果是否正确
        if response.status_code == 200:
            return True
        else:
            messagebox.showwarning(
                message='请求错误：'+str(response.status_code)+' '+str(response.reason))
            return False

def my_callback(monitor):
    global percent
    global fileSize
    percent=monitor.bytes_read/fileSize
