import os
import json


tmpPath = './tmp/'


def getConfigInfo():
    readFile = open('config/config.json', 'r', encoding='utf-8')
    readData = readFile.read()
    readFile.close()

    if readData.startswith(u'\ufeff'):
        readData = readData.encode('utf8')[3:].decode('utf8')
    return json.loads(readData)


def getIoTServerInfo(name):
    readFile = open('config/IoTServer.config', 'r', encoding='utf-8')
    readData = readFile.read()
    readFile.close()

    if readData.startswith(u'\ufeff'):
        readData = readData.encode('utf8')[3:].decode('utf8')
    allData = json.loads(readData)

    IoTServerInfo = {
        "name": name,
        "ip": allData[name]["ip"],
        "port": allData[name]["port"],
        "username": allData[name]["username"],
        "password": allData[name]["password"]
    }
    return IoTServerInfo


def getDevModel():
    readFile = open('config/devModel.config', 'r', encoding='utf-8')
    readData = readFile.read()
    readFile.close()

    if readData.startswith(u'\ufeff'):
        readData = readData.encode('utf8')[3:].decode('utf8')
    return json.loads(readData)


def getList(file):
    global tmpPath

    allLines = []
    if os.path.exists(tmpPath + file):
        # 如果ipList.txt存在，还要判断内容是否为空
        if os.path.getsize(tmpPath + file):
            # 文件存在且不为空
            readFile = open(tmpPath + file, 'r', encoding='utf-8')
            try:
                for ip in readFile.readlines():
                    allLines.append(ip.rstrip('\n'))
            finally:
                readFile.close()
                return allLines
        else:
            # 文件存在，但是内容为空
            return None
    else:
        # 如果ipList.txt不存在，则返回None
        return None


def setList(devip,file):
    global tmpPath

    if os.path.exists(tmpPath +file):  # 如果ipList.txt存在，还要判断内容是否为空
        if os.path.getsize(tmpPath + file):  # 文件存在且不为空
            readFile = open(tmpPath + file, 'r', encoding='utf-8')
            for ip in readFile.readlines():
                if(devip == ip.rstrip('\n')):
                    # 如果ip相等，则直接返回
                    readFile.close()
                    return

            # 如果遍历完还没有返回，说明是一个新ip，则写入文件
            readFile.close()
            readFile = open(tmpPath + file, 'a', encoding='utf-8')
            readFile.write(devip + '\n')
            readFile.close()
            return
        else:
            # 文件存在，但是内容为空
            pass
    else:
        if not os.path.exists(tmpPath):
            # 如果目录不存在，则首先创建目录
            os.makedirs(tmpPath)

    # 写入当前ip
    readFile = open(tmpPath + file, 'w', encoding='utf-8')
    try:
        readFile.write(devip + '\n')
    finally:
        readFile.close()
