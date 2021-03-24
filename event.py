#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import signal
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import base64
import uuid
import time

faceFlag='0'
faceNum=0
faceList=[]
pedestrianFlag='0'
pedestrianNum=0
pedestrianList=[]
vehicleFlag='0'
vehicleNum=0
vehicleList=[]
bicycleFlag='0'
bicycleNum=0
bicycleList=[]
path=''
flag=0

class EeventServerHandler(tornado.web.RequestHandler):
    
    def post(self):
        global faceFlag 
        global faceNum 
        global pedestrianFlag 
        global pedestrianNum 
        global vehicleFlag 
        global vehicleNum 
        global bicycleFlag 
        global bicycleNum 
        global path
        global flag
        global faceList 
        global pedestrianList
        global vehicleList
        global bicycleList 
        r = json.loads(self.request.body.decode('utf-8'))

        if ('eventType' in r.keys()) and  r['eventType'] == 114:
            if (not os.path.exists(path+'/face')and(faceFlag=='1')):
                os.mkdir(path+'/face')
            if (not os.path.exists(path+'/data')and(faceFlag=='1')):
                os.mkdir(path+'/data')
            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【陌生人事件】'+str(r['eventTime']))
            for i in range(0,len(r['eventDetail']['images'])):
                if 'data' in r['eventDetail']['images'][i] and r['eventDetail']['images'][i]['picType']=='face' and flag==1:
                    with open(path+'/face/'+r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg', 'wb') as f:
                        f.write(base64.b64decode(r['eventDetail']['images'][i]['data']))
                        faceNum=faceNum+1
                        f.close()
                    temp={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['bbox']=min(r['eventDetail']['faceInfo']['faceRec']['position']['width'],r['eventDetail']['faceInfo']['faceRec']['position']['height'])
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['quality']=r['eventDetail']['faceInfo']['faceRec']['attributes']['isFace']['confidence']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['confidence']=r['eventDetail']['faceInfo']['faceRec']['position']['confidence']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['blur']=r['eventDetail']['faceInfo']['faceRec']['qualities']['blur']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['yaw']=r['eventDetail']['faceInfo']['faceRec']['qualities']['yaw']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['pitch']=r['eventDetail']['faceInfo']['faceRec']['qualities']['pitch']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['roll']=r['eventDetail']['faceInfo']['faceRec']['qualities']['roll']
                    #faceList.append(temp)
                    with open(path+'/data/faceList.txt', 'a+', encoding='utf-8') as f1:
                        f1.write(str(temp)+';' + '\n')
                        f1.close()
            
            print('********************************************************************************************************************')

        elif ('eventType' in r.keys()) and  r['eventType'] == 1010003:
            if (not os.path.exists(path+'/vehicle')and(vehicleFlag=='1')):
                os.mkdir(path+'/vehicle')
            if (not os.path.exists(path+'/data')and(faceFlag=='1')):
                os.mkdir(path+'/data')
            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【机动车事件】'+str(r['eventTime']))
            for i in range(0,len(r['eventDetail']['images'])):
                if 'data' in r['eventDetail']['images'][i] and r['eventDetail']['images'][i]['picType']=='crop' and flag==1:
                    with open(path+'/vehicle/'+r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg', 'wb') as f:
                        f.write(base64.b64decode(r['eventDetail']['images'][i]['data']))
                        vehicleNum=vehicleNum+1
                        f.close()
                    temp={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['bbox']=min(r['eventDetail']['info']['bbox']['width'],r['eventDetail']['info']['bbox']['height'])
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['quality']=r['eventDetail']['info']['quality']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['confidence']=r['eventDetail']['info']['bbox']['confidence']
                    #vehicleList.append(temp)
                    with open(path+'/data/vehicleList.txt', 'a+', encoding='utf-8') as f2:
                        f2.write(str(temp)+';' + '\n')
                        f2.close()
            print('********************************************************************************************************************')
        elif ('eventType' in r.keys()) and  r['eventType'] == 1010004:
            if (not os.path.exists(path+'/pedestrian')and(pedestrianFlag=='1')):
                os.mkdir(path+'/pedestrian')
            if (not os.path.exists(path+'/data')and(faceFlag=='1')):
                os.mkdir(path+'/data')
            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【行人事件】'+str(r['eventTime']))
            for i in range(0,len(r['eventDetail']['images'])):
                if 'data' in r['eventDetail']['images'][i] and r['eventDetail']['images'][i]['picType']=='crop' and flag==1:
                    with open(path+'/pedestrian/'+r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg', 'wb') as f:
                        f.write(base64.b64decode(r['eventDetail']['images'][i]['data']))
                        pedestrianNum=pedestrianNum+1
                        f.close()
                    temp={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['bbox']=min(r['eventDetail']['info']['bbox']['width'],r['eventDetail']['info']['bbox']['height'])
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['quality']=r['eventDetail']['info']['quality']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['confidence']=r['eventDetail']['info']['bbox']['confidence']
                    #pedestrianList.append(temp)
                    with open(path+'/data/pedestrianList.txt', 'a+', encoding='utf-8') as f3:
                        f3.write(str(temp)+';' + '\n')
                        f3.close()
            print('********************************************************************************************************************')
        elif ('eventType' in r.keys()) and  r['eventType'] == 1010005:
            if (not os.path.exists(path+'/bicycle')and(bicycleFlag=='1')):
                os.mkdir(path+'/bicycle')
            if (not os.path.exists(path+'/data')and(faceFlag=='1')):
                os.mkdir(path+'/data')
            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【非机动车事件】'+str(r['eventTime']))
            for i in range(0,len(r['eventDetail']['images'])):
                if 'data' in r['eventDetail']['images'][i] and r['eventDetail']['images'][i]['picType']=='crop' and flag==1:
                    with open(path+'/bicycle/'+r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg', 'wb') as f:
                        f.write(base64.b64decode(r['eventDetail']['images'][i]['data']))
                        bicycleNum=bicycleNum+1
                        f.close()
                    temp={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']={}
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['bbox']=min(r['eventDetail']['info']['bbox']['width'],r['eventDetail']['info']['bbox']['height'])
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['quality']=r['eventDetail']['info']['quality']
                    temp[r['eventTime'].replace(' ', '').replace(':', '').replace('-', '') +'.jpg']['confidence']=r['eventDetail']['info']['bbox']['confidence']
                    #bicycleList.append(temp)
                    with open(path+'/data/bicycleList.txt', 'a+', encoding='utf-8') as f4:
                        f4.write(str(temp)+';' + '\n')
                        f4.close()
            print('********************************************************************************************************************')
        elif ('eventType' in r.keys()) and  r['eventType'] == 1111:
            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【传参事件】')
            faceFlag=r['faceFlag']
            pedestrianFlag=r['pedestrianFlag']
            vehicleFlag=r['vehicleFlag']
            bicycleFlag=r['bicycleFlag']
            path=r['path']
            flag=r['flag']
            print(json.dumps(r, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
            r['code']=200000
            self.write(json.dumps(r))
            print('********************************************************************************************************************')
        elif ('eventType' in r.keys()) and  r['eventType'] == 2222:
            if faceFlag=='0':
                faceNum=-1
            if pedestrianFlag=='0':
                pedestrianNum=-1
            if vehicleFlag=='0':
                vehicleNum=-1
            if bicycleFlag=='0':
                bicycleNum=-1

            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【获取参数事件】')
            self.write(json.dumps({'faceNum': faceNum,'pedestrianNum': pedestrianNum,'vehicleNum': vehicleNum,'bicycleNum': bicycleNum,'path': path,'flag': flag,'code':200000}))
            print('********************************************************************************************************************')
        elif ('eventType' in r.keys()) and  r['eventType'] == 3333:
            faceNum=0
            faceList=[]
            pedestrianNum=0
            pedestrianList=[]
            vehicleNum=0
            vehicleList=[]
            bicycleNum=0
            bicycleList=[]
            flag=0
            print('********************************************************************************************************************')
            print(str(r['eventType'])+'【参数置位事件】')
            self.write(json.dumps({'code':200000}))
            print('********************************************************************************************************************')
        #self.write(json.dumps({'data': 'asdf1234567890'}))


def on_kill(*_):
    tornado.log.app_log.info('progress stop')
    os._exit(0)


#if __name__ == '__main__':
def event():

    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, on_kill)
    app = tornado.web.Application([('.*', EeventServerHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.log.app_log.info('start listen on 8888')
    tornado.ioloop.IOLoop.current().start()
