import requests
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.pyplot import MultipleLocator,savefig
import requests.exceptions as exceptions
import traceback
import json

def getAlert(ip,pageSize,text_cb):
    text_cb(ip+' 人脸报警处理开始......\n', 'detail')
    try:
        flag=True
        if ':' in ip:
            rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/a/login', json={'username': 'admin', 'password': 'B32FA6018771638F277F0BE418708C10'})
            result=requests.get(url='http://'+ip+'/api/alert?pageSize='+str(pageSize),
                                headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        else :
            rLogin=requests.post(url='http://'+ip.split(':')[0]+'/api/login', json={'userName': 'admin', 'password': '27a3388aedc1dfaa7a94e7223a0fa1c1'})
            result=requests.get(url='http://'+ip+'/api/alert?pageSize='+str(pageSize),
                                headers={'Content-Type':'application/json;charset=utf-8','Authorization':rLogin.json()['data']['token']})
        if result.json()['code']==200000:
            results=json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            #text_cb('\n'+results+'\n', 'pass')
        else:
            results=json.dumps(json.loads(results.text), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
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
        text_cb(ip+' '+ErroResult+'   \n', 'fail')
    return result.json()['data']
    
def processAlert(ip,alertData,names,flag,path,text_cb):
    strangerData=[]
    isData=[]
    for i in alertData:
        if i['faceName'] in names:
            isData.append(float(i['score']))
        else:
            strangerData.append(float(i['score']))

    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    
    x1 = isData
    # 通过切片获取纵坐标R
    y1 = x1

    # 横坐标x2
    x2 = strangerData
    # 纵坐标y2
    y2 = strangerData
    # 创建画图窗口
    fig = plt.figure()
    # 将画图窗口分成1行1列，选择第一块区域作子图
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.grid()
    # 设置标题
    #ax1.set_title('识别')
    # 设置横坐标名称
    ax1.set_xlabel('分数区间')
    # 设置纵坐标名称
    ax1.set_ylabel('识别分数')
    # 画散点图
    ax1.scatter(x1, y1, s=40,c='g', marker='.')
    ax1.scatter(x2, y2,s=15, c='r', marker='.')
    # 画直线图
    #ax1.plot(x1, y1,c='y',ls='-',linewidth=0.1, mfc='w')
    # 调整横坐标的上下界
    #plt.legend('x1')
    #plt.legend('x2') 
    # 显示
    x_major_locator=MultipleLocator(1)
    #把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator=MultipleLocator(1)
    #把y轴的刻度间隔设置为10，并存在变量里
    ax=plt.gca()
    #ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    #把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    
    if not os.path.exists(path+'/result/alert/'):
        os.makedirs(path+'/result/alert/')   
    savefig(path+'/result/alert/'+flag+'.png')
    text_cb(ip+'人脸报警分数折线图绘制完成，保持路径为：'+path+'/result/alert/'+flag+'.png    \n', 'pass')
            
        


def alert(path,ip,flag,pageSize,text_cb):

    if flag=='output104':
        name=['黄严','王涛','冯印国','游玉兰','李潇','胡海云','李梦楠','孙泽平','王子实','张东萍',
                  '单相振','李超','孙子夕','李瑶晗','崔鸿华','陈甜甜','董志','车颖飞','王一舒','申新静',
                  '周玉腾','刘彤','赵云飞','安其立','于丽霞','邓亚锋','连姣','洪晓威','李兴华','王攀佳','陈计云']
    if flag=='output106':
        name=['秦斌','李璇','董志','连钊','冯建帅','王涛','沈冰然','李瑶晗','孙子夕','晏冉','孙泽平','李雨恒',
                  '张诚','郭新彩','胡海云','孙启昌','单相振','张星','乌兰','陈甜甜','王子实','王一舒','车颖飞',
                  '游玉兰','洪晓威','连姣','刘彤','邓亚峰','陈计云','张晓垒','王志洋','张亚男','沈传刚','姚觐']
    if flag=='output107':
        name=['王萧乐','邓亚锋','李秋彦','沈冰然','王攀佳','于丽霞','李家丞','冯子勇','郭丽凯','张星',
                  '王雨萌','李梦楠','连钊','车颖飞','胡开先','胡泽琛','秦慧莹','晏冉','郭邵萍','孙景润',
                  '张亚男','张德兵','李红将','狄烨','孙志成','王一舒','宋剑飞']
    if flag=='outputSH':  
        name=['陈鸿志','何志飞','陈振雄','赵志洲','邓高峰','周叶飞','张治安',
                 '张召','殷俊','赵康','李海峰','李兴华','张琦','陈鑫元','孙健永']
    alertData=getAlert(ip,pageSize,text_cb)
    processAlert(ip,alertData,name,flag,path,text_cb)
    
    
    
