import os
import threading
import time
from multiprocessing import Process

def my():
    while True:
        print('子进程')
        time.sleep(1)

'''
if __name__ == '__main__':
    print('主进程已启动')
    p = Process(target=my)
    p.start()
    while True:
        print('主进程')
        time.sleep(1)
'''
def thread_it(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()
def runEvent():
    os.system('event.py')
def runUI():
    os.system('toolUI.py')
if __name__ == '__main__':
    runUI()
    #p = Process(target=runEvent)
    #p.start()
    #p.join()
    
    #thread_it(runEvent)
    #thread_it(runUI)
