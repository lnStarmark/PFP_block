# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:16:17 2023

@author: admin
"""
import sys
import os
#import swd
import usb
import usb.core
import usb.util
import win32api

from tkinter import *
import tkinter as tk
from tkinter import *
from tkinter import ttk

from tkinter import font
from tkinter import messagebox
from tkinter.messagebox import showerror

import warnings

from math import *
import numpy as np
from numpy import *

import serial
from serial.tools import list_ports

#import time
#import timeit
from time import sleep
import datetime
from datetime import date

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

import str_common as str_c

#--- Defines --------------------------------------------------------------------------
#--- Параметры главного окна
WIN_L = 1600
WIN_H = 1126
WIN_X = 0
WIN_Y = 0
ZAZOR_X = 1
ZAZOR_Y = 1

MAIN_ICON = "logoL.png"
MAIN_TITLE = "ДП МОУ «Науковий центр» ( v 1.01 )"

#--- переиенная графики
root = Tk()

fnt_tab_head = None
fnt_statusbar = None

MOVA = ("EN","UA")
ind_mova = 0

name_columns = ()   
colnamesEN = ()
colnamesUA = () 
colwidth = []

#--- для работы с COM портом
NUMPORTS = 40
BAUDRATE = 19200
TIMEOUT  = 0.002

nCom = 20
str_comm = ""
dict_stat_port = {"0":" closed  ", "1":" opened  "} 
stat_port = "0"
statPortText = tk.StringVar()

#AddText = ""
full_name_port = "Device not present\nPress 'Open' key menu"
InfoAddText = tk.StringVar()
InfoAddText.set(full_name_port)

icon_left = "ICONleft"
var_icon_left = tk.StringVar()
var_icon_left.set(icon_left)

full_name_dev = "Factory name"
NameDevText = tk.StringVar()
NameDevText.set(full_name_dev)

icon_right = "ICONtight"
var_icon_right = tk.StringVar()
var_icon_right.set(icon_right)


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

#fnt_tab_head=font.Font(family= "Verdana", size=12, weight="bold", slant="roman", underline=True, overstrike=True)
#style.configure("TNotebook", font=('Verdana', 12, 'bold'), )
COLOR_1 = 'silver'
COLOR_2 = 'white'
COLOR_3 = 'navy'
COLOR_4 = '#3E2E0E'
COLOR_5 = '#8A4B08'
COLOR_6 = 'silver' 
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
noteStyler.configure("TNotebook", background=COLOR_1, borderwidth=0)
noteStyler.configure("TNotebook.Tab", background="green", foreground=COLOR_3,
                                      lightcolor=COLOR_6, borderwidth=2)
noteStyler.configure("TNotebook.tab",font=('Verdana', 16, 'bold') )
noteStyler.configure("TFrame", background=COLOR_1, foreground=COLOR_2, borderwidth=0)

#--- Global variables -----------------------------------------------------------------
PORT = ''
ser = None


frameL1 = ttk.Frame()
frameL2 = ttk.Frame()

freq1 = 0.0
freq2 = 0.0

cnt_xxx1 = 0
xxx1 = -100.0
XX1 = np.array([], dtype=float)
YY1 = np.array([], dtype=float)

cnt_xxx = 0
xxx = -100.0
XX = np.array([], dtype=float)
YY = np.array([], dtype=float)

'''
fig1 = Figure(figsize=(1.2, 0.6), dpi=60, facecolor='silver')
ax1 = fig1.add_subplot(111) 
canvasAgg1 = FigureCanvasTkAgg(fig1, master=frameL1)

fig2 = Figure(figsize=(1, 0.5), dpi=60, facecolor='lightgray')
ax2 = fig2.add_subplot(111)
canvasAgg2 = FigureCanvasTkAgg(fig2, master=frameL2)
''' 

#VENDOR_ID = 0x0483      # vendor ID
#PRODUCT_ID = 0x374B     # Device product name

VENDOR_ID = 0x1A86      # vendor ID
PRODUCT_ID = 0x7523     # Device product name

def empty():
    pass

def USB_GetID(venId, prodId):
    #--- Требуется сформировать
    #--- USB\VID_07E5&PID_7530\IZM-105.21.04  = Вимірювач
    #--- USB\VID_07E5&PID_7530\L-103.21.04  = Джерело випромінювання
    tell1 = "USB\\VID_"    
    tell2 = "&PID_"  
    tell3 = "\\"         
    tellVID = ""
    tellPID = ""
    tellSerialNumber = ""
    
    win32api.Beep(500, 500)
    # find our device
    dev = usb.core.find(idVendor=venId, idProduct=prodId)
    # was it found?
    if dev is None:
        raise ValueError('Device not found')
        sys.exit()
    else:
        stdev = str(dev)
        #print(stdev)
        print("-----------------------------------------------------------------")
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
                    tellSerialNumber = el[(-1)*ind2+4:]
            
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
            

def Get_SystemFonts():
    global fnt_tab_head
    print("System fonts available:")
    for font_name in font.names():
        print(font_name)
    print()   
    #fnt_tab_head = font.Font(family= "Verdana", size=18, weight="bold", slant="roman", underline=True, overstrike=True)
    #fnt_statusbar = font.Font(family= "Verdana", size=16, weight="bold", slant="roman", underline=True, overstrike=True)

#... Функции теста графики ............................................................

def PLT_Set_Fonts():
    plt.rc('font', size=16) #controls default text size
    plt.rc('axes', titlesize=16) #fontsize of the title
    plt.rc('axes', labelsize=20) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=15) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=15) #fontsize of the y tick labels
    #plt.rc('legend', fontsize=15) #fontsize of the legend

def AX_Config(ax):
    PLT_Set_Fonts()
 
    ax.clear()          # очистить графическую область
    ax.set_facecolor('lightyellow')
    ax.set_ylabel("dBm")
    ax.set_xlabel("Номер вимiру")
    #ax.set_title("Trend: Current measurements")
    #ax.minorticks_on()
    ax.grid(True)

'''
def evaluate(ax, canvasAgg, freq):
    a = 0.0
    b = 100.0
        
    X = np.linspace(a, b, 8, endpoint=False)
    Y = [100*sin(freq1*x*sin(freq1*x/180.0)/180.0) for x in X]

    PLT_Set_Fonts()
    AX_Config(ax)
 
    ax.plot(X, Y, linewidth=2)
    ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    canvasAgg.draw()    # перерисовать "составной" холст
        
    freq += 5
    if(freq > 100):
        freq = 0
        
    return

def evaluate2(ax, canvasAgg, freq):
    a = 0.0
    b = 100.0
        
    X = np.linspace(a, b, 100, endpoint=False)
    Y = [100*sin(freq2*x/180.0) for x in X]
        
    PLT_Set_Fonts()
    AX_Config(ax)
 
    ax.plot(X, Y, linewidth=2)
    ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    canvasAgg.draw()    # перерисовать "составной" холст
        
    freq += 1.5
    if(freq > 100):
        freq = 0
        
    return
'''

def evaluate(event):
    global fig1
    global ax1
    global canvasAgg1
        
    global freq1    
    global cnt_xxx1
    global xxx1
    global XX1
    global YY1    

    XX1 = np.append(XX1, xxx1)
    xxx1 += 1
    #y = 100*sin(freq2*xxx1/180.0)
    y = 100*sin(freq1*xxx1/180.0)
    #y = 100*sinc(xxx1)
    YY1 = np.append(YY1, y)
        
        
    PLT_Set_Fonts()
    AX_Config(ax1)
 
    ax1.plot(XX1, YY1, '-go', linewidth=1,  )
    ax1.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    canvasAgg1.draw()    # перерисовать "составной" холст
        
    freq1 += 1.5*sin(xxx1/180.0)
    
    cnt_xxx1 += 1
    if(cnt_xxx1 > 100):
        XX1 = XX1[1:]
        YY1 = YY1[1:]
        
    return

def evaluate2(event):
    global fig2
    global ax2
    global canvasAgg2
        
    global freq2 
    global cnt_xxx
    global xxx
    global XX
    global YY    

    XX = np.append(XX, xxx)
    xxx += 1
    #y = 100*sin(freq2*xxx/180.0)
    y = 100*sinc(freq2*xxx/180.0)
    #y = 100*sinc(xxx)
    YY = np.append(YY, y)
        
        
    PLT_Set_Fonts()
    AX_Config(ax2)
 
    ax2.plot(XX, YY, '-go', linewidth=1,  )
    ax2.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    canvasAgg2.draw()    # перерисовать "составной" холст
        
    freq2 += 3*sin(3*xxx/180.0)
    
    cnt_xxx += 1
    if(cnt_xxx > 100):
        XX = XX[1:]
        YY = YY[1:]
       
    return


#--- Функции меню ---------------------------------------------------------------------
def finish():                             # Функция для  
    root.destroy()                        # ручного закрытие окна и всего приложения
    print("Закрытие приложения")

def open_click():
    Port_Open()
    
def close_click():
    Port_Close()
    
def save_click():
    empty()
    
def exit_click():
    finish()

def rules_click():
    empty()
    
def owner_click():
    empty()
    
def autor_click():
    empty()
    
    
def period_click():
    empty()    

def points_click():   
    empty()      
        
def view_click():
    empty()
    
def reflection_click():
    empty()   

def scale_click():
    empty()       
    
def confPort_click():
    empty()

def language_click():
    empty()

#--- Функции клавиш -------------------------------------------------------------------       

def Graph_button_click(event):
    print("Была нажата кнопка Graphics") 
    
def G_raph_key_click(event):
    print("Была нажата клавиша Space")      
    
#--- Функции окна ---------------------------------------------------------------------    
def create_frame(label_text):
    frm = ttk.Frame(borderwidth=1, relief=SOLID, padding=[4, 4])
    # добавляем на фрейм метку
    lb = ttk.Label(frm, text=label_text)
    lb.pack(anchor=NW)
    # добавляем на фрейм текстовое поле
    entry = ttk.Entry(frm)   
    entry.pack(anchor=NW)
    # возвращаем фрейм из функции    
    return frm  

def MainFrame_Create():    
    sWIN = str(WIN_L)+"x"+str(WIN_H)+"+"+str(WIN_X)+"+"+str(WIN_Y)    
    root.geometry(sWIN)      # Размеры и привязка окна к Л.В. углу
    #root.minsize(WIN_L,WIN_H)      # мин размеры
    #root.maxsize(WIN_L,WIN_H)      # макс размеры
    root.resizable(False, False)    # Разрешить/Запретить растягивать окно
        
    root.title(MAIN_TITLE)          # Заголовок окна

    icon = PhotoImage(file = MAIN_ICON)   # Иконка окна
    root.iconphoto(False, icon)

#--- Функции порта --------------------------------------------------------------------
'''
def change_port():
    str_c.zagolovok('Get port from list:')
    nmport = 0
    my_ports = []
    if(os.name=="posix") :
        for i in range(NUMPORTS):
            ###self.comboBox.addItem("/dev/ttyACM{}".format(i))
            pass
    else:
        #--- Windows
        listports = list_ports.comports()
        for port in listports:
            st_port = str(port)
            st_port = st_port[:st_port.index(' ')]
            my_ports.append(st_port)
            print("%5s -> %d" % (st_port, nmport))
            nmport += 1

    err = 0
    while err == 0:
        numport = int(input('Get port by numb:'))
        if(numport < nmport):
            err = 1
            prt = my_ports[numport]
            print('Now port is: %s' % (prt))
            print()
        else:
            print('Err: Noch einmall!')
        
    return prt
'''


def change_port():
    str_c.zagolovok('Get port from list:')
    nmport = 0
    my_ports = []
    
    TEMPLATE = "USB-SERIAL CH340"

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

    
        if(prt2 == TEMPLATE):
            print(prt2)    
            print("%5s -> %d" % (st_port, nmport))
            return st_port , full_name
        
        else:
            nmport += 1

    return "COM0"

def ComPort_Stop(ser):
    print('\nЗакрываем порт')
    ser.close()

    
def ComPort_Open(Port):
    str_c.zagolovok('Port opening:')
  
    try:
      ser = serial.Serial(      
        port = Port,
        baudrate = BAUDRATE,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 0.001, #TIMEOUT, 
        #inter_byte_timeout=0.1
      ) 
 
      ser.setDTR(False) 
      ser.setRTS(False)       

      print('\nСоединение удалось.\n') 
      return ser 

    except serial.SerialException:
      print('\n--- Error: Соединение не удалось ---')
      print() 
      sys.exit()          
      
def Port_Open():
    global ser
    global PORT
    st, full_name_port = change_port()
    if(st == "COM0"):
         print("Device not found")
    else:     
         PORT = st
         full_name_port += "\n"
         InfoAddText.set(full_name_port)
         #ser = ComPort_Open({PORT})
         stat_port = "1"    
         changePortText(stat_port, PORT)
    
def Port_Close():
    global PORT
    full_name_port = "Device closed\n"
    InfoAddText.set(full_name_port)
    
    stat_port = "0"
    changePortText(stat_port, PORT)     
    #ComPort_Stop(ser)

def changePortText(stat_port, prt):
    str_comm = "Port " + prt + dict_stat_port.get(stat_port)
    statPortText.set(str_comm)
  
#=== Точка входа ======================================================================    
def main():    
   
    Device_ID = "" 
    Serial_N = ""  
   
    global ax 
   

    Device_ID, Serial_N = USB_GetID(VENDOR_ID, PRODUCT_ID)
    print("Device: %s;\tSerial: %s" % (Device_ID, Serial_N) ) 
    
    if(ind_mova == 1):
        full_name_port = "Вимірювач\n"+Device_ID
    elif(ind_mova == 0):
        full_name_port = "Meter\n"+Device_ID
    InfoAddText = tk.StringVar()
    InfoAddText.set(full_name_port)

    if(ind_mova == 1):  
        full_name_dev = "Серійний №:\n"+Serial_N
    elif(ind_mova == 0):                   
        full_name_dev = "Serial N:\n"+Serial_N 
    NameDevText = tk.StringVar()
    NameDevText.set(full_name_dev)
   
    MainFrame_Create()
    
    #Get_SystemFonts()

    #--- Вначале порт закрыт
    stat_port = "0"
    changePortText(stat_port, "COMxx")
    
    #--- Создание иерархии меню -------------------------------------------------------
    #--- Info: https://metanit.com/python/tkinter/2.18.php
    #----------------------------------------------------------------------------------
    file_menu = Menu(tearoff=0)           # Созд. file_menu и откл. подчерк.    
    file_menu.add_command(label="Open port", command=open_click)
    file_menu.add_command(label="Close port", command=close_click)
    file_menu.add_command(label="Save XLS", command=save_click)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_click)
 
    about_menu = Menu(tearoff=0)          # Созд. file_menu и откл. подчерк.    
    about_menu.add_command(label="Rules", command=rules_click)
    about_menu.add_command(label="Owner", command=owner_click)
    about_menu.add_separator()
    about_menu.add_command(label="Autor", command=autor_click)   
 
    config_menu = Menu(tearoff=0)          # Созд. file_menu и откл. подчерк.    
    config_menu.add_command(label="Port USB", command=confPort_click)
    config_menu.add_separator()
    config_menu.add_command(label="Language", command=language_click)   
    
    meas_menu = Menu(tearoff=0)          # Созд. file_menu и откл. подчерк.    
    meas_menu.add_command(label="Period", command=period_click)
    meas_menu.add_separator()
    meas_menu.add_command(label="Points", command=points_click)  
 
    trend_menu = Menu(tearoff=0)          # Созд. file_menu и откл. подчерк.    
    trend_menu.add_command(label="View", command=view_click)
    trend_menu.add_command(label="Reflection", command=reflection_click)
    trend_menu.add_separator()
    trend_menu.add_command(label="Scale", command=scale_click)
    
    main_menu = Menu()                    # Создать main_menu
    main_menu.configure(bg = "lightgray")
    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Config", menu=config_menu)
    main_menu.add_cascade(label="Measurements", menu=meas_menu)
    main_menu.add_cascade(label="Trend", menu=trend_menu)    
    main_menu.add_cascade(label="View")      
    main_menu.add_cascade(label="About", menu=about_menu)

    root.config(menu=main_menu)           # И установить его
    
    #--- Добавить контейнер с контейнерами внутри с помощью таблицы ------------------- 
    #--- Info: https://younglinux.info/tkinter/grid
    #---------------------------------------------------------------------------------- 
    
    IPADX1 = 300 
    IPADX2 = 800
    IPAD = 270
    IPADYBOT = 24
    
    #--- Верх и низ поля дисплея ------------------------------------------------------
    frm_top = ttk.Frame(master=root, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_top.pack(side=TOP, expand=False, fill=BOTH,  anchor="nw")
    
    #--- Низ
    frm_bot = ttk.Frame(master=root, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot.pack(side=TOP, expand=True, fill=BOTH, anchor="nw")
    
    #--- Status frm
    frm_status = ttk.Frame(master=root, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_status.pack(side=BOTTOM, expand=True, fill=BOTH, anchor="sw")
    #----------------------------------------------------------------------------------
   
    
    #--- Левая верхняя площадка -------------------------------------------------------
    frm_top_L = ttk.Frame(master=frm_top, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_top_L.pack(side=LEFT, expand=True, fill=Y, anchor="nw")
    
    #--- Canvas слева-вверху
    canv_top_L = Canvas(master=frm_top_L, bg="lightblue", width=440, height=503)
    canv_top_L.pack(anchor="nw", expand=0)

#    imgH = Image.open("OSN_R.png")
    imgH = Image.open("OSN_R.png")
#    imgH = Image.open("STEK_SCAN.png")
    phtH = ImageTk.PhotoImage(imgH)
    imgH = canv_top_L.create_image(0, 0, anchor='nw',image=phtH)
    #----------------------------------------------------------------------------------
    
    
    #--- Правая верхняя площадка для NoteBook с вкладками -----------------------------
    frm_top_R = ttk.Frame(master=frm_top, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_top_R.pack(side=LEFT, expand=True, fill=X, anchor="nw")     
    #--- создаем набор вкладок для таблицы --------------------------------------------
    #--- https://metanit.com/python/tkinter/2.19.php
    notebookH_tab = ttk.Notebook(frm_top_R,  style="TNotebook")
    notebookH_tab.pack(side=LEFT, expand=True, fill=X, anchor="nw")
    notebookH_tab.configure(width=1150, height=481)
 
    # создаем пару фреймвов
    frameH1 = ttk.Frame(notebookH_tab)
    frameH2 = ttk.Frame(notebookH_tab)
 
    frameH1.pack(fill=BOTH, expand=True)
    frameH2.pack(fill=BOTH, expand=True)
 
    # добавляем фреймы в качестве вкладок
    # Python GUI tkinter #22 - Notebook. Вкладки. Виджет с
    notebookH_tab.add(frameH1, text="Current measurements",)
    notebookH_tab.add(frameH2, text="Memory content",)
    #----------------------------------------------------------------------------------     

    
    #--- Левая нижняя площадка --------------------------------------------------------
    frm_bot_L = ttk.Frame(master=frm_bot, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_L.pack(side=LEFT, expand=True, fill=Y, anchor="nw")
   
    #--- Canvas слева-внизу    
    canv_bot_L = Canvas(master=frm_bot_L, bg="lightyellow", width=440, height=433)
    canv_bot_L.pack(anchor="nw", expand=0)
    
    #img = Image.open("klav_CODE_SCAN_350.png")
    imgL = Image.open("klav_READ_WRITE_440.png")
    phtL = ImageTk.PhotoImage(imgL)
    imgL = canv_bot_L.create_image(0, 0, anchor='nw',image=phtL)
    #----------------------------------------------------------------------------------    

    #--- Правая нижняя площадка  
    frm_bot_R = ttk.Frame(master=frm_bot, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_R.pack(side=LEFT, expand=True, fill=X, anchor="nw")   
    
    #--- создаем набор вкладок для графика --------------------------------------------
    #--- https://metanit.com/python/tkinter/2.19.php
    #---------------------------------------------------------------------------------- 
    notebookL_tab = ttk.Notebook(frm_bot_R,style="TNotebook")
    notebookL_tab.pack(side=LEFT, expand=True, fill=X, anchor="nw")
    notebookL_tab.configure(width=1150, height=537,)
 
    # создаем пару фреймвов
    frameL1 = ttk.Frame(notebookL_tab)
    frameL2 = ttk.Frame(notebookL_tab)
 
    frameL1.pack(fill=BOTH, expand=True)
    frameL2.pack(fill=BOTH, expand=True)
 
    # добавляем фреймы в качестве вкладок
    notebookL_tab.add(frameL1, text="Current measurements")
    notebookL_tab.add(frameL2, text="Memory content")
    
    #... Добавить графическое полотно и поле построения fig ...........................
    #--- Info:  https://www.codecamp.ru/blog/change-font-size-matplotlib/
    #----------------------------------------------------------------------------------
    global fig1
    global ax1
    global canvasAgg1
    
    fig1 = Figure(figsize=(1.2, 0.6), dpi=60, facecolor='silver')
    fig1.subplots_adjust(left=0.045, right=0.97, bottom=0.08, top=0.97, hspace=0.002)
    PLT_Set_Fonts()
    
    ax1 = fig1.add_subplot(111)  
    AX_Config(ax1)

    canvasAgg1 = FigureCanvasTkAgg(fig1, master=frameL1)
    canvas1 = canvasAgg1.get_tk_widget()
    canvas1.pack(fill=BOTH, expand=1)    
    
    #... Добавить графическое полотно и поле построения fig ...........................
    #--- Info:  https://www.codecamp.ru/blog/change-font-size-matplotlib/
    #----------------------------------------------------------------------------------
    global fig2
    global ax2
    global canvasAgg2
    
    fig2 = Figure(figsize=(1, 0.5), dpi=60, facecolor='lightgray')
    fig2.subplots_adjust(left=0.045, right=0.97, bottom=0.08, top=0.97, hspace=0.002)
    PLT_Set_Fonts()
    
    ax2 = fig2.add_subplot(111)   
    AX_Config(ax2)

    canvasAgg2 = FigureCanvasTkAgg(fig2, master=frameL2)
    canvas2 = canvasAgg2.get_tk_widget()
    canvas2.pack(fill=BOTH, expand=1)
    

    #=== Таблицы ======================================================================
    #--- Info: http://grep.cs.msu.ru/python3.8_RU/digitology.tech/docs/python_3/library/tkinter.ttk.html
    #----------------------------------------------------------------------------------    
    # определяем данные для отображения 
    dt = date.today().strftime("%d-%m-%Y") 
    cur_time = datetime.datetime.now().strftime("%H:%M:%S")
    # данные таблицы будем получать из порта и после преобразрвания
    measurements = [
        (1, dt, cur_time, 1280, 2678, 12.34, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
        (2, dt, cur_time, 1280, 2678, 12.32, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
        (3, dt, cur_time, 1280, 2678, 12.24, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
        (4, dt, cur_time, 1280, 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
        (5, dt, cur_time, 1280, 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
        (6, dt, cur_time, 1280, 2678, 12.35, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
        (7, dt, cur_time, 1280, 2678, 12.24, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
        (8, dt, cur_time, 1280, 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
        (9, dt, cur_time, 1280, 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
        (10, dt, cur_time, 1280, 2678, 12.35, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),        
    ]
    
    print(dt)
    print(cur_time)
        
    global colnamesEN
    global colnamesUA 
    # определяем заголовки
    name_columns = ("NN", "Date", "Time", "Modulation", "Wavelen", 
               "Value", "Unit", "Reper", "Unitrep", "Resume", 
               "A", "B", "C")    
    colnamesEN = ("NN", "Date", "Time", "Modul.Hz", "Wavelen nm", 
               "Value", "Unit", "Reper", "Unit", "Resume", 
               "A_v", "B_v", "C_v")
    colnamesUA = ("№№", "Дата", "Час", "Модул.Гц", "Довж.хв нм", 
               "Значение", "Од.вим.", "Репер", "Од.вим.", "Резюме", 
               "A в", "B в", "C в")  
    # ширина стлобцрв
    colwidth = (80,110,90,110,130,80,80,70,80,85,70,70,70,)

    #--- первая закладка -------------------------------------------------------------- 
    tree = ttk.Treeview(master=frameH1, columns=name_columns, show="headings", height=17)
    scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview,master=frameH1)
    Table_to_tabs(tree, measurements, name_columns, colwidth, scrollbar)
    
    #--- вторая закладка --------------------------------------------------------------
    tree2 = ttk.Treeview(master=frameH2, columns=name_columns, show="headings", height=17)
    scrollbar2 = ttk.Scrollbar(orient=VERTICAL, command=tree.yview,master=frameH2)
    Table_to_tabs(tree2, measurements, name_columns, colwidth, scrollbar2)
    #==================================================================================   

    #--- Левая нижняя малая 1-я площадка для дополнительной информации ----------------
    frm_bot_top = ttk.Frame(master=frm_bot_L, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_top.pack(side=TOP, expand=True, fill=X, anchor="nw") 
    
    #--- полное название прибора
    InfoLabel = tk.Label(frm_bot_top, textvariable=InfoAddText,  bd=1, relief=tk.SUNKEN, anchor="c")
    InfoLabel.config(font = "Arial 16 bold", bg = "slategray3", fg="navy" )
    InfoLabel.pack(side=tk.TOP, fill=tk.X)  
    
    #--- Левая нижняя малая 2-я площадка для дополнительной информации ----------------
    frm_bot_bot = ttk.Frame(master=frm_bot_L, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_bot.pack(side=TOP, expand=True, fill=X, anchor="nw")   
       
    #--- логотип левый
    imglogo1 = ImageTk.PhotoImage(Image.open("logoL.tif"))
    logoL = Label(frm_bot_bot, image = imglogo1,  bd=1, relief=tk.SUNKEN, anchor="sw")
    logoL.pack(side=tk.LEFT)
    
    #--- Заводской номер
    InfoLabe3 = tk.Label(frm_bot_bot, textvariable=NameDevText,  bd=1, relief=tk.SUNKEN, anchor="c")
    InfoLabe3.config(font = "Arial 16 bold", bg = "khaki3", fg="navy")
    InfoLabe3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
 
    #--- логотип правый
    imglogo2 = ImageTk.PhotoImage(Image.open("logoR.tif"))
    logoR = Label(frm_bot_bot, image = imglogo2,  bd=1, relief=tk.SUNKEN, anchor="sw")
    logoR.pack(side=tk.RIGHT) 
    
    
    #--- Площадка под StatusBar (см. вверху) ------------------------------------------
    #--- А вот и сам StatusBar
    statusbar = tk.Label(frm_status, textvariable=statPortText,  bd=1, relief=tk.SUNKEN, anchor=tk.W)
    statusbar.config(font = "Arial 10 bold", bg = "lightgray", fg="black")
    statusbar.pack(side=tk.LEFT, fill=tk.X) 
    
    btn_G = tk.Button(frm_status, text="Graphics", width=10, height=16) 
    btn_G.config(bg = "gray", fg="red", anchor="w")
    btn_G.bind("<Button-1>", evaluate)
    btn_G.pack(side=tk.LEFT, fill=tk.X)

    ###--- OR:
    root.bind("<space>", evaluate2    )
    
    img_svetofor = ImageTk.PhotoImage(Image.open("svetofor_20.tif"))
    svetofor = tk.Label(frm_status, image = img_svetofor,  bd=1, relief=tk.SUNKEN, anchor="e")
    svetofor.pack(side=tk.RIGHT) 
    #----------------------------------------------------------------------------------


    # Регистрация события закрытия окна и привязка к функции
    root.protocol("WM_DELETE_WINDOW", finish)

    root.mainloop()                       # Перерисовка окна  
 
###====================================================================================
'''
def Graph_to_tabs(fig, ax, canvasAgg):
    fig.subplots_adjust(left=0.045, right=0.97, bottom=0.08, top=0.97, hspace=0.002)
    PLT_Set_Fonts()
    AX_Config(ax)
    canvas = canvasAgg.get_tk_widget()
    canvas.pack(fill=BOTH, expand=1)        
'''

def Table_to_tabs(trvw, measurements, columns, colwidth, scrollbar):
    trvw.pack(fill=BOTH, expand=1, anchor="se")
    trvw.grid(row=0, column=0, sticky="nsew")

    trvw.tag_configure('lightgreen', background='lightgreen')
    trvw.tag_configure('lightyellow', background='lightyellow')
    
    # заголовки размещаем на Treeview
    cnt_name = 0
    for el in columns:
        if(ind_mova == 0):
            trvw.heading(el, text=colnamesEN[cnt_name], anchor="c")
        elif(ind_mova == 1):
            trvw.heading(el, text=colnamesUA[cnt_name], anchor="c")
        num = "#"+str(cnt_name+1)
        trvw.column(num, stretch=tk.NO, width=colwidth[cnt_name], anchor="c")
        cnt_name += 1
    
    # добавляем данные 
    trvw.tag_configure("evenrow",background='lightblue',foreground='navy')
    trvw.tag_configure("oddrow",background='lightyellow',foreground='brown')
    cnt_tag = 0
    for meas in measurements:
        if(cnt_tag % 2 == 0):
            trvw.insert("", END, values=meas, tags=('evenrow',)) 
        elif(cnt_tag % 2 != 0):
            trvw.insert("", END, values=meas, tags=('oddrow',))  
        cnt_tag += 1
        
    # добавляем вертикальную прокрутку
    trvw.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="n")        
 
###====================================================================================
if __name__ == "__main__":
    main()       