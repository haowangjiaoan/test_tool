from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from mttkinter import mtTkinter as tk
import tkinter.constants as const
import tkinter.font as tf
import tkinter
from threading import Timer
import threading
import re
import getConfig
import toolAPI
import toolProc
import time
import event
import os
from multiprocessing import Process
#import PyQt5.sip


class toolUI(object):
    def __init__(self):
        self.UpgradeWin = tk.Tk()
        self.UpgradeWin.title(string='测试工具')
        self.UpgradeWin.geometry('1200x600')
        #self.UpgradeWin.resizable(False, False)

        # operate frame
        self.operateFrame = tk.Frame(self.UpgradeWin)  # 定义frame

        # 文本输入框
        #ft = tf.Font(family='黑体', size=15, weight=tf.BOLD)

        #ssh操作
        self.sshFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.sshLabel = Label(self.sshFrame, text='SSH端口操作',width=11,foreground='blue',anchor='e')
        #sshDeviceIpvar = tkinter.StringVar()
        #sshDeviceIpvar.set("172.17.0.1")
        self.sshDeviceIpCombo=ttk.Combobox(self.sshFrame,width=14)
        self.sshSystemCombo=ttk.Combobox(self.sshFrame,width=12)
        self.sshSystemCombo["value"]=("Delinux","Fglinux")
        self.sshSystemCombo.current(0)
        self.sshTypeCombo=ttk.Combobox(self.sshFrame,width=17)
        self.sshTypeCombo["value"]=("临时打开，重启后恢复","永久打开","临时关闭，重启后恢复","永久关闭")
        self.sshTypeCombo.current(1)
        self.sshSubmitButton = Button(self.sshFrame, command=self.sshDef, text="确定",width=7)

        #api操作
        self.apiFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.apiLabel = Label(self.apiFrame, text='API调试',width=11,foreground='blue',anchor='e')
        self.apiDeviceIpCombo=ttk.Combobox(self.apiFrame,width=14)
        self.apiUrlCombo=ttk.Combobox(self.apiFrame,width=18)
        self.apiMethodCombo=ttk.Combobox(self.apiFrame,width=5)
        self.apiMethodCombo["value"]=("post","get","put","delete")
        self.apiMethodCombo.current(0)
        apiBodyVar = tkinter.StringVar()
        apiBodyVar.set("{}")
        self.apiBodyEntry=Entry(self.apiFrame,textvariable=apiBodyVar,width=15)
        self.apiTokenCombo=ttk.Combobox(self.apiFrame,width=9)
        self.apiTokenCombo["value"]=("token/l4t","token/l4ab","no")
        self.apiTokenCombo.current(0)
        self.apiSubmitButton = Button(self.apiFrame, command=self.apiDef, text="确定",width=7)

        #系统性能
        self.sysFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.sysLabel = Label(self.sysFrame, text='系统监控',width=11,foreground='blue',anchor='e')
        self.sysDeviceIpCombo=ttk.Combobox(self.sysFrame,width=14)
        sysUserVar = tkinter.StringVar()
        sysUserVar.set("root/On1shiuva4")
        self.sysUserEntry=Entry(self.sysFrame,textvariable=sysUserVar,width=15)
        self.sysLnameCombo=ttk.Combobox(self.sysFrame,width=10)
        self.sysLnameCombo["value"]=("DEH5Bin","MainThread")
        self.sysLnameCombo.current(0)
        self.sysStorageCombo=ttk.Combobox(self.sysFrame,width=5)
        self.sysStorageCombo["value"]=("15G","10T","12.4G")
        self.sysStorageCombo.current(0)
        self.sysSubmitButton = Button(self.sysFrame, command=self.sysDef, text="开始",width=7)
        self.sysStopButton = Button(self.sysFrame, command=self.sysStopDef, text="关闭",width=7)

        #图像base64互转
        self.base64Frame = tk.Frame(self.operateFrame)  # 定义frame
        self.toBase64Label = Label(self.base64Frame, text='图像转base64',width=11,foreground='blue',anchor='e')
        self.toBase64PathVar = tkinter.StringVar()
        self.toBase64PathVar.set("图片路径")
        self.toBase64PathEntry=Entry(self.base64Frame,textvariable=self.toBase64PathVar,width=17)
        self.toBase64SelectButton = Button(self.base64Frame, command=self.toBase64SelectImageDef, text="选择图片",width=7)
        self.toBase64SubmitButton = Button(self.base64Frame, command=self.toBase64Def, text="确定",width=7)
        self.base64toLabel = Label(self.base64Frame, text='base64转图像',width=15,foreground='blue',anchor='e')
        self.base64toPathVar = tkinter.StringVar()
        self.base64toPathVar.set("编码路径")
        self.base64toPathEntry=Entry(self.base64Frame,textvariable=self.base64toPathVar,width=15)
        self.base64toSelectButton = Button(self.base64Frame, command=self.base64toSelectImageDef, text="选择编码",width=7)
        self.base64toSubmitButton = Button(self.base64Frame, command=self.base64toDef, text="确定",width=7)

        #算法数据收集
        self.dataFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.dataLabel = Label(self.dataFrame, text='算法数据收集',width=11,foreground='blue',anchor='e')
        self.dataDeviceIpCombo=ttk.Combobox(self.dataFrame,width=14)
        self.dataOpenApiButton = Button(self.dataFrame, command=self.dataOpenApi, text="打开设备接口",width=11)
        self.dataCloseApiButton = Button(self.dataFrame, command=self.dataCloseApi, text="关闭设备接口",width=11)
        self.dataCheckVar1 = StringVar(value="1")
        self.dataCheckVar2 = StringVar(value="1")
        self.dataCheckVar3 = StringVar(value="1")
        self.dataCheckVar4 = StringVar(value="1")
        self.dataCheck1 = Checkbutton(self.dataFrame, text="人脸", variable=self.dataCheckVar1)
        self.dataCheck2 = Checkbutton(self.dataFrame, text="行人", variable=self.dataCheckVar2)
        self.dataCheck3 = Checkbutton(self.dataFrame, text="机动车", variable=self.dataCheckVar3)
        self.dataCheck4 = Checkbutton(self.dataFrame, text="非机动车", variable=self.dataCheckVar4)
        
        self.dataFrame2 = tk.Frame(self.operateFrame)
        self.dataLabel2 = Label(self.dataFrame2, text='',width=11,foreground='blue',anchor='e')
        self.dataPathVar = tkinter.StringVar()
        self.dataPathVar.set("保存路径")
        self.dataPathEntry=Entry(self.dataFrame2,textvariable=self.dataPathVar,width=17)
        self.dataPathButton = Button(self.dataFrame2, command=self.dataPathCapture, text="选择路径",width=7)
        self.dataNumVar = tkinter.StringVar()
        self.dataNumVar.set("采集时间（分钟）")
        self.dataNumEntry=Entry(self.dataFrame2,textvariable=self.dataNumVar,width=14)
        self.dataButton = Button(self.dataFrame2, command=self.dataCapture, text="收集",width=7)

        #算法参数排序
        self.faceFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.faceLabel = Label(self.faceFrame, text='算法参数排序',width=11,foreground='blue',anchor='e')
        self.facePathVar = tkinter.StringVar()
        self.facePathVar.set("数据路径")
        self.facePathEntry=Entry(self.faceFrame,textvariable=self.facePathVar,width=17)
        self.facePathButton = Button(self.faceFrame, command=self.facePathCapture, text="选择路径",width=7)
        self.faceCombo=ttk.Combobox(self.faceFrame,width=20)
        self.faceCombo["value"]=("face_bbox","face_quality","face_confidence","face_blur","face_yaw","face_pitch","face_roll",
                                 "pedestrian_bbox","pedestrian_quality","pedestrian_confidence",
                                 "vehicle_bbox","vehicle_quality","vehicle_confidence",
                                 "bicycle_bbox","bicycle_quality","bicycle_confidence")
        self.faceCombo.current(0)
        self.faceButton = Button(self.faceFrame, command=self.face, text="确定",width=7)

        #算法参数关系
        self.faceFrame2 = tk.Frame(self.operateFrame)  # 定义frame
        self.faceLabel2 = Label(self.faceFrame2, text='算法参数关系',width=11,foreground='blue',anchor='e')
        self.facePathVar2 = tkinter.StringVar()
        self.facePathVar2.set("数据路径")
        self.facePathEntry2=Entry(self.faceFrame2,textvariable=self.facePathVar2,width=17)
        self.facePathButton2 = Button(self.faceFrame2, command=self.facePathCapture2, text="选择路径",width=7)
        self.faceCombo2=ttk.Combobox(self.faceFrame2,width=20)
        self.faceCombo2["value"]=("face_bbox_quality","face_bbox_confidence","face_bbox_blur","face_blur_quality","face_blur_confidence","face_confidence_quality",
                                 "pedestrian_bbox_quality","pedestrian_bbox_confidence",
                                 "vehicle_bbox_quality","vehicle_bbox_confidence",
                                 "bicycle_bbox_quality","bicycle_bbox_confidence")
        self.faceCombo2.current(0)
        self.faceButton2 = Button(self.faceFrame2, command=self.face2, text="确定",width=7)
        

        #人脸报警阈值
        self.alertFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.alertLabel = Label(self.alertFrame, text='人脸报警阈值',width=11,foreground='blue',anchor='e')
        self.alertPathVar = tkinter.StringVar()
        self.alertPathVar.set("保存路径")
        self.alertPathEntry=Entry(self.alertFrame,textvariable=self.alertPathVar,width=17)
        self.alertPathButton = Button(self.alertFrame, command=self.alertPathCapture, text="选择路径",width=7)
        self.alertDeviceIpCombo=ttk.Combobox(self.alertFrame,width=14)
        self.alertCombo=ttk.Combobox(self.alertFrame,width=10)
        self.alertCombo["value"]=("output104","output106","output107","outputSH")
        self.alertCombo.current(0)
        self.alertNumVar = tkinter.StringVar()
        self.alertNumVar.set("统计个数")
        self.alertNumEntry=Entry(self.alertFrame,textvariable=self.alertNumVar,width=10)
        self.alertButton = Button(self.alertFrame, command=self.alert, text="确定",width=7)

        #通道批量配置/修改
        self.channelFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.channelLabel = Label(self.channelFrame, text='通道批量增改',width=11,foreground='blue',anchor='e')
        self.channelDeviceIpCombo=ttk.Combobox(self.channelFrame,width=14)
        self.channelIdVar = tkinter.StringVar()
        self.channelIdVar.set("参考通道ID")
        self.channelIdEntry=Entry(self.channelFrame,textvariable=self.channelIdVar,width=10)
        self.channelCombo=ttk.Combobox(self.channelFrame,width=10)
        self.channelCombo["value"]=("批量增加","批量修改")
        self.channelCombo.current(0)
        self.channelNumVar = tkinter.StringVar()
        self.channelNumVar.set("操作个数")
        self.channelNumEntry=Entry(self.channelFrame,textvariable=self.channelNumVar,width=10)
        self.channelButton = Button(self.channelFrame, command=self.channel, text="确定",width=7)

        #库批量配置/修改
        self.repoFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.repoLabel = Label(self.repoFrame, text='库批量增改',width=11,foreground='blue',anchor='e')
        self.repoDeviceIpCombo=ttk.Combobox(self.repoFrame,width=14)
        self.repoFaceIdVar = tkinter.StringVar()
        self.repoFaceIdVar.set("参考人脸库ID")
        self.repoFaceIdEntry=Entry(self.repoFrame,textvariable=self.repoFaceIdVar,width=12)
        self.repoVehicleIdVar = tkinter.StringVar()
        self.repoVehicleIdVar.set("参考车辆库ID")
        self.repoVehicleIdEntry=Entry(self.repoFrame,textvariable=self.repoVehicleIdVar,width=12)
        self.repoCombo=ttk.Combobox(self.repoFrame,width=10)
        self.repoCombo["value"]=("批量增加","批量修改")
        self.repoCombo.current(0)
        self.repoNumVar = tkinter.StringVar()
        self.repoNumVar.set("操作个数")
        self.repoNumEntry=Entry(self.repoFrame,textvariable=self.repoNumVar,width=10)
        self.repoButton = Button(self.repoFrame, command=self.repo, text="确定",width=7)
        self.repoButton.config(state="disabled")

        #任务批量修改
        self.taskFrame = tk.Frame(self.operateFrame)  # 定义frame
        self.taskLabel = Label(self.taskFrame, text='任务批量修改',width=11,foreground='blue',anchor='e')
        self.taskDeviceIpCombo=ttk.Combobox(self.taskFrame,width=14)
        self.taskIdVar = tkinter.StringVar()
        self.taskIdVar.set("参考任务ID")
        self.taskIdEntry=Entry(self.taskFrame,textvariable=self.taskIdVar,width=10)
        self.taskButton = Button(self.taskFrame, command=self.task, text="确定",width=7)

        

        
        #self.sshDeviceIpCombo = ttk.Combobox(self.sshFrame)

        
        ipList = getConfig.getList('ipList.txt')
        if(ipList != None):
            self.sshDeviceIpCombo['value'] = tuple(ipList)
            self.sshDeviceIpCombo.current(len(ipList)-1)
            self.apiDeviceIpCombo['value'] = tuple(ipList)
            self.apiDeviceIpCombo.current(len(ipList)-1)
            self.sysDeviceIpCombo['value'] = tuple(ipList)
            self.sysDeviceIpCombo.current(len(ipList)-1)
            self.dataDeviceIpCombo['value'] = tuple(ipList)
            self.dataDeviceIpCombo.current(len(ipList)-1)
            self.alertDeviceIpCombo['value'] = tuple(ipList)
            self.alertDeviceIpCombo.current(len(ipList)-1)
            self.channelDeviceIpCombo['value'] = tuple(ipList)
            self.channelDeviceIpCombo.current(len(ipList)-1)
            self.repoDeviceIpCombo['value'] = tuple(ipList)
            self.repoDeviceIpCombo.current(len(ipList)-1)
            self.taskDeviceIpCombo['value'] = tuple(ipList)
            self.taskDeviceIpCombo.current(len(ipList)-1)
        urlList = getConfig.getList('urlList.txt')
        if(ipList != None):
            self.apiUrlCombo['value'] = tuple(urlList)
            self.apiUrlCombo.current(len(urlList)-1)
    
        #self.backButton = Button(self.sshFrame, command=self.backFunc, text="返回", bd=2)

        # text frame
        # self.textFrame = tk.Frame(self.UpgradeWin)  # 定义frame

        self.text = Text(self.UpgradeWin,bd=2,wrap=NONE)
        self.scrollbar = Scrollbar(self.text, command=self.text.yview,width=10)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbarX = Scrollbar(self.text, command=self.text.xview, orient=HORIZONTAL,width=10)
        self.text.config(xscrollcommand=self.scrollbarX.set)
        #self.text.configure(state=tkinter.DISABLED)
        # self.scrollbar.config(command=self.text.yview)
        self.menubar = Menu(self.text,tearoff=False)
        self.text.bind('<Button-3>', self.popup)
        self.text.bind('<Button-1>', self.unactive)
        # popup menu
        self.popup_menu = Menu(self.text, tearoff = 0)
        # menu_copy = Menu(self.popup_menu)
        self.popup_menu.add_command(label='复制', command=self.copy_log) 
        self.popup_menu.add_command(label='清空', command=self.clear_log) 

        # 设置title的格式
        self.text.tag_configure('title', font=('微软雅黑', 8, 'bold'),foreground='red', justify=LEFT, spacing3=2)
        self.text.tag_configure('title_text', font=('微软雅黑', 8, 'bold'),foreground='red', justify=LEFT, spacing3=2)

        # 设置device info的格式
        self.text.tag_configure('devinfo_title', font=('微软雅黑', 8, 'bold'),foreground='blue', justify=LEFT, spacing3=2)
        self.text.tag_configure('devinfo', font=('微软雅黑', 8),foreground='blue', justify=LEFT, spacing3=2)

        # 设置普通log的格式
        '''
        self.text.tag_configure('detail', foreground='black',
                                font=('微软雅黑', 11, 'bold'),
                                spacing2=10,  # 设置行间距
                                spacing3=15,lmargin2=40)  # 设置段间距
                                '''
        self.text.tag_configure('detail', foreground='gray',font=('微软雅黑', 8),lmargin2=0, spacing3=2)  # 设置段间距
        self.text.tag_configure('fail', foreground='red',font=('微软雅黑', 8),lmargin2=0, spacing3=2)  # 设置段间距
        self.text.tag_configure('pass', foreground='green',font=('微软雅黑', 8),lmargin2=0, spacing3=2)  # 设置段间距
        # 设置特殊log的格式

        # self.text.insert(END, common.getCurTime() + '  ' +
        #                  "当前为内网升级，请输入待升级设备的IP，点击确定，升级过程会自动进行！\n")


    def gui_arrang(self):
        # 文本显示框放在上面
        self.text.pack(side=LEFT, fill=BOTH, padx=10, pady=10, expand=YES)
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=NO)
        self.scrollbarX.pack(side=BOTTOM, fill=X, expand=NO)

        # 操作区放在下面
        self.operateFrame.pack(side=const.TOP, padx=10, pady=10, fill=const.X, expand=const.NO, anchor=const.N)
        
        self.sshFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.sshLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.sshDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.sshSystemCombo.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.sshTypeCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.sshSubmitButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.apiFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.apiLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.apiDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.apiUrlCombo.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.apiMethodCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.apiBodyEntry.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        #self.apiScrollbar.pack(side=RIGHT, expand=NO)
        self.apiTokenCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.apiSubmitButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.sysFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.sysLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.sysDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.sysUserEntry.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.sysLnameCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.sysStorageCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.sysSubmitButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.sysStopButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.base64Frame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.toBase64Label.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.toBase64PathEntry.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.toBase64SelectButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.toBase64SubmitButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.base64toLabel.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.base64toPathEntry.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.base64toSelectButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.base64toSubmitButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)


        self.dataFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.dataLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.dataDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.dataOpenApiButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataCloseApiButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataCheck1.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataCheck2.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.dataCheck3.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.dataCheck4.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataFrame2.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.dataLabel2.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.dataPathEntry.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataPathButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataNumEntry.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.dataButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.faceFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.faceLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.facePathEntry.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.facePathButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.faceCombo.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.faceButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.faceFrame2.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.faceLabel2.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.facePathEntry2.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.facePathButton2.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.faceCombo2.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.faceButton2.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.alertFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.alertLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.alertDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.alertPathEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.alertPathButton.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.alertCombo.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.alertNumEntry.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)
        self.alertButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.channelFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.channelLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.channelDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.channelIdEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.channelCombo.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.channelNumEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.channelButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.repoFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.repoLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.repoDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.repoFaceIdEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.repoVehicleIdEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.repoCombo.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.repoNumEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.repoButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)

        self.taskFrame.pack(side=const.TOP, padx=5, pady=0, fill=const.X, expand=const.NO, anchor=const.N)
        self.taskLabel.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.taskDeviceIpCombo.pack(side=const.LEFT,padx=5, pady=0, expand=const.NO)
        self.taskIdEntry.pack(side=const.LEFT, padx=5,pady=0, expand=const.NO)
        self.taskButton.pack(side=const.LEFT, padx=5, pady=0, expand=const.NO)




    def popup(self, event) :
        # print ("text recv event:", event)
        self.popup_menu.post(event.x_root, event.y_root)
    def unactive(self, event) :
        self.popup_menu.unpost()
    def copy_log(self) :
        # print("sel first=", SEL_FIRST, ", sel last=", SEL_LAST)
        # print("select:", self.text.get(SEL_FIRST, SEL_LAST))
        self.text.clipboard_clear()
        self.text.clipboard_append(self.text.get(SEL_FIRST, SEL_LAST))
    def clear_log(self):
        self.text.delete(1.0, END)
    def sshDef(self): 
        toolProc.thread_it(toolProc.sshDef, (self.sshDeviceIpCombo.get(),self.text_cb, self.sshSystemCombo.get(),self.sshTypeCombo.get()))
        getConfig.setList(self.sshDeviceIpCombo.get(),'ipList.txt')
    def apiDef(self):
        toolProc.thread_it(toolProc.apiDef, (self.apiDeviceIpCombo.get(),self.text_cb, self.apiUrlCombo.get(),self.apiMethodCombo.get(),self.apiBodyEntry.get(),self.apiTokenCombo.get()))
        getConfig.setList(self.apiDeviceIpCombo.get(),'ipList.txt')
        getConfig.setList(self.apiUrlCombo.get(),'urlList.txt')
    def sysDef(self):
        toolProc.thread_it(toolProc.sysDef, (self.sysDeviceIpCombo.get(),self.text_cb, self.sysUserEntry.get(),self.sysLnameCombo.get(),self.sysStorageCombo.get()))
        getConfig.setList(self.sshDeviceIpCombo.get(),'ipList.txt')
    def sysStopDef(self):
        toolProc.thread_it(toolProc.sysStopDef, (self.sysDeviceIpCombo.get(),self.text_cb))
        #self.UpgradeWin.destroy()
        #self.__init__()
        #self.UpgradeWin.geometry('1080x600')
        #self.UpgradeWin.resizable(False, False)
        #self.gui_arrang()
    def toBase64SelectImageDef(self):
        self.toBase64PathVar.set(filedialog.askopenfilename())
    def base64toSelectImageDef(self):
        self.base64toPathVar.set(filedialog.askopenfilename())
    def toBase64Def(self):
        toolProc.thread_it(toolProc.toBase64Def, (self.toBase64PathEntry.get(),self.text_cb))
    def base64toDef(self):
        toolProc.thread_it(toolProc.base64toDef, (self.base64toPathEntry.get(),self.text_cb))
    def dataOpenApi(self):
        toolProc.thread_it(toolProc.dataOpenApi, (self.dataDeviceIpCombo.get(),self.text_cb))
        getConfig.setList(self.sshDeviceIpCombo.get(),'ipList.txt')
    def dataCloseApi(self):
        toolProc.thread_it(toolProc.dataCloseApi, (self.dataDeviceIpCombo.get(),self.text_cb))
        getConfig.setList(self.sshDeviceIpCombo.get(),'ipList.txt')
    def dataCapture(self):
        toolProc.thread_it(toolProc.dataCapture, (self.dataDeviceIpCombo.get(),self.dataCheckVar1.get(),self.dataCheckVar2.get(),self.dataCheckVar3.get(),self.dataCheckVar4.get(),self.dataPathEntry.get(),self.dataNumEntry.get(),self.text_cb))
    def dataPathCapture(self):
        self.dataPathVar.set(filedialog.askdirectory())
    def facePathCapture(self):
        self.facePathVar.set(filedialog.askdirectory())
    def facePathCapture2(self):
        self.facePathVar2.set(filedialog.askdirectory())
    def pedestrianPathCapture(self):
        self.pedestrianPathVar.set(filedialog.askdirectory())
    def vehiclePathCapture(self):
        self.vehiclePathVar.set(filedialog.askdirectory())
    def bicyclePathCapture(self):
        self.bicyclePathVar.set(filedialog.askdirectory())
    def alertPathCapture(self):
        self.alertPathVar.set(filedialog.askdirectory())
    def face(self):
        toolProc.thread_it(toolProc.face, (self.facePathVar.get(),self.faceCombo.get(),self.text_cb))
    def face2(self):
        toolProc.thread_it(toolProc.face2, (self.facePathVar2.get(),self.faceCombo2.get(),self.text_cb))
    def alert(self):
        toolProc.thread_it(toolProc.alert, (self.alertPathVar.get(),self.alertDeviceIpCombo.get(),self.alertCombo.get(),self.alertNumEntry.get(),self.text_cb))
        getConfig.setList(self.alertDeviceIpCombo.get(),'ipList.txt')
    def channel(self):
        toolProc.thread_it(toolProc.channel, (self.channelDeviceIpCombo.get(),self.channelIdEntry.get(),self.channelCombo.get(),self.channelNumEntry.get(),self.text_cb))
    def repo(self):
        toolProc.thread_it(toolProc.repo, (self.repoDeviceIpCombo.get(),self.repoFaceIdEntry.get(),self.repoVehicleIdEntry.get(),self.repoCombo.get(),self.repoNumEntry.get(),self.text_cb))
        getConfig.setList(self.repoDeviceIpCombo.get(),'ipList.txt')
    def task(self):
        toolProc.thread_it(toolProc.task, (self.taskDeviceIpCombo.get(),self.taskIdEntry.get(),self.text_cb))
        getConfig.setList(self.taskDeviceIpCombo.get(),'ipList.txt')
    def text_cb(self, str, format=None):
        self.text.insert(END, time.strftime('%H:%M:%S  ')+str, format)
        self.text.see(END)
    def setGUI(self):
        self.UpgradeWin.geometry('1080x600')
        #self.UpgradeWin.resizable(False, False)
        #self.gui_arrang()
    def thread_it(func, args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    
def runUI():
    L = toolUI()
    L.gui_arrang()
    mainloop()   
if __name__ == '__main__':
    #runUI()
    
    proc=os.popen('netstat -ano |findstr "8888"').read()
    pidStrs=proc.split('\n')
    for pidStr in pidStrs:
        os.popen('taskkill /f /pid %s' % pidStr.split(' ')[-1]+'"')
    p1 = Process(target=runUI)
    p1.start()
    p = Process(target=event.event)
    p.start()
    

    

