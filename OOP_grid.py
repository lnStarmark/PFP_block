# -*- coding: utf-8 -*-
"""
Program template window-application

Created on Tue Mar 28 15:33:11 2023

@author: LN Starmark
@e-mail: ln.starmark@ekatra.io
@e-mail: ln.starmark@gmail.com
@tel:    +380 66 9805661
"""

import sys
import os

import usb
import usb.core
import usb.util
#import win32api

import configparser as cfprs


import numpy as np 
import math as mt

#--- для работы по выводу в xlsx
import pandas as pd

import tkinter as tk
from tkinter import ttk

from tkinter import font
from tkinter import messagebox
from tkinter.messagebox import showerror, showwarning, showinfo
import warnings

from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import serial
from serial.tools import  list_ports

from threading import Thread, Event
from collections import deque

import time
import timeit
from time import sleep
import datetime
from datetime import date

import PFP_Parser as prs
import str_common as str_c

#======================================================================================
DEBUG = False

OPSYS = "WIN"
#OPSYS = "LIN"

BAUDRATE = 19200

PRG_NAME = "Template GUI programs"
PRG_USER = "LN Starmark"
VAR_STR = "Test string"

MAIN_TITLE = PRG_NAME

if (OPSYS == "WIN"):
    PATH_MAIN_ICON = "img\\dali.png"
    PATH_CONFIG = 'config\\Config_OOP_Grid.ini'
    PATH_XLSX = "xlsx\\OOP_Grid"
elif(OPSYS == "LIN"):
    PATH_MAIN_ICON = "img/dali.png"
    PATH_CONFIG = 'config/Config_OOP_Grid.ini'
    PATH_XLSX = "xlsx/OOP_Grid"

###--- Factory config
prm = {"mova":"EN","GabX":1600,"GabY":1100,"WIN_X":0,"WIN_Y":0,
       "GUI_RESIZABLE_X":False,"GUI_RESIZABLE_Y":False,
       "MenY":40,"perLeft":0.25,"perRightTop":0.35,
       "perRightMid":0.45,"perRightBot":0.2,
       "baudrate":BAUDRATE,"points":25,
      }

dt = date.today().strftime("%d-%m-%Y") 
tm = datetime.datetime.now().strftime("%H:%M:%S")
colwidth = (80,110,90,110,130,80,80,70,80,85,70,70,70,)
colnamesEN = ("NN","Date","Time","Mod.Hz","Wavelen.nm",
              "Value", 'Unit', "Reper", 'Unit', "Resume", 
              "A.v", "B.v", "C.v",)
measurements = [    
    (1, dt, tm, "2 kHz", 2678, 12.34, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),        
    (2, dt, tm, "2 kHz", 2678, 12.32, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
    (3, dt, tm, "2 kHz", 2678, 12.24, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
    (4, dt, tm, "2 kHz", 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
    (5, dt, tm, "2 kHz", 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
    (6, dt, tm, "2 kHz", 2678, 12.35, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
    (7, dt, tm, "2 kHz", 2678, 12.24, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
    (8, dt, tm, "2 kHz", 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
    (9, dt, tm, "2 kHz", 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
    (10, dt, tm, "2 kHz", 2678, 12.35, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
    (11, dt, tm, "2 kHz", 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
    (12, dt, tm, "2 kHz", 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
]


q = deque()    
SIGNAL = 0

q1 = deque()    
SIGNAL1 = 0
#event_graph = Event()

q2 = deque()
SIGNAL_XLSX = 0  
XLSX_CAPACITY = 25


SIGNAL_GRAPH = 0  


#--- мета-переменные ------------------------------------------------------------------

class MetaVariables():
    def __init__(self):
        self.statPortText = tk.StringVar()
        self.statPortText.set("Port closed                 ")                             
        self.InfoAddText = tk.StringVar()
        self.InfoAddText.set("Device not present. Press 'Open' key menu")

        self.NameDevText = tk.StringVar()
        self.NameDevText.set("Factory name")
        
    def Set_statPortText(self, s):
        self.statPortText.set(s)

    def Set_InfoAddText(self, s):
        self.InfoAddText.set(s)
        
    def Set_NameDevText(self, s):
        self.NameDevText.set(s)
        
    def Get_statPortText(self):
        return self.statPortText.get()

    def Get_InfoAddText(self):
        return self.InfoAddText.get()
        
    def Get_NameDevText(self):
        return self.NameDevText.get()        
        
#--- config --------------------------------------------------------------------------- 
class Cfg():
    def __init__(self, path, dct):
        self.path = path
        self.dct = dict(dct)
        
    ###--- Загрузить config
    def loadConfig(self):
        cfg = cfprs.ConfigParser()  # создаём объекта парсера
        cfg.read(self.path)  # читаем конфиг
        self.dct["mova"] =        cfg["Main"]["mova"]
        self.dct["GabX"] =    int(cfg["Main"]["GabX"])
        self.dct["GabY"] =    int(cfg["Main"]["GabY"])
        self.dct["WIN_X"] =   int(cfg["Main"]["WIN_X"])
        self.dct["WIN_Y"] =   int(cfg["Main"]["WIN_Y"])
        self.dct["GUI_RESIZABLE_X"] =   cfg["Main"]["GUI_RESIZABLE_X"]
        self.dct["GUI_RESIZABLE_Y"] =   cfg["Main"]["GUI_RESIZABLE_Y"]        
        self.dct["MenY"] =    int(cfg["Main"]["MenY"])
        self.dct["perLeft"] =       float(cfg["Main"]["perLeft"])
        self.dct["perRightTop"] =   float(cfg["Main"]["perRightTop"])
        self.dct["perRightMid"] =   float(cfg["Main"]["perRightMid"])
        self.dct["perRightBot"] =   float(cfg["Main"]["perRightBot"]) 
        self.dct["BAUDRATE"] =   int(cfg["Main"]["BAUDRATE"])
        self.dct["points"] =   int(cfg["Main"]["points"])
        return self.dct
    
    ###--- Сохранить config
    def saveConfig(self):
        cfg = cfprs.ConfigParser()
        cfg['Main'] = {'mova': self.dct["mova"],
                       'GabX': self.dct["GabX"],
                       'GabY': self.dct["GabY"],
                       'WIN_X' : self.dct["WIN_X"],
                       'WIN_Y' : self.dct["WIN_Y"],
                       'GUI_RESIZABLE_X' : self.dct["GUI_RESIZABLE_X"],
                       'GUI_RESIZABLE_Y' : self.dct["GUI_RESIZABLE_Y"],                       
                       'MenY' : self.dct["MenY"],
                       'perLeft': self.dct["perLeft"],
                       'perRightTop' : self.dct["perRightTop"],
                       'perRightMid' : self.dct["perRightMid"],
                       'perRightBot' : self.dct["perRightBot"],
                       'BAUDRATE' : self.dct["BAUDRATE"],
                       'points' : self.dct["points"],}                       
        with open(self.path, 'w') as configfile:
            cfg.write(configfile)
            
    def OutConfig(self):
        print("\nCurrent configuration\n")
        print("mova: %s" % self.dct["mova"]) 
        print("GabX: %d" % self.dct["GabX"]) 
        print("GabY: %d" % self.dct["GabY"]) 
        print("WIN_X: %d" % self.dct["WIN_X"]) 
        print("WIN_Y: %d" % self.dct["WIN_Y"]) 
        print("GUI_RESIZABLE_X: %s" % str(self.dct["GUI_RESIZABLE_X"])) 
        print("GUI_RESIZABLE_Y: %s" % str(self.dct["GUI_RESIZABLE_Y"]))         
        print("MenY: %d" % self.dct["MenY"]) 
        print("perLeft: %d" % self.dct["perLeft"]) 
        print("perRightTop: %s" % self.dct["perRightTop"]) 
        print("perRightMid: %s" % self.dct["perRightMid"]) 
        print("perRightBot: %s" % self.dct["perRightBot"]) 
        print("BAUDRATE: %d" % self.dct["BAUDRATE"]) 
        print("points: %d" % self.dct["points"]) 
        
    def Get_sWIN(self):
        sWIN = str(self.dct["GabX"])+"x"+str(self.dct["GabY"])
        sWIN += "+"+str(self.dct["WIN_X"])+"+"+str(self.dct["WIN_Y"])
        return sWIN
    
    def Get_Baud(self):
        return self.dct["BAUDRATE"]
    
    def Get_Points(self):
        return self.dct["points"]    
     
class MyStyles():
    def __init__(self):
        pass 
    
    def create(self):
        LARGE_FONT = 14
        MON_FONTSIZE = 16
        NOTEBOOK_FONTSIZE = 12
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", 
                        font=('Verdana', LARGE_FONT),
                        background="gray", 
                        foreground="yellow",
                        rowheight = int(LARGE_FONT*2.5),
                        )        
                
        style.configure("Treeview",
                        font=('Arial', NOTEBOOK_FONTSIZE),
                        background = "silver",
                        foreground = "navy",
                        rowheight = int(LARGE_FONT*2.5),
                        fieldbackground = "silver",                
                       )
        style.map('Treeview', background=[('selected', 'purple')])
        
        
        font_lab = font.Font(family= "Arial", 
                             size=11, weight="bold", 
                             slant="roman", 
                             underline=False, overstrike=False)
        
        noteStyler = ttk.Style()
        # Import the Notebook.tab element from the default theme
        noteStyler.element_create('Plain.Notebook.tab', "from", 'default')
        # Redefine the TNotebook Tab layout to use the new element
        noteStyler.layout("TNotebook.Tab",
            [('Plain.Notebook.tab', {'children':
                [('Notebook.padding', {'side': 'top', 'children':
                    [('Notebook.focus', {'side': 'top', 'children':
                        [('Notebook.label', {'side': 'top', 'sticky': ''})],
                    'sticky': 'nswe'})],
                'sticky': 'nswe'})],
            'sticky': 'nswe'})])
        noteStyler.configure("TNotebook", background='silver', borderwidth=0)
        noteStyler.configure("TNotebook.Tab", background="ivory3", foreground='navy',
                             lightcolor='silver' , borderwidth=2)
        noteStyler.configure("TNotebook.tab",font=('Verdana', 16, 'bold') )
        noteStyler.configure("TFrame", background='silver', foreground='white', borderwidth=0)        
        
        return font_lab, noteStyler
  
        
class MyMenu():
    def __init__(self,master,com):
        self.com = com 
        
    def create_menu(self):     
        file_menu = tk.Menu(tearoff=0)    
        file_menu.add_command(label="Open port", command=self.open_click)
        file_menu.add_command(label="Close port", command=self.close_click)
        file_menu.add_command(label="Save XLS", command=self.save_click)
        file_menu.add_command(label="Load Config", command=self.load_config)    
        file_menu.add_command(label="Save Config", command=self.save_config)          
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_click)
            
        edit_menu = tk.Menu(tearoff=0)    
        edit_menu.add_command(label="EditParams", command=self.editParams_click)        
        edit_menu.add_command(label="Editconfig", command=self.editConfig_click)
    
        view_menu = tk.Menu(tearoff=0)    
        view_menu.add_command(label="ViewStart", command=self.viewStart_click)
            
        about_menu = tk.Menu(tearoff=0)  
        about_menu.add_command(label="Rules", command=self.rules_click)
        about_menu.add_command(label="Owner", command=self.owner_click)
        about_menu.add_separator()
        about_menu.add_command(label="Author", command=self.author_click)   
            
        # Создано и передано как параметр main_menu
        main_menu = tk.Menu(tearoff=0) 
        main_menu.configure(bg = "gray")
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Edit", menu=edit_menu)
        main_menu.add_cascade(label="View", menu=view_menu)
        main_menu.add_cascade(label="About", menu=about_menu)
        #master.config(menu=main_menu) 
        return main_menu
    
    def finish(self):         
        self.com.Port_Close() 
        root.destroy()    # ручное закрытие окна и всего приложения
        print("Закрытие приложения")
  
    def exit_click(self):
        self.finish()
    
    def open_click(self):
        self.com.Port_Open()        
    def close_click(self):
        self.com.Port_Close()
        
    def save_click(self):
        self.to_xlsx.Save_to_xlsx(self.to_xlsx.create_XLSX_name(), 'Data',
                                  self.BLOCK_TO_XLSX, colnamesEN)      
        self.BLOCK_TO_XLSX = []
                      
    
    def load_config(self):
        self.pem = self.cfg.loadConfig
        #self.cfgedit = self.create_ConfigEditor(self.pem)
    def save_config(self):
        self.cfg.saveConfig() 

    
    def editParams_click(self):
        s="Fragment program\n"
        s+="Edit parameters program"
        showinfo(title="Editor parameters panel:", message=s)
    def editConfig_click(self):
        s="Fragment program\n"
        s+="Edit config panel"
        showinfo(title="Editor config panel:", message=s)
        
    def viewStart_click(self):
        pass
    
    def author_click(self):
        s="Programmer\n"
        s+="Starmark LN\n"
        s+="e-mail: ln.starmark@ekatra.io\n"
        s+="e-mail: ln.starmark@gmail.com\n"
        s+="tel: +380 66 9805661"    
        showinfo(title="About author:", message=s)
        
    def owner_click(self):
        s="STARMARK DESIGN\n"
        s+="help center\n"
        s+="{v 1.01}\n"
        showinfo(title="Owner:", message=s)
        
    def rules_click(self):
        s = "The program is designed for quick deployment"
        s += "\nof a certain class of window applications"
        s += "\nfor practicing control of remote devices"
        s += "\nvia channels: RS-485, Wi-Fi, nRF24,..."
        showinfo(title="Forewarning:", message=s) 


class InfoUSB():
    def __init__(self,master):
        
        #--- для работы с USB и COM портом
        self.VENDOR_ID = 0x1A86      # vendor ID
        self.PRODUCT_ID = 0x7523     # Device product name
        self.Device_ID = "" 
        self.Serial_N = ""  
        self.full_name_dev = ""

    def USB_GetID(self, venId, prodId):
        tell1 = "USB\\VID_"    
        tell2 = "&PID_"  
        tell3 = "\\"         
        tellVID = ""
        tellPID = ""
        tellSerialNumber = ""
        
        print("venId: %s  prodId: %s" % (hex(venId), hex(prodId)) )
        
        #win32api.Beep(500, 500)
        # find our device
        dev = usb.core.find(idVendor=venId, idProduct=prodId)
        # was it found?
        if dev is None:
            raise ValueError('***Device not found')
            sys.exit()
        else:
            stdev = str(dev)
            lst_dev = stdev.split("\n")
            sl_dev = lst_dev[:15]
            for el in sl_dev:
                print(el)
                ind = el.find("idVendor", 0)         
                if(ind > -1):
                    el.strip() 
                    tellVID = el[-6:]
                ind = el.find("idProduct", 0)         
                if(ind > -1):
                    el.strip() 
                    tellPID = el[-6:]
                ind = el.find("iSerialNumber", 0)         
                if(ind > -1):
                    el.strip() 
                    ind2 = el.find("0x", 0)
                    if(ind2 > -1):
                        tellSerialNumber = el[ind2:]

        path_to_instance_device = []
        path_to_instance_device.append(tell1)
        path_to_instance_device.append(tellVID)
        path_to_instance_device.append(tell2)
        path_to_instance_device.append(tellPID)
        path_to_instance_device.append(tell3)
        path_to_instance_device.append(tellSerialNumber)
        
        Dev_ID = path_to_instance_device[0]+\
                 path_to_instance_device[1]+\
                 path_to_instance_device[2]+\
                 path_to_instance_device[3]
        Ser_N = path_to_instance_device[5]    
         
        return Dev_ID, Ser_N   
    
    
    def Echo_to_USB(self):        
        Device_ID, Serial_N = self.USB_GetID(self.VENDOR_ID, self.PRODUCT_ID) 
        self.Device_ID = Device_ID
        print("***Device_ID: %s" % Device_ID)
        self.full_name_dev = Device_ID + "\\" + Serial_N 
        return Device_ID, Serial_N
    
    def Out_Full_Names(self):
        print("Fullname USB device: %s" % self.full_name_dev)
        print("Get_DEVID: %s" % self.Get_DEVID())
        
    def Get_DEVID(self):
        return self.Device_ID     
        

class Comm():
    def __init__(self,master,baudrate, Device_ID, DEV_ID, metavar, metavar2):
        self.dict_stat_port = {"0":" closed  ", "1":" opened  "}         
        self.stat_port = 0          # port OFF
        self.metavar = metavar
        self.metavar2 = metavar2
        
        self.PORT = ""              # port name
        self.ser = None             # descriptor      

        
        self.full_name_port = ""    # для инф
        self.DEV_ID = DEV_ID
        
        #--- для работы с USB и COM портом
        self.Device_ID = Device_ID
        self.Serial_N = ""  

        self.BAUDRATE = baudrate
        self.TIMEOUT  = 0.001
        #nCom = 20
        #str_comm = ""    
        self.count = 0
        self.item = []
        self.val = 0.0

    def change_port(self):
        #--- параметр DEV_ID получим как константу
        str_c.zagolovok('Get port from list:')
        nmport = 0
        my_ports = []
  
        listports = list_ports.comports()
        
        for port in listports:
            st_port = str(port)
            full_name = st_port
            
            st_port = st_port[:st_port.index(' ')]
            my_ports.append(st_port)        
        
            prt = str(port)
            ind_tire = prt.find(" - ")        
        
            ind_beg = ind_tire+3
            prt1 = prt[ind_beg:]
        
            ind_scoba = prt1.find(" (")
            prt2 = prt1[:ind_scoba]
            
            print("Device_ID= %s\t DEV_ID= %s" % (self.Device_ID, self.DEV_ID))
            
            if(self.Device_ID == self.DEV_ID):
                print(prt2)    
                print("%5s -> %d" % (st_port, nmport))
                return st_port , full_name            
            else:
                nmport += 1
    
        return "COM0", "COM0"


    def ComPort_Work(self):
        global q    
        global SIGNAL
        
        global q1    
        global SIGNAL1
    
        #--- По приходу bBegin {0x7E} переводим start = 1
        #--- потом ждем 2-й байт с количеством байт в посылке
        start = 0
        fl_stop = 0   
        #--- должно быть в приходе        
        quantity_bytes = 0
        #--- реально пришлых байт
        cnt_bytes = 0
        
        #--- Сбрасываем буфер приема
        self.ser.flushInput()
        
        #--- Цикл вычитывания посылки и ее обработка 
        while fl_stop == 0:        
    
            #--- буфер для прихода
            lst = []
    
            #--- Забрать данные из буфера порта, как только появятся  
            if (self.ser.in_waiting > 0):
                lin = self.ser.read(self.ser.in_waiting)            
    
                for el in lin:                
                    if (el == prs.bBEGIN and start == 0):
                        #--- Наконец встречен стартовый символ. Старт!!!
                        lst.append(el)
                        #--- наращивая количество принятых реально байт
                        cnt_bytes += 1
                        #--- Взвод флажка и переход к ловле блох
                        start = 1                     
                    else:
                        #--- Запомнить оглашенное в посылке к-во бвйт
                        if(cnt_bytes == 1):              
                            quantity_bytes = prs.Get_Quantity(el)   
                        #--- и продолжить наполнять список    
                        lst.append(el)
                        #--- наращивая количество принятых реально байт
                        cnt_bytes += 1
                        #--- ставим точки от скуки
                        if(DEBUG == True):
                            print(".", end = " ")                              
                          
                sleep(0.002) 
                 
                if(DEBUG == True):
                    print("cnt_bytes = %d" % cnt_bytes)                
        
                #--- Обрезаем лишние байты с конца списка
                lst = lst[0:quantity_bytes]
                #--- Показать приход 
                if(DEBUG == True):
                    self.Print_Codes(lst)
                   
                #--- Парсерить приход -----------------------------------
                dct = {}
                dct = prs.Parser(lst)
                #--------------------------------------------------------
    
                if(dct["sMode"]=='INDICATION'):
                    dt = date.today().strftime("%d-%m-%Y") 
                    tm = datetime.datetime.now().strftime("%H:%M:%S")            
                    self.item.append(self.count)
                    self.item.append(dt)
                    self.item.append(tm)
                    self.item.append(dct['sFM_NAME'])
                    self.item.append(dct['len_wave'])
                    self.val = dct['Val_1']
                    self.item.append(dct['Val_1'])
                    self.item.append(dct['unit_1'])
                    self.item.append(dct['Val_2'])
                    self.item.append(dct['unit_2'])
                    self.item.append(dct['sBell'])
                    BothReading = 1
                    
                if(dct["sMode"]=='AKK'): 
                    mvlt = dct['mvolts[]']
                    self.item.append(mvlt[0]/1000.)
                    self.item.append(mvlt[1]/1000.)
                    self.item.append(mvlt[2]/1000.)              
                    BothReading = 2
    
                if(BothReading == 2):
                    #--- отправка в 2 очереди - в таблицу и в график
                    if( (len(q) == 0) and (SIGNAL == False) ):             
                        q.append(self.item)     #--- пойдет в таблицу                     
                        BothReading = 0                      
                        sleep(0.002)                    
                        SIGNAL = True   
                        
                    if( (len(q1) == 0) and (SIGNAL1 == False) ):                  
                        q1.append(self.val)     #--- пойдет в график                 
                        sleep(0.02)                    
                        SIGNAL1 = True                          
                        
                        
                    self.count += 1  
                #--------------------------------------------------------
                      
                #--- Сбросить переменные и флажки для начала нового цикла                  
                cnt_bytes = 0
                start = 0
                fl_stop = 0
                
                self.ser.reset_input_buffer()
                self.ser.flushInput()
    
    
    def ComPort_Open(self, Port):
        str_c.zagolovok('Port opening:')
      
        try:
          ser = serial.Serial(      
            port = Port,
            baudrate = self.BAUDRATE,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = self.TIMEOUT, 
          ) 
          print("****************************************",ser.port)
     
          ser.setDTR(False) 
          ser.setRTS(False)       
    
          print('\nСоединение удалось.\n') 
          return ser 
    
        except serial.SerialException:
          print('\n--- Error: Соединение не удалось ---')
          print() 
          sys.exit()          
          
    
    def Port_Open(self):
        st, self.full_name_port = self.change_port()
        if(st == "COM0"):  
            print("* *Device not found: st=%s\tfull_name_port=%s" % (st, self.full_name_port))
        else:     
            self.PORT = st
            
        self.ser = self.ComPort_Open(self.PORT)
        #--- вывод в statusbar табличку ----
        self.metavar2.set(self.full_name_port)
        #-----------------------------------
        self.stat_port = "1"    
        self.changePortText(self.stat_port, self.PORT)

        #=== Запуск потока приема из порта =========
        Thread(target=self.ComPort_Work, args=()).start() 
        #===========================================
        
    def Port_Close(self):
        #--- вывод в statusbar табличку ----
        self.full_name_port = "Device closed.      Press 'Open' key menu"
        self.metavar2.set(self.full_name_port)
        #----------------------------------=
        if(self.stat_port == "1"):
            self.stat_port = "0"
            self.changePortText(self.stat_port, self.PORT)     
            print('\nЗакрываем порт')
            self.ser.close()  
            
    def changePortText(self, stat_port, prt):
        str_comm = "Port " + prt + self.dict_stat_port.get(stat_port)
        self.metavar.set(str_comm)
        
    def Port_Info(self, stat_port):
        #--- Вначале порт закрыт
        if(stat_port == "0"):
            self.changePortText(stat_port, "COMxx") 
        print("stat_port = %s\t{%s}" % (stat_port, self.dict_stat_port.get(stat_port) ) )                         
            
    def Print_Codes(self, lst):
        print("< ", end = ' ')
        for el in lst:        
            print(hex(el),end=' ')
        print(" >\n")          
         
    
class To_xlsx():
    #--- Применение --------------------------------------------------------------------
    #--- Save_to_xlsx(create_XLSX_name(), 'Main_data', measurements, colnamesEN)
    #-----------------------------------------------------------------------------------
    def __init__(self, master, basename):
        self.basename = basename
        
    def create_XLSX_name(self):
        dt = date.today().strftime("%d-%m-%Y") 
        tm = datetime.datetime.now().strftime("%H-%M-%S")
        name = self.basename
        name += "_"
        name += dt
        name += "_"
        name += tm
        name += ".xlsx" 
        return name
     
    def Save_to_xlsx(self, path, sheet, datalist, colnames):
        df = pd.DataFrame(datalist, columns = colnames)
        #print(df)
        #df.to_excel(r'data.xlsx', sheet_name='Main_data', index=False)
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet, index=False)
        writer.save()      
#=============================================================================

class App(ttk.Frame):
   
    def __init__(self, master=None):        
        super().__init__(master)
        self.pack()
   
        global SIGNAL_GRAPH     
   
        self.eventGraph = Event()
        self.eventGraph.clear()
        
        self.baud = 19200
        
        self.Device_ID = ""
        self.Serial_N = ""
        
        self.COUNT = 0
        self.BLOCK_TO_XLSX = []           
        self.XLSX_ERRCOUNT = 0
        self.XLSX_OKCOUNT = 0
        
        #--- Meta Variables --------------------------------------------------
        self.metaVar = MetaVariables()
        print(self.metaVar.Get_statPortText())
        print(self.metaVar.Get_NameDevText())
        print(self.metaVar.Get_InfoAddText())
        
        #--- Поиск своего устройства на шине и создание экземпляра порта -----
        self.infoUSB = InfoUSB(self)
        self.Device_ID, self.Serial_N = self.infoUSB.Echo_to_USB()
        self.infoUSB.Out_Full_Names()
        

        #--- Читаем конфигурацию ---------------------------------------------
        prm = dict()
        self.cfg = Cfg(PATH_CONFIG, prm)
        prm = self.cfg.loadConfig()
        self.cfg.OutConfig()               
        sWIN = self.cfg.Get_sWIN()        
        self.baud = self.cfg.Get_Baud()
        
        #--- для работы генератора --------
        self.freq = 0.
        self.cnt_x = 0
        self.cur_x = -100.0
        self.cur_y = 0.0 
        self.XX = np.array([], dtype=float)
        self.YY = np.array([], dtype=float)
        self.points = self.cfg.Get_Points()
        
        #--- Для сохранения в xlsx файл создадим экземпляр писателя ----------
        self.to_xlsx = To_xlsx(self, PATH_XLSX)
        
        #--- Уствнавливает порт ----------------------------------------------
        self.com = Comm(self, self.baud, 
                        self.Device_ID, "USB\\VID_0x1a86&PID_0x7523", 
                        self.metaVar.statPortText, self.metaVar.InfoAddText)       
 
        #--- и строим главное окно приложения --------------------------------
        self.master.geometry(sWIN)  
        self.master.resizable(prm["GUI_RESIZABLE_X"], prm["GUI_RESIZABLE_Y"]) 
        self.master.title(PRG_NAME)    
        self.icon = ImageTk.PhotoImage(file = PATH_MAIN_ICON) 
        self.master.iconphoto(False, self.icon)
        
        #--- указываем стиль -------------------------------------------------
        self.mystyle = MyStyles()
        self.font_lab, self.noteStyler = self.mystyle.create()
        
        #--- строим paneles --------------------------------------------------
        self.menu = MyMenu(self.master,self.com)
        self.main_menu = self.menu.create_menu()
        self.master.config(menu=self.main_menu) 
        
        
        #--- Фреймы ----------------------------------------------------------
        self.frm_bot_status = self.create_BOTTOM()        
        self.create_statusbar(self.metaVar.statPortText, self.metaVar.InfoAddText)
        
        
        self.frm_left = self.create_LEFT()
        
        
        self.frm_left_top = self.create_Panel(self.frm_left, "lab_Left_Top: ", 185)
        self.txt_l = self.create_Text(self.frm_left_top,"Text field", 86, 20,"black","yellow")
        
        self.frm_left_mid = self.create_Panel(self.frm_left, "lab_Left_Mid: ", 185)
        self.txt_2 = self.create_Text(self.frm_left_mid,"Text field 2", 86, 20,"navy","white")
        
        self.frm_left_bot = self.create_Panel(self.frm_left, "Additional text input and output fields: ", 350)
        self.frm_left_bot_L = self.create_Panel_new(self.frm_left_bot, "lab_Left_Bot: ", 350)
        self.frm_left_bot_R = self.create_Panel_new(self.frm_left_bot, "lab_Left_Bot: ", 350)
        self.txt_3 = self.create_ConfigEditor(self.frm_left_bot_L, prm)
        self.txt_4 = self.create_AddEditor(self.frm_left_bot_R, data=None)
        
        self.frm_right = self.create_RIGHT()
        
        self.frm_top = self.create_Panel(self.frm_right, "Graphic functions", 250)
        self.graph = self.Graph_Win(self.frm_top)
        self.val = 0

               
        self.frm_middle = self.create_Panel(self.frm_right, "lab_Right_Mid: ", 250)


        self.frm_bottom = self.create_Panel(self.frm_right, "Table values: ", 120)        
        self.notebook, self.frame1, self.frame2 = self.create_Notebook(self.frm_bottom)

        self.scrollbar = ttk.Scrollbar(master=self.frame1, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree = ttk.Treeview(master=self.frame1, columns=colnamesEN, show="headings", 
                                 yscrollcommand=self.scrollbar.set, height=8)
        self.scrollbar.config(command=self.tree.yview)    
        self.Table_to_tabs(self.tree, measurements, colnamesEN, colwidth, self.scrollbar)   


        #root.bind('self.eventGraph', self.draw_Graph) 
       
        #===========================================
        Thread(target=self.Item_to_table, args=()).start()        
        #===========================================
        
        #===========================================
        Thread(target=self.Get_Value_for_Graph, args=()).start()        
        #===========================================

        #===========================================
        Thread(target=self.Save_to_XLSX, args=()).start()        
        #===========================================
        
        # Регистрация события закрытия окна и привязка к функции
        root.protocol("WM_DELETE_WINDOW", self.menu.finish)
        
      
        
    #--- Все . методы ------------------------------------------------   

    def Item_to_table(self):
        global q
        global SIGNAL
        global SIGNAL_XLSX  

        while True:      
           if( (len(q) > 0) and (SIGNAL == True) ):                    
               itm = q.popleft()
               
               #--- вывод в таблицу ----------------------------------
               if(self.COUNT % 2 == 0):
                   self.tree.insert("", tk.END, values=itm, tags=('evenrow',)) 
               elif(self.COUNT % 2 != 0):
                   self.tree.insert("", tk.END, values=itm, tags=('oddrow',)) 
               self.tree.yview_scroll(number=1, what="units")    
               

               #--- вывод в xlsx -------------------------------------
               self.BLOCK_TO_XLSX.append(itm.copy())               
               if(self.COUNT % XLSX_CAPACITY == 0):
                   SIGNAL_XLSX = True                  
               
               self.COUNT += 1

               
               #--- вывод в текстовое окно --------------------------- 
               s = ' '.join(map(str, itm))
               s += "\n"
               self.txt_l.insert(tk.INSERT, s)
               self.txt_l.yview_scroll(number=1, what="units")  

               
               self.txt_2.insert(tk.INSERT, s)
               self.txt_2.yview_scroll(number=1, what="units")                 
               

               
               sleep(0.1)
               SIGNAL = False
               itm.clear()  
  
    
    #--- вывод в xlsx -------------------------------------  
    def Save_to_XLSX(self):
        global SIGNAL_XLSX  
        
        
        while True:                           
            if(SIGNAL_XLSX == True):
                try:
                    self.to_xlsx.Save_to_xlsx(self.to_xlsx.create_XLSX_name(),'Data', 
                                              self.BLOCK_TO_XLSX, colnamesEN)
                    print("*** XLSX saving Ok {%d} ***"  % self.XLSX_OKCOUNT)
                except:
                    
                    self.XLSX_ERRCOUNT += 1
                    print("*** Error XLSX saving: {%d} ***" % self.XLSX_ERRCOUNT)
                finally:
                    self.BLOCK_TO_XLSX = [] 
                    SIGNAL_XLSX = False
                    self.XLSX_OKCOUNT+=1
                    
               
    #--- выдает x,y пары -----
    def Graph_Win(self, master):
        self.master = master
        self.fig = Figure(figsize=(2.5, 4), dpi=60, facecolor='silver')
        self.fig.subplots_adjust(left=0.045, right=0.97, bottom=0.12, top=0.94, hspace=0.002)        
        self.canvasAgg = FigureCanvasTkAgg(self.fig, master=self.master)
        
        self.canvas = self.canvasAgg.get_tk_widget()
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)        
        
        self.ax = self.fig.add_subplot(111)
        self.ax_config()
        self.PLT_Set_Fonts() 
        return self
        
    def PLT_Set_Fonts(self):
        plt.rc('font', size=14) #controls default text size
        plt.rc('axes', titlesize=14) #fontsize of the title
        plt.rc('axes', labelsize=14) #fontsize of the x and y labels
        plt.rc('xtick', labelsize=14) #fontsize of the x tick labels
        plt.rc('ytick', labelsize=14) #fontsize of the y tick labels
        plt.rc('legend', fontsize=14) #fontsize of the legend  
        
    def ax_config(self):         
        self.ax.clear()          # очистить графическую область
        self.ax.set_facecolor('lightyellow')
        self.ax.set_ylabel("Unit")
        self.ax.set_xlabel("Number point")
        self.ax.set_title("Trend: Current measurements")
        self.ax.minorticks_on()
        self.ax.grid(True)        
 
    def Get_Value_for_Graph(self):
        global q1
        global SIGNAL1
        
        while True: 
            if( (len(q1) > 0) and (SIGNAL1 == True) ):                    
                self.cur_y = q1.popleft()       
                print(f"{self.cur_y}")
               
                self.XX = np.append(self.XX, self.cur_x)   
                self.cur_x += 1          
                self.YY = np.append(self.YY, self.cur_y)                 
            
          
                self.ax.plot(self.XX, self.YY, '-go', linewidth=1,  )
                self.ax.plot.show()
                #self.canvasAgg.draw()    # перерисовать "составной" холст  
                   
                self.cnt_x += 1
                if(self.cnt_x >= self.points):
                    self.XX = self.XX[1:]
                    self.YY = self.YY[1:]  
        
                SIGNAL1 = False

      
    def create_BOTTOM(self):
        frm = ttk.Frame(self.master, borderwidth=3, relief=tk.SOLID, padding=[0, 0])
        frm.pack(side=tk.BOTTOM, expand=False, fill=tk.Y,  anchor="nw")
        return frm    
 
    def create_statusbar(self, metavar, metavar2):
        self.statusbar = tk.Label(self.frm_bot_status, textvariable=metavar,
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.LEFT, fill=tk.X)  
        self.statusbar2 = tk.Label(self.frm_bot_status, textvariable=metavar2,
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar2.pack(side=tk.LEFT, fill=tk.X)     

    def create_LEFT(self):
        frm = ttk.Frame(self.master, borderwidth=3, relief=tk.SOLID, padding=[0, 0])
        frm.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
        return frm
        
    def create_RIGHT(self):
        frm = ttk.Frame(self.master, borderwidth=3, relief=tk.SOLID, padding=[0, 0])
        frm.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH,  anchor="nw")
        return frm
        
    def create_Panel(self, mast, name, hght): 
        lab = tk.Label(master=mast, text=name, font=self.font_lab, 
                       bg="azure4", fg="antiquewhite1", 
                       bd=1, relief=tk.SUNKEN, anchor="c")   
        lab.pack(side=tk.TOP, fill=tk.X)        
        frm = ttk.Frame(master=mast, style='TFrame', height=hght,
                        borderwidth=1, relief=tk.SOLID, padding=[0, 0])
        frm.pack(side=tk.TOP, expand=True, fill=tk.BOTH,  anchor="nw") 
        frm.pack_propagate()
        return frm
    
    def create_Panel_new(self, mast, name, hght): 
        frm = ttk.Frame(master=mast, style='TFrame', height=hght,
                        borderwidth=1, relief=tk.SOLID, padding=[0, 0])
        frm.pack(side=tk.LEFT, expand=True, fill=tk.BOTH,  anchor="nw") 
        frm.pack_propagate()
        return frm
 
    def create_Text(self, mast, name, w, h, b_g, f_g):
        lab = tk.Label(master=mast, text=name, font=self.font_lab, 
                       bg="azure3", fg="darkslateblue", 
                       bd=1, relief=tk.SUNKEN, anchor="c")
        lab.pack(side=tk.TOP, fill=tk.X)
        txt = tk.Text(master=mast,width=w,height=h,bg=b_g,fg=f_g,wrap=tk.WORD)
        txt.pack(side=tk.TOP, fill=tk.BOTH) 
        '''
        scroll_bar = tk.Scrollbar(mast,orient='vertical')
        scroll_bar.pack(side=tk.RIGHT,fill='y',  anchor="ne")
        txt.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=txt.yview)
        '''
        return txt
    
    def create_Notebook(self, mast):
        notebook = ttk.Notebook(master=mast, style="TNotebook")
        notebook.pack(side=tk.TOP, expand=True, fill=tk.X, anchor="nw")
        # создаем пару фреймвов
        frame1 = ttk.Frame(notebook, height=180)
        frame2 = ttk.Frame(notebook, height=180) 
        frame1.pack(fill=tk.BOTH, expand=True)
        frame2.pack(fill=tk.BOTH, expand=True) 
        frame1.pack_propagate()
        frame2.pack_propagate()                
        # добавляем фреймы в качестве вкладок
        notebook.add(frame1, text="Current table",)
        notebook.add(frame2, text="Memory content",)         
        return notebook, frame1, frame2   
    
    def Table_to_tabs(self, trvw, measurements, columns, colwidth, scrollbar):
        trvw.pack(side=tk.TOP, fill=tk.BOTH, expand=1, anchor="nw")    
        trvw.tag_configure('lightgreen', background='lightgreen')
        trvw.tag_configure('lightyellow', background='lightyellow')        
        # заголовки размещаем на Treeview
        trvw.tag_configure("evenrow",background='azure2',foreground='navy')
        trvw.tag_configure("oddrow",background='ivory2',foreground='brown')
        cnt_name = 0
        for el in columns:
            trvw.heading(el, text=columns[cnt_name], anchor="c")
            num = "#"+str(cnt_name+1)
            trvw.column(num, stretch=tk.NO, width=colwidth[cnt_name], anchor="c")
            cnt_name += 1          
 
    def create_Test(self):
        #--- Опыт с labelframe -----------------------------------------------
        self.labelframe = tk.LabelFrame(self.frm_bottom, text="This is a LabelFrame",
                                        bg="silver",fg="brown")
        self.labelframe.pack(side=tk.LEFT, fill="both", expand="no", anchor="c") 
        text1="1 Inside the LabelFrame\nInside the LabelFrame"
        self.left = ttk.Label(self.labelframe,text=text1,foreground="black", background="silver")
        self.left.pack(side=tk.LEFT)
        
        text2="2 Inside the LabelFrame\nInside the LabelFrame"
        self.mid = ttk.Label(self.labelframe,text=text2,foreground="black", background="silver")
        self.mid.pack(side=tk.LEFT)   
        
        text3="This is a LabelFrame 2"
        self.labelframe2 = tk.LabelFrame(self.frm_bottom, text=text3,bg="silver",fg="brown")
        self.labelframe2.pack(side=tk.LEFT, fill="both", expand="no", anchor="c") 
        
        self.right = ttk.Label(self.labelframe2,text="Inside the LabelFrame",
                               foreground="black", background="silver")
        self.right.pack(side=tk.LEFT)  
 
    def create_ConfigEditor(self, mast, prm):
        txt = self.create_Text(mast,"Text editor", 30, 15,"maroon","white")
        txt.pack(side=tk.LEFT, fill=tk.Y, expand="no", anchor="nw")  
        for key in prm:
            txt.insert(tk.INSERT, key)
            txt.insert(tk.INSERT, " = ")
            txt.insert(tk.INSERT, prm[key])
            txt.insert(tk.INSERT, "\n")
            txt.yview_scroll(number=1, what="units") 
          
        return txt    

    def create_AddEditor(self, mast, data=None):
        txt = self.create_Text(mast,"Add text editor", 56, 15,"blue","white")
        txt.pack(side=tk.LEFT, fill=tk.Y, expand="no", anchor="nw")
        return txt
       
        
 
    '''    
    def create_WidgetHello(self):
        self.btnHello = ttk.Button(self,text="Приветствовать:") 
        self.btnHello.bind("<ButtonRelease>", self.say_hello) 
        self.btnHello.pack()
        self.btnShow = ttk.Button(self,text="Exit",
                                  command=root.destroy).pack(side="bottom") 
        
    def say_hello(self, evt):
        tk.messagebox.showinfo("Hi: ", "Hi, "+PRG_USER+"!") 
        
    def create_WidgettestVariable(self):
        self.varstrVal = tk.StringVar()
        self.varstrVal.set(VAR_STR)
        self.entValue = ttk.Entry(self, textvariable=self.varstrVal).pack()
        self.btnShow2 = ttk.Button(self,text="Bывести значение",
                                   command=self.show_value).pack(side="bottom")
        
    def show_value(self):
        print(self.varstrVal.get())
        tk.messagebox.showinfo("varstrVal: ", self.varstrVal.get()) 
    '''
    

###===========================================================================   
str_c.titleprogram("GUI application", 
                   "Program template window-application", 
                   "LN Starmark", mult = str_c.MULT1)        
root = tk.Tk()
app = App(master=root)
root.mainloop() 
###===========================================================================

