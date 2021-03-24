import paramiko
import time
import numpy as np
import matplotlib.pyplot as plt
import _thread
from matplotlib.pyplot import MultipleLocator
import matplotlib
matplotlib.use("Qt5agg")
import threading
import gc 
global printRun
#global fig

def getdataHardDiskStorage(ssh,flags,storage):
    try:
        stdin,stdout,stderr = ssh.exec_command("df -h")
        #print(stdout.readlines())
        sss=stdout.readlines()
        flag=False
        for ss in sss:
            if storage in ss:
                s=ss.split()[4][:-1]
                flag=True
        if flag==False:
            s=-10
        #s=float((stdout.readlines()[2]).split()[4][:-1])
    except:
        s=-10
    return float(s)

def getdataMemory(ssh,flags):
    try:
        stdin,stdout,stderr = ssh.exec_command("free -m")
        #print(stdout.readlines())
        ss=stdout.readlines()
        total=float((ss[1]).split()[1])
        memory=float((ss[1]).split()[6])
        s=total-memory
    except:
        s=-10
    return s
def getdataAppL(ssh,flags,Lname):
    try:
        stdin,stdout,stderr = ssh.exec_command("top -b -n 1")
        #print(stdout.readlines())
        sss=stdout.readlines()
        flag=False
        for s in sss:
            if Lname in s:#DEH5Bin MainThread
                s1=s.split()[8]
                s2=s.split()[9]
                flag=True
        if flag==False:
            s1=-10
            s2=-10
    except:
        s1=-10
        s2=-10
    return [float(s1),float(s2)]
def getdataAppT(ssh,flags):
    try:
        stdin,stdout,stderr = ssh.exec_command("top -b -n 1")
        #print(stdout.readlines())
        sss=stdout.readlines()
        flag=False
        for s in sss:
            if 'libra' in s:
                s1=s.split()[8]
                s2=s.split()[9]
                flag=True
        if flag==False:
            s1=-10
            s2=-10
    except:
        s1=-10
        s2=-10
    return [float(s1),float(s2)]

def getTemperature(ssh,flags):
    try:
        stdin,stdout,stderr = ssh.exec_command("cat /sys/class/thermal/thermal_zone0/temp")
        #print(stdout.readlines())
        s1=float(stdout.readlines()[0])/1000
        #print(sss)
    except:
        s1=-10
    return float(s1)
def getOtherLog(ssh,file_path):

    fp1 = open(file_path+"free.log", 'a')
    stdin1,stdout1,stderr1=ssh.exec_command("free -m") 
    s1=stdout1.read()
    s1=str(s1)
    s1=s1.replace('\n','\r\n')
    fp1.write(time.strftime("%H:%M:%S")+"\n"+s1+"\n")
    fp1.close()
    
    
    fp2 = open(file_path+"top.log", 'a')
    stdin2,stdout2,stderr2=ssh.exec_command("top -n 1") 
    s2=stdout2.readlines()[0:2]
    s2=str(s2)
    s2=s2.replace('\n','\r\n')
    fp2.write(time.strftime("%H:%M:%S")+"\n"+s2+"\n")
    fp2.close()
    

    fp3 = open(file_path+"ps.log", 'a')    
    stdin3,stdout3,stderr3=ssh.exec_command("ps -a") 
    s3=stdout3.read()
    s3=str(s3)
    s3=s3.replace('\n','\r\n')
    fp3.write(time.strftime("%H:%M:%S")+"\n"+s3+"\n")
    fp3.close()

    fp4 = open(file_path+"meminfo.log", 'a')    
    stdin4,stdout4,stderr4=ssh.exec_command("cat /proc/meminfo") 
    s4=stdout4.read()
    s4=str(s4)
    s4=s4.replace('\n','\r\n')
    fp4.write(time.strftime("%H:%M:%S")+"\n"+s4+"\n")
    fp4.close()
    
def printPlot(times,datas,axs,flags):
    axs[0].cla()
    axs[0].set_title(flags)
    axs[0].set_ylabel("Storage(%)")

    axs[1].cla()
    axs[1].plot(times, datas[1],c='b',ls='-',linewidth=0.3, mfc='w')
    axs[1].set_ylabel("Memory(M)")
    axs[1].set_xticks([])
    #ax2.grid()

    #print(dataAppMemorys)
    axs[2].cla()
    axs[2].plot(times, datas[2],c='g',ls='-',linewidth=0.3, mfc='w')
    axs[2].set_ylabel("L Memory(%)")
    axs[2].set_xticks([])
    #ax3.grid()

    axs[4].cla()
    axs[4].plot(times, datas[3],c='purple',ls='-',linewidth=0.3, mfc='w')
    axs[4].set_ylabel("L CPU(%)")
    axs[4].set_xticks([])
    #ax4.grid()
    #plt.xticks(range(0,len(times),int(len(times)/20)+1),rotation=45,fontsize=7)

    axs[3].cla()
    axs[3].plot(times, datas[4],c='g',ls='-',linewidth=0.3, mfc='w')
    axs[3].set_ylabel("T Memory(%)")
    axs[3].set_xticks([])
    #ax3.grid()

    axs[5].cla()
    axs[5].plot(times, datas[5],c='purple',ls='-',linewidth=0.3, mfc='w')
    axs[5].set_ylabel("T CPU(%)")
    axs[5].set_xticks([])
    
    axs[6].cla()
    axs[6].plot(times, datas[6],c='y',ls='-',linewidth=0.3, mfc='w')
    axs[6].set_ylabel("Temperature(℃)")
    #ax4.set_xlabel("time")
    #ax5.grid()
    #ax4.set_xticks([])

    ############## | 新增时需要修改
    
    axs[0].plot(times, datas[0],c='r',ls='-',linewidth=0.3, mfc='w')
    axs[0].set_xticks([])
    #ax1.grid()
    
    plt.xticks(range(0,len(times),int(len(times)/20)+1),rotation=45,fontsize=7)
    #plt.grid()
    plt.pause(10)
def loops(ip,username,password,axs,flags,Lname,storage,text_cb):
    print('stop 4')
    dataHardDiskStorages=[]
    times=[]
    dataMemorys=[]
    dataAppMemorys=[]
    dataAppCPUs=[]
    dataAppTMemorys=[]
    dataAppTCPUs=[]
    dataTemperatures=[]
    ##############新增时需要修改
    global printRun
    while printRun:
        print('stop 5')
        try:
            print('stop 6')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,22,username,password)
        except:
            pass
        print('stop 7')
        dataHardDiskStorage=getdataHardDiskStorage(ssh,flags,storage)
        dataMemory=getdataMemory(ssh,flags)
        [dataAppCPU,dataAppMemory]=getdataAppL(ssh,flags,Lname)
        [dataAppTCPU,dataAppTMemory]=getdataAppT(ssh,flags)
        dataTemperature=getTemperature(ssh,flags)
        ##############新增时需要修改
        ssh.close()
        print('stop 8')
        text_cb(ip+' 存储：'+str(dataHardDiskStorage)+'%  内存：'+str(dataMemory)+'M  L内存：'+
              str(dataAppMemory)+'%  T内存：'+str(dataAppTMemory)+'%  L CPU：'+str(dataAppCPU)+
              '%  T CPU：'+str(dataAppTCPU)+'%  温度：'+str(dataTemperature)+'℃   \n', 'detail')
        
        #getOtherLog(ssh,file_path)
        print('stop 9')
        times.append(time.strftime("%m.%d %H:%M:%S"))
        dataHardDiskStorages.append(dataHardDiskStorage)
        dataMemorys.append(dataMemory)
        dataAppMemorys.append(dataAppMemory)
        dataAppCPUs.append(dataAppCPU)
        dataAppTMemorys.append(dataAppTMemory)
        dataAppTCPUs.append(dataAppTCPU)
        dataTemperatures.append(dataTemperature)
        ##############新增时需要修改
        print('stop 10')
        datas=[dataHardDiskStorages,dataMemorys,dataAppMemorys,dataAppCPUs,dataAppTMemorys,dataAppTCPUs,dataTemperatures]##############新增时需要修改
        
        printPlot(times,datas,axs,flags)
        print('stop 11')
    plt.close('all')
    print('stop 12')
    gc.collect()
    print('stop 13')

def login_run(ip,text_cb,user,Lname,storage,imageNumber):
    print('stop 2')
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(ip,22,username,password)
    username=user.split('/')[0]
    password=user.split('/')[1]
    flags=ip+" monitor"
    #plt.close('all')
    plt.ion()
    print('stop 21')
    #global fig
    #fig = plt.figure()
    plt.close('all')
    print('stop 22')
    fig = locals()
    #plt.close(fig['fig%s' % imageNumber])
    fig['fig%s' % imageNumber]  = plt.figure(num=imageNumber)
    print('stop 23')
    ax1 = fig['fig%s' % imageNumber].add_subplot(7,1,1)
    ax2 = fig['fig%s' % imageNumber].add_subplot(7,1,2)
    ax3 = fig['fig%s' % imageNumber].add_subplot(7,1,3)
    ax4 = fig['fig%s' % imageNumber].add_subplot(7,1,4)
    ax5 = fig['fig%s' % imageNumber].add_subplot(7,1,5)
    ax6 = fig['fig%s' % imageNumber].add_subplot(7,1,6)
    ax7 = fig['fig%s' % imageNumber].add_subplot(7,1,7)
    print('stop 24')
    ##############新增时需要修改

    axs=[ax1,ax2,ax3,ax4,ax5,ax6,ax7]##############新增时需要修改
    global printRun
    printRun=True
    print('stop 3')
    loops(ip,username,password,axs,flags,Lname,storage,text_cb)

  

    #login_run("172.17.0.6","ubuntu","On1shiuva4","172.17.0.6 monitor","D:\\work\\皓目L\\log\\")
    #login_run("172.17.0.36","root","On1shiuva4","172.17.0.36 monitor","D:\\work\\皓目L\\log\\")
    #login_run("172.17.0.144","root","On1shiuva4","HaomuF 144 monitor")
def login_stop(imageNumber):
    print('stop 1')
    global printRun
    #global fig
    printRun=False
    #plt.close('all')
    #plt.close()
def thread_it(func, args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

