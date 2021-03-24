import os
import requests
import base64
from urllib import parse,request
import shutil
import time
import cv2
import numpy
import matplotlib.pyplot as plt
import math
from PIL import Image
import json

def getRawData(urls,methods,tokens):
    Headers='application/json;charset=utf-8'
    result = requests.request(methods,url=urls,headers={'Content-Type':Headers,'Authorization':tokens})
    return result.json()['data']
def sortSDK(datas):
    sortSdkData=sorted(datas.items(),key=lambda x:x[1])
    return sortSdkData
def getResult(data,flag):
    width_i = 100
    height_i = 100
    line_row_max=math.ceil( math.sqrt(len(data)))
    toImage = Image.new('RGBA',(width_i*line_row_max,height_i*line_row_max))
    index=0
    for ii in data:
        img0=cv2.imread('./images/'+flag+'/'+ii[0])
        xx=index%line_row_max
        yy=int(index/line_row_max)
        img1 = cv2.resize(img0, (width_i,height_i), interpolation=cv2.INTER_AREA)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img2 = cv2.putText(img1, str(round(ii[1],5)), (2,15), font,0.5, (0,255,0), 1)
        loc = (int((xx%line_row_max)*width_i),int((yy%line_row_max)*height_i))
        img2 = Image.fromarray(cv2.cvtColor(img2,cv2.COLOR_BGR2RGB))
        toImage.paste(img2,loc)
        index=index+1
    toImage.save('./result/'+flag+'.png')

def proceData(dataAll):
    All={}
    Size={}
    Is_face={}
    Age={}
    Blur={}
    Gender={}
    Hat={}
    Glass={}
    Helmet={}
    SunGlass={}
    Mask={}
    Pitch={}
    Yaw={}
    Roll={}
    Hood={}
    for i in dataAll.keys():
        Size[i]=dataAll[i]['faceRec']['position']['width']
        Is_face[i]=dataAll[i]['faceRec']['attributes']['isFace']['value']
        Age[i]=dataAll[i]['faceRec']['attributes']['age']['value']
        Blur[i]=dataAll[i]['faceRec']['qualities']['blur']
        
        if dataAll[i]['faceRec']['attributes']['gender']['value']==1:
            Gender[i]=dataAll[i]['faceRec']['attributes']['gender']['confidence']*-1
        elif dataAll[i]['faceRec']['attributes']['gender']['value']==2:
            Gender[i]=dataAll[i]['faceRec']['attributes']['gender']['confidence']
            
        if dataAll[i]['faceRec']['attributes']['hat']['value']==1:
            Hat[i]=dataAll[i]['faceRec']['attributes']['hat']['confidence']*-1
            Hood[i]=dataAll[i]['faceRec']['attributes']['hat']['confidence']*-1
        elif dataAll[i]['faceRec']['attributes']['hat']['value']==2:
            Hat[i]=dataAll[i]['faceRec']['attributes']['hat']['confidence']
            Hood[i]=0
        elif dataAll[i]['faceRec']['attributes']['hat']['value']==3:
            Hat[i]=0
            Hood[i]=dataAll[i]['faceRec']['attributes']['hat']['confidence']

        if dataAll[i]['faceRec']['attributes']['glass']['value']==1:
            Glass[i]=dataAll[i]['faceRec']['attributes']['glass']['confidence']*-1
            SunGlass[i]=dataAll[i]['faceRec']['attributes']['glass']['confidence']*-1
        elif dataAll[i]['faceRec']['attributes']['glass']['value']==2:
            Glass[i]=dataAll[i]['faceRec']['attributes']['glass']['confidence']
            SunGlass[i]=0
        elif dataAll[i]['faceRec']['attributes']['glass']['value']==3:
            Glass[i]=0
            SunGlass[i]=dataAll[i]['faceRec']['attributes']['glass']['confidence']

        if dataAll[i]['faceRec']['attributes']['mask']['value']==1:
            Mask[i]=dataAll[i]['faceRec']['attributes']['mask']['confidence']*-1
        elif dataAll[i]['faceRec']['attributes']['mask']['value']==2:
            Mask[i]=dataAll[i]['faceRec']['attributes']['mask']['confidence']
            
        Pitch[i]=dataAll[i]['faceRec']['qualities']['pitch']
        Yaw[i]=dataAll[i]['faceRec']['qualities']['yaw']
        Roll[i]=dataAll[i]['faceRec']['qualities']['roll']
        All['size']=Size
        All['isFace']=Is_face
        All['age']=Age
        All['blur']=Blur
        All['gender']=Gender
        All['hat']=Hat
        All['glass']=Glass
        All['sunGlass']=SunGlass
        All['mask']=Mask
        All['pitch']=Pitch
        All['yaw']=Yaw
        All['roll']=Roll
        All['hood']=Hood
    return All
        
def getCutImage(path,dataAll):
    pathBase=os.path.dirname(path)
    if not os.path.exists(pathBase+'\\result\\Cut'):
        os.makedirs(pathBase+'\\result\\Cut')
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file in dataAll.keys():
                continue
            #dataAll[file]=data['faceInfo']
            position=dataAll[file]['faceRec']['position']
            print(position)
            img = cv2.imread(path+'//'+file)
            x=int(position["x"])
            y=int(position["y"])
            w=int(position["width"])
            h=int(position["height"])
            imgCut=img[y:y+w,x:x+h]
            if h<100 and w<100:
                imgCut = cv2.copyMakeBorder(imgCut, 100-w, 100-w, 100-h, 100-h, cv2.BORDER_CONSTANT, value=[0,0,0])
            cv2.imwrite(pathBase+'\\result\\Cut\\'+file, imgCut)
    
    
def getAttributesImage(name,data,path):
    width_i = 100
    height_i = 100
    line_row_max=math.ceil( math.sqrt(len(data.keys())))
    pathBase=os.path.dirname(path)

    dataSort=sorted(data.items(),key=lambda x:x[1])
    #print(dataSort)
    toImage = Image.new('RGBA',(width_i*line_row_max,height_i*line_row_max))
    index=0
    for ii in dataSort:
        img0=cv2.imread(pathBase+'\\result\\Cut\\'+ii[0])
        xx=index%line_row_max
        yy=int(index/line_row_max)
        img1 = cv2.resize(img0, (width_i,height_i), interpolation=cv2.INTER_AREA)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img2 = cv2.putText(img1, str(round(ii[1],5)), (20,120), font,5, (0,255,0), 10)
        loc = (int((xx%line_row_max)*width_i),int((yy%line_row_max)*height_i))
        img2 = Image.fromarray(cv2.cvtColor(img2,cv2.COLOR_BGR2RGB))
        toImage.paste(img2,loc)
        index=index+1
    toImage.save(pathBase+'\\result\\'+name+'.png')
    
if __name__ == "__main__":
    '''
    ip='88.company-remilia.freeddns.org:18180'
    path='D:\\work\haomuL2\\全目标\性能测试\\test\\1586935062251'
    attribute=["Cut","Size","Is_face","Age","Blur","Gender","Hat","Glass","Pitch","Yaw","Roll"]
    imageUrl='http://'+ip+'/api/face/feature'
    #getFeature(ip,path)
    dataAll=getData(path,'result.txt')
    All=proceData(dataAll)
    getCutImage(path,dataAll)
    for i in All.keys():
        getAttributesImage(i,All[i],path)
    '''
    ip='172.17.0.6:8080'
    urls='http://'+ip+'/api/passHistory?pageSize=500&channelIDs=1'
    keys= 'faceImagePath'
    flag='yaw'# blur quality pitch roll yaw
    
    methods='get'
    rawData=getRawData(urls,methods,getToken(ip))
    saveImage(rawData,keys,ip,flag)
    jsonData=getJsonData(rawData,keys,flag)
    sortSdkData=sortSDK(jsonData)
    getResult(sortSdkData,flag)
    

    
