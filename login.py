# -*- coding: utf-8 -*-
# import tkinter as tk
from tkinter import *
import time
import json
import tkinter.font as tf
import tkinter.constants as const
from iot import iotManage
from verifyAccount import verifyAccountData
from mttkinter import mtTkinter as tk
from uploadWin import uploadWin
from uploadWin_processbar import uploadWin
from upgradeWin import upgradeWin
from LANUpgradeUI import LANUpgradeUI
from OTAUpgradeUI import OTAUpgradeUI
import getConfig
import LANUpgradeAPI
import OTAUpgradeAPI


class loginWin(object):
    def __init__(self):

        # 创建主窗口
        self.loginWin = tk.Tk()
        self.loginWin.geometry('400x600')
        self.loginWin.resizable(False, False)

        # 设置标题内容
        self.loginWin.title("fduUtil")

        # 第一部分： title
        self.titleFrame = Frame(self.loginWin)  # , bg='red')

        # pic frame
        self.picFrame = Frame(self.titleFrame)  # , bg='blue')
        self.image_file = PhotoImage(
            file='pic/deepglintLogin.gif')  # 加载图片文件
        self.labelPic = Label(self.picFrame, image=self.image_file)

        # ver frame
        self.toolVerFrame = Frame(self.titleFrame)  # , bg='green')
        self.fontVer = tf.Font(family='arial', size=9, weight=tf.BOLD)
        self.labelToolVer = Label(
            self.toolVerFrame, text='设备软件升级工具 v0.0.1', font=self.fontVer)

        # 第二部分： config信息展示
        self.configJson = getConfig.getConfigInfo()

        # config frame
        self.configFrame = Frame(self.loginWin)  # , bg='red')
        self.fontConfig = tf.Font(family='arial', size=13, weight=tf.BOLD)
        self.configLabel = Label(
            self.configFrame, text='设备: ' + self.configJson["DisplayName"] + '\n\n' +
            '型号: ' + self.configJson["DeviceName"] + '\n\n' +
            '版本: ' + self.configJson["SWVer"], justify=const.LEFT, font=self.fontConfig)

        # 第三部分： listbox显示软件详细信息
        self.listFrame = Frame(self.loginWin)  # , bg='red')
        self.listBox = Listbox(self.listFrame, selectbackground='red')
        self.scrollBar = Scrollbar(
            self.listBox, command=self.listBox.yview)
        self.listBox.config(yscrollcommand=self.scrollBar.set)

        for i in range(len(self.configJson["Apps"])):
            self.listBox.insert(END, "fgapp"+str(i+1))
            self.listBox.insert(END, "名称：" +
                                self.configJson["Apps"][i]["name"])
            self.listBox.insert(END, "版本：" +
                                self.configJson["Apps"][i]["version"])
            self.listBox.insert(END, "")

        # 第四部分： 功能切换按钮
        self.buttonFrame = Frame(self.loginWin)  # , bg='red')
        self.fontButton = tf.Font(family='arial', size=15, weight=tf.BOLD)
        self.LANUpgradeButton = Button(
            self.buttonFrame, command=self.loginLANUpgrade, text='内网升级', font=self.fontButton, width=10, bd=2)
        self.OTAUpgradeButton = Button(
            self.buttonFrame, command=self.loginOTAUpgrade, text='OTA升级', font=self.fontButton, width=10, state='disabled', bd=2)

    def gui_arrang(self):
        # 第一部分： title
        self.titleFrame.pack(side=const.TOP, pady=10,
                             fill=const.X, expand=const.NO)

        self.picFrame.pack(side=const.LEFT, fill=const.NONE, expand=const.NO)
        self.labelPic.pack(side=const.LEFT, fill=const.X, expand=const.NO)

        self.toolVerFrame.pack(
            side=const.LEFT, fill=const.BOTH, expand=const.YES)
        self.labelToolVer.pack(side=const.TOP, padx=10,
                               fill=const.X, expand=const.YES)

        # 第二部分： config信息展示
        self.configFrame.pack(side=const.TOP, fill=const.X, expand=const.NO)
        self.configLabel.pack(side=const.TOP, padx=10, pady=4,
                              fill=const.X, anchor=const.W)

        # 第三部分： listbox显示软件详细信息
        self.listFrame.pack(side=const.TOP, padx=40, pady=10,
                            fill=const.BOTH, expand=const.YES)
        self.listBox.pack(side=const.TOP,
                          fill=const.BOTH, expand=const.YES, anchor=const.N)
        self.scrollBar.pack(side=const.RIGHT, fill=const.Y)

        # 第四部分： 功能切换按钮
        self.buttonFrame.pack(side=const.BOTTOM, pady=10,
                              fill=const.NONE, expand=const.NO)
        self.LANUpgradeButton.pack(side=const.LEFT, padx=30, pady=20,
                                   expand=const.NO, anchor=const.N)
        self.OTAUpgradeButton.pack(side=const.LEFT, padx=30, pady=20,
                                   expand=const.NO, anchor=const.N)

    def saveLastInfo(self):
        self.saveLastInfoFile = open(
            'tmp/lastInfoTemp.txt', 'w+', encoding='utf-8')
        self.saveLastInfoFileDataJson = {}
        self.saveLastInfoFileDataJson["state"] = str(self.CheckVar.get())
        self.saveLastInfoFileDataJson["server"] = self.Combo.get()
        self.saveLastInfoFile.write(json.dumps(
            self.saveLastInfoFileDataJson, ensure_ascii=False))
        self.saveLastInfoFile.close()

    def getLastInfo(self):
        self.LastInfoFile = open('tmp/lastInfoTemp.txt', 'r', encoding='utf-8')
        self.LastInfo = self.LastInfoFile.read()
        self.LastInfoFile.close()

        if self.LastInfo.startswith(u'\ufeff'):
            self.LastInfo = self.LastInfo.encode('utf8')[3:].decode('utf8')
        self.LastInfoJson = json.loads(self.LastInfo)

        self.LastInfos = ['', '', '', '']
        self.LastInfos[0] = self.LastInfoJson["state"]

        self.readFile = open('config/IoTServer.config', 'r', encoding='utf-8')
        self.readAccountData = self.readFile.read()
        self.readFile.close()
        if self.readAccountData.startswith(u'\ufeff'):
            self.readAccountData = self.readAccountData.encode('utf8')[
                3:].decode('utf8')
        self.readAccountDataJson = json.loads(self.readAccountData)
        if (self.LastInfoJson["state"] == "1"):
            self.LastInfos[1] = self.LastInfoJson["server"]
            self.LastInfos[2] = self.readAccountDataJson[self.LastInfoJson["server"]]["username"]
            self.LastInfos[3] = self.readAccountDataJson[self.LastInfoJson["server"]]["password"]
        else:
            self.LastInfos[2] = ""
            self.LastInfos[3] = ""
        return self.LastInfos

    def loginIOT_interface(self):
        iot = iotManage()
        iot.gui_arrang()

    # 验证用户名和密码是否正确
    def verifyAccount_interface(self):
        serverName = self.Combo.get()
        userName = self.input_account.get()
        password = self.input_password.get()
        IoTServer = verifyAccountData.readAccount()
        verifyResult = verifyAccountData.verifyAccount(
            serverName, userName, password, IoTServer)

        if verifyResult == 'ok':
            self.updateData(serverName)
            self.loginWin.destroy()
            iot = mainWin()
            iot.gui_arrang()

        elif verifyResult == 'pok':
            messagebox.showinfo(message='请输入正确的用户名或密码！')

    def updateData(self, tempData):
        updateFile = open('tmp/data.txt', 'w', encoding='utf-8')
        updateFile.write(tempData)
        updateFile.close()

    def loginLANUpgrade(self):
        self.loginWin.destroy()
        LANUpgrade = LANUpgradeUI()
        LANUpgrade.gui_arrang()


    def loginOTAUpgrade(self):
        self.loginWin.destroy()
        OTA = OTAUpgradeUI()
        OTA.gui_arrang()


class longTime(object):
    def __init__(self):
        self.readFile = open('tmp/data.txt', 'r', encoding='utf-8')
        self.accountName = self.readFile.read()
        self.readFile.close()
        self.IoTServerInfo = config.getIoTServerInfo(
            self.accountName)

    # 指定deviceID判断设备是否在线
    def deviceIsOnline(self, deviceId):
        flag = False
        self.getDeviceListDataTemp = {
            "url": "http://"+self.IoTServerInfo["ip"]+":"+self.IoTServerInfo["port"]+"/api/device/search",
            "body": {
                "deviceId": deviceId,
                "online": 1
            },
            "token": getAPI.getToken(self.IoTServerInfo)
        }

        # self.getDeviceListResponceTemp=getAPI.getDeviceList( self.getDeviceListDataTemp)
        # if self.getDeviceListResponceTemp["data"]["totalElements"]==0:
        x = self.treeviewUpgrade.get_children()
        for item in x:
            self.treeviewUpgrade.delete(item)

        self.treeviewUpgrade.insert('', 0, values=("最后确认是否有待升级的设备，请稍等！"))

        self.text_ongoing = Label(self.upgradeTab, text=str(
            self.deviceNumber)+"台", bg="white", font=('楷体', 15))

        self.text_ongoing.grid(row=8, column=2, padx=10, pady=5, sticky='W')

        self.treeviewUpgrade.grid(row=3, column=5, rowspan=6,
                                  columnspan=3, ipadx=30, ipady=30)

        time.sleep(120)
        self.getDeviceListResponceTemp = getAPI.getDeviceList(
            self.getDeviceListDataTemp)
        if self.getDeviceListResponceTemp["data"]["totalElements"] != 0:
            flag = True
        return flag

    # 判断是否还有待更新的设备
    def deviceIsNewVersion(self):
        flag_deviceIsNewVersion = True
        self.readVersionModel = open(
            'tmp/versionModelTemp.txt', 'r', encoding='utf-8')
        self.readVersionModelData = self.readVersionModel.read()
        self.readVersionModel.close()

        self.getDeviceListData = {
            "url": "http://"+self.IoTServerInfo["ip"]+":"+self.IoTServerInfo["port"]+"/api/device/search",
            "body": {
                "deviceModel": self.readVersionModelData,
                "online": 1
            },
            "token": getAPI.getToken(self.IoTServerInfo)
        }
        self.getDeviceListResponceIsNewVersion = getAPI.getDeviceList(
            self.getDeviceListData)

        # 如果没有，等待后再次判断
        self.deviceNumber = 0
        for i in range(self.getDeviceListResponceIsNewVersion["data"]["totalElements"]):
            self.checkUpdateData = {
                "url": "http://"+self.IoTServerInfo["ip"]+":"+self.IoTServerInfo["port"]+"/api/fota/checkUpdate?fwname="+self.getDeviceListResponceIsNewVersion["data"]["content"][i]["appName"]+"&fwver="+self.getDeviceListResponceIsNewVersion["data"]["content"][i]["appVer"],
                "token": getAPI.getToken(self.IoTServerInfo)
            }
            self.checkUpdateResp = getAPI.checkUpdate(
                self.checkUpdateData)
            if self.checkUpdateResp["data"]["newerversion"] == True:
                self.deviceNumber = self.deviceNumber+1
        if self.deviceNumber == 0:
            time.sleep(120)
            for j in range(self.getDeviceListResponceIsNewVersion["data"]["totalElements"]):
                self.checkUpdateData = {
                    "url": "http://"+self.IoTServerInfo["ip"]+":"+self.IoTServerInfo["port"]+"/api/fota/checkUpdate?fwname="+self.getDeviceListResponceIsNewVersion["data"]["content"][j]["appName"]+"&fwver="+self.getDeviceListResponceIsNewVersion["data"]["content"][j]["appVer"],
                    "token": getAPI.getToken(self.IoTServerInfo)
                }
                self.checkUpdateResp = getAPI.checkUpdate(
                    self.checkUpdateData)
                if self.checkUpdateResp["data"]["newerversion"] == True:
                    self.deviceNumber = self.deviceNumber+1
            if self.deviceNumber == 0:
                flag_deviceIsNewVersion = False
        return flag_deviceIsNewVersion


if __name__ == '__main__':
    # 初始化对象
    L = loginWin()

    # 进行布局
    L.gui_arrang()

    # 主程序执行
    mainloop()
