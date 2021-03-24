import getopt
import requests
import json
import sys
import hashlib


def post_json(url, data):
    resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    return resp.text


def get_json(url, params=None):
    resp = requests.get(url, params=params)
    return resp.json()


def gen_sk(ip,system):
    if system=="Fglinux":
        ret = get_json("http://%s:9000/api/GetDeviceInfo" % ip)
        uuid = ret['data']['UUID']
    elif system=="Delinux":
        ret = get_json("http://%s:9000/sys/DeviceInfo" % ip)
        uuid = ret['data']['Hardware']['UUID']
    return hashlib.md5(("deepglint%s" % uuid).encode(encoding='UTF-8')).hexdigest()


def main(ip,system,status):
    #print(system)
    #print(status)
    sk = gen_sk(ip,system)
    if status=='临时打开，重启后恢复':
        data={"On":1, "SecretKey":sk,"Permanent":False}
    elif status=='永久打开':
        data={"On":1, "SecretKey":sk,"Permanent":True}
    elif status=='临时关闭，重启后恢复':
        data={"On":0, "SecretKey":sk,"Permanent":False}
    else:
        data={"On":0, "SecretKey":sk,"Permanent":True}
    #print(data)  
    if system=="Fglinux":
        result=post_json("http://"+ip+":9000/api/SSH", data)
    elif system=="Delinux":
        result=post_json("http://"+ip+":9000/sys/SSH", data)
    return result
