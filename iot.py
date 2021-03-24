import tkinter  

from tkinter import messagebox
from tkinter import Frame
import tkinter.font as tf
from tkinter import ttk
from verifyAccount import verifyAccountData
from tkinter import *

  

class iotManage(object):  

    def __init__(self):  

        # 创建主窗口,用于容纳其它组件  

        self.rootIOT = tkinter.Toplevel()
        #self.rootIOT = tkinter.Tk()
        self.rootIOT.resizable(False,False)
        self.rootIOT.title("IOT服务器管理")
        #center_window(self.rootIOT)
        #w = self.rootIOT.winfo_screenwidth()
        #h = self.rootIOT.winfo_screenheight()
        #self.rootIOT.geometry("%dx%d" %(w,h))
        #self.rootIOT.attributes("-topmost",True)
        #self.rootIOT.geometry('400x500')
        #w, h = self.rootIOT.maxsize()
        #self.rootIOT.geometry("{}x{}".format(w, h))
        #self.rootIOT.minsize(400, 500)
        #self.rootIOT.maxsize(400, 500)
        #self.rootIOT.overrideredirect(True)

        #控件，标签，图像
        self.image_file = tkinter.PhotoImage(file='pic/deepglintIOT.gif')#加载图片文件  
        self.label_image = tkinter.Label(self.rootIOT, image=self.image_file)

        #控件，标签，标题
        self.ft=tf.Font(family='微软雅黑', size=20)  #("Times, 15") 
        self.label_title = tkinter.Label(self.rootIOT, text='IOT服务器管理',font=self.ft,fg = "#b22c46") 

        #控件，标签，IOT属性
        self.label_k = tkinter.Label(self.rootIOT)
        self.label_name = tkinter.Label(self.rootIOT, text='名称')
        self.label_ip = tkinter.Label(self.rootIOT, text='IP')
        self.label_port = tkinter.Label(self.rootIOT, text='端口号')
        self.label_username = tkinter.Label(self.rootIOT, text='用户名')
        self.label_password = tkinter.Label(self.rootIOT, text='密码')

        #控件，标签，添加IOT
        self.label_add = tkinter.Label(self.rootIOT, text='添加服务器')
        self.add_input_name = tkinter.Entry(self.rootIOT,width=15)
        self.add_input_ip = tkinter.Entry(self.rootIOT,width=15)
        self.add_input_port = tkinter.Entry(self.rootIOT,width=15)
        self.add_input_username = tkinter.Entry(self.rootIOT,width=15)
        self.add_input_password = tkinter.Entry(self.rootIOT,width=15)  
        self.add_label_button = tkinter.Button(self.rootIOT, text='保存')

        #控件，标签，留白
        self.label_k2 = tkinter.Label(self.rootIOT)

        #控件，按钮，查看服务器、刷新
        self.view_label= tkinter.Label(self.rootIOT, text='查看服务器')
        #self.view_label_button = tkinter.Button(self.rootIOT, text='刷新')
        
        #控件，标签，留白
        self.label_k3 = tkinter.Label(self.rootIOT)

        #Treeview，查看IOT信息
        columns = ("名称","IP",'端口号','用户名','密码')
        self.treeview = ttk.Treeview(self.rootIOT, show="headings", columns=columns)
        #self.vsb = ttk.Scrollbar(orient="vertical",command=self.treeview.yview)
        #self.treeview.configure(yscrollcommand=self.vsb.set)
        self.treeview.column("名称",  anchor='center')
        self.treeview.column("IP",anchor='center')
        self.treeview.column("端口号",  anchor='center')
        self.treeview.column("用户名",  anchor='center')
        self.treeview.column("密码",  anchor='center')
        #self.treeview.column(" ",  anchor='center')
        self.treeview.heading("名称", text="名称")
        self.treeview.heading("IP", text="IP")
        self.treeview.heading("端口号", text="端口号")
        self.treeview.heading("用户名", text="用户名")
        self.treeview.heading("密码", text="密码")
        self.treeview.bind('<3>', self.rightClick)
        #self.treeview.heading(" ", text=" ")
        #self.checkButton=tkinter.Checkbutton(self.rootIOT)
        #ttk.Style().configure("Treeview", background="#383838",foreground="red")
        #ttk.Style().configure("Treeview.Heading",background = "blue",foreground="Black")


        #Treeview，输入IOT信息
        #button_refresh_treeview.grid(row=1, column=2,padx=10,pady=10,sticky='N')
        #button_save_treeview.grid(row=1, column=3,padx=10,pady=10,sticky='N')

        self.iotdata=verifyAccountData.readAccount(self)

        n=0
        for i in self.iotdata.keys(): # 写入数据
            self.treeview.insert('', n, values=(i, self.iotdata[i]['ip'],self.iotdata[i]['port'],self.iotdata[i]['username'],'******'))
            n=n+1


        

        '''
        #控件，标签，删除IOT
        self.label_del = tkinter.Label(self.rootIOT, text='删除服务器')
        self.del_input_name = tkinter.Entry(self.rootIOT,width=15)
        self.del_input_ip = tkinter.Entry(self.rootIOT,width=15)
        self.del_input_port = tkinter.Entry(self.rootIOT,width=15)
        self.del_input_username = tkinter.Entry(self.rootIOT,width=15)
        self.del_input_password = tkinter.Entry(self.rootIOT,width=15)  
        self.del_label_button = tkinter.Button(self.rootIOT, text='确定')
        
        self.label_view = tkinter.Label(self.rootIOT, text='查看服务器')
        self.view_input_name = tkinter.Entry(self.rootIOT,width=15)
        self.view_input_ip = tkinter.Entry(self.rootIOT,width=15)
        self.view_input_port = tkinter.Entry(self.rootIOT,width=15)
        self.view_input_username = tkinter.Entry(self.rootIOT,width=15)
        self.view_input_password = tkinter.Entry(self.rootIOT,width=15)  
        self.view_label_button = tkinter.Button(self.rootIOT, text='确定')
        '''

    def gui_arrang(self):

        
        #布局，图像、标题
        self.label_image.grid(row=0, column=0, columnspan=3,padx=10,pady=10)
        self.label_title.grid(row=0, column=2,columnspan=3,padx=10,pady=10)

        #布局，IOT属性
        self.label_k.grid(row=1, column=0) 
        self.label_name.grid(row=1, column=1)
        self.label_ip.grid(row=1, column=2)
        self.label_port.grid(row=1, column=3)
        self.label_username.grid(row=1, column=4)
        self.label_password.grid(row=1, column=5)

        #布局，添加IOT
        self.label_add.grid(row=2, column=0,sticky='E')
        self.add_input_name.grid(row=2, column=1)
        self.add_input_ip.grid(row=2, column=2)
        self.add_input_port.grid(row=2, column=3)
        self.add_input_username.grid(row=2, column=4)
        self.add_input_password.grid(row=2, column=5)       
        self.add_label_button.grid(row=2, column=6,sticky='W')

        #布局，留白
        self.label_k2.grid(row=4, column=0,padx=10,pady=10,sticky='E')

        #布局，查看服务器、刷新
        self.view_label.grid(row=5, column=0,pady=10,sticky='E')
        #self.view_label_button.grid(row=5, column=6,pady=10,sticky='W')

        #布局，Treeview，查看IOT信息
        self.treeview.grid(row=6, column=0,columnspan=8,padx=50)

        #布局，留白
        self.label_k3.grid(row=7, column=0,padx=10,pady=10,sticky='E')

        '''
        #布局，删除IOT
        self.label_del.grid(row=3, column=0,sticky='E')
        self.del_input_name.grid(row=3, column=1)
        self.del_input_ip.grid(row=3, column=2)
        self.del_input_port.grid(row=3, column=3)
        self.del_input_username.grid(row=3, column=4)
        self.del_input_password.grid(row=3, column=5)  
        self.del_label_button.grid(row=3, column=6,sticky='W')
        '''
        
    def rightClick(self,event):
        self.file_menu = Menu(self.treeview,tearoff=0)
        self.file_menu.add_command(label='刷新')
        self.file_menu.add_command(label='编辑')
        self.file_menu.add_command(label='删除')
        self.file_menu.add_command(label='排序')
        
        
        self.file_menu.post(event.x_root, event.y_root)


        
        #tkinter.messagebox.showinfo(message='右击弹框') 
        
        


    '''

    def siginUp_interface(self):  

        # self.rootIOT.destroy()  

        tkinter.messagebox.showinfo(title='影视资源管理系统', message='进入注册界面')  
    '''
          

    # 进行登录信息验证  

    def backstage_interface(self):  

        account = self.input_account.get().ljust(10," ")  

        password = self.input_password.get().ljust(10," ")  

        #对账户信息进行验证，普通用户返回user，管理员返回master，账户错误返回noAccount，密码错误返回noPassword  

        verifyResult = verifyAccount.verifyAccountData(account,password)  

  

        if verifyResult=='master':  

            self.rootIOT.destroy()  

            tkinter.messagebox.showinfo(title='影视资源管理系统', message='进入管理界面')  

        elif verifyResult=='user':  

            self.rootIOT.destroy()  

            tkinter.messagebox.showinfo(title='影视资源管理系统', message='进入用户界面')   

        elif verifyResult=='noAccount':  

            tkinter.messagebox.showinfo(title='影视资源管理系统', message='该账号不存在请重新输入!')  

        elif verifyResult=='noPassword':  

            tkinter.messagebox.showinfo(title='影视资源管理系统', message='账号/密码错误请重新输入!')  
