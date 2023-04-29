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
#import win32api

from tkinter import *
import tkinter as tk
from tkinter import *
from tkinter import ttk

from tkinter import font
from tkinter import messagebox
from tkinter.messagebox import showerror, showwarning, showinfo

import warnings

from math import *
import numpy as np
from numpy import *

#--- для работы по выводу в xlsx
import pandas as pd

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

#from threading import *
from threading import Thread, Event
from collections import deque

import configparser as cfprs

import PFP_Parser as prs

import str_common as str_c

#--- Events ---------------------------------------------------------------------------

#--- Событие: 'Пришли данные из порта'
eventData = Event()

#--- Clear event
eventData.clear()

q = deque()
q.clear()

SEMAPHORE = False
COUNT = 0
BothReading = 0

#--- Defines --------------------------------------------------------------------------

DEBUG = False
DEBUG_PORT = False
DEBUG_DEMO = False

#--- config ---------------------------------------------------------------------------
###--- Factory config
MOVA = ("EN","UA")
ind_mova = 0
period = 1
points = 25
t_line = 0
t_bar = 0
t_value = 0
t_view3D = 0
t_scale = "Auto"
SCALE = ["10...-80dBm (10...1E-8 mWt)",
         "30...-60dBm (30...1E-6 mWt)",     
         "Auto"]  

###--- Загрузить config
def loadConfig():
    global ind_mova
    global period
    global points
    global t_line
    global t_bar
    global t_value
    global t_view3D
    global t_scale     
    cfg = cfprs.ConfigParser()  # создаём объекта парсера
    cfg.read("config\\Settings.ini")  # читаем конфиг
    ind_mova =  int(cfg["Main"]["ind_mova"])
    period =    int(cfg["Main"]["period"])
    points =    int(cfg["Main"]["points"])
    t_line =    int(cfg["Main"]["t_line"])
    t_bar =     int(cfg["Main"]["t_bar"])
    t_value =   int(cfg["Main"]["t_value"])
    t_view3D =  int(cfg["Main"]["t_view3D"])
    t_scale =   cfg["Main"]["t_scale"]

    print("ind_mova: %d" % ind_mova) 
    print("period: %d" % period) 
    print("points: %d" % points) 
    print("t_line: %d" % t_line) 
    print("t_bar: %d" % t_bar) 
    print("t_value: %d" % t_value) 
    print("t_view3D: %d" % t_view3D) 
    print("t_scale: %s" % t_scale) 

###--- Сохранить config
def saveConfig():
    global ind_mova
    global period
    global points
    global t_line
    global t_bar
    global t_value
    global t_view3D
    global t_scale 
    cfg = cfprs.ConfigParser()
    cfg['Main'] = {'ind_mova': ind_mova,
                     'period': period,
                     'points': points,
                     't_line' : t_line,
                     't_bar'  : t_bar,
                     't_value' : t_value,
                     't_view3D': t_view3D,
                     't_scale' : t_scale}
    with open('config\\Settings.ini', 'w') as configfile:
        cfg.write(configfile)

#--- Параметры главного окна ----------------------------------------------------------
WIN_L = 1600
WIN_H = 1126
WIN_X = 0
WIN_Y = 0
ZAZOR_X = 1
ZAZOR_Y = 1

MAIN_ICON = "img\\logoL.png"
MAIN_TITLE = "ДП МОУ «Науковий центр» ( v 1.01 )"

MOVA = ("EN","UA")
ind_mova = 0

#--- переиенная графики
root = Tk()

main_menu = Menu()

fnt_tab_head = None
fnt_statusbar = None

name_columns = ()   
colnamesEN = ()
colnamesUA = () 
colwidth = []

#--- для работы с USB и COM портом
Device_ID = "" 
Serial_N = ""  

NUMPORTS = 40
BAUDRATE = 19200
TIMEOUT  = 0.002
nCom = 20
str_comm = ""

dict_stat_port = {"0":" closed  ", "1":" opened  "} 
stat_port = "0"
statPortText = tk.StringVar()

full_name_port = "Device not present\nPress 'Open' key menu"
InfoAddText = tk.StringVar()
InfoAddText.set(full_name_port)

full_name_dev = "Factory name"
NameDevText = tk.StringVar()
NameDevText.set(full_name_dev)

icon_left = "img\\ICONleft"
var_icon_left = tk.StringVar()
var_icon_left.set(icon_left)

icon_right = "img\\ICONtight"
var_icon_right = tk.StringVar()
var_icon_right.set(icon_right)


path_img_left_top = "img\\OSN_R.png"
path_img_left_bot = "img\\klav_READ_WRITE_440.png"


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
'''
#VENDOR_ID = 0x0483      # vendor ID
#PRODUCT_ID = 0x374B     # Device product name
'''
VENDOR_ID = 0x1A86      # vendor ID
PRODUCT_ID = 0x7523     # Device product name

PORT = ''
ser = None

item = []
count = 0
tree = ttk.Treeview()
text = Text()
    
#--------------------------------------------------------------------------------------

frameL1 = ttk.Frame()
frameL2 = ttk.Frame()


def empty():
    pass

def Get_SystemFonts():
    #--- Получаем справочные данные об уст. системных фрнтах
    global fnt_tab_head
    print("System fonts available:")
    for font_name in font.names():
        print(font_name)
    print()   

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


freq1 = 0.0
cnt_xxx1 = 0
xxx1 = -100.0
XX1 = np.array([], dtype=float)
YY1 = np.array([], dtype=float)
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
    y = 100*sin(freq1*xxx1/180.0)
    YY1 = np.append(YY1, y)        
        
    PLT_Set_Fonts()
    AX_Config(ax1)
 
    ax1.plot(XX1, YY1, '-go', linewidth=1,  )
    ax1.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    canvasAgg1.draw()    # перерисовать "составной" холст
        
    freq1 += 1.5*sin(xxx1/180.0)
    
    cnt_xxx1 += 1
    if(cnt_xxx1 > points):
        XX1 = XX1[1:]
        YY1 = YY1[1:]
        #cnt_xxx1 = 0
    return


freq2 = 0.0
cnt_xxx = 0
xxx = -100.0
XX = np.array([], dtype=float)
YY = np.array([], dtype=float)
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
    y = 100*sinc(freq2*xxx/180.0)
    YY = np.append(YY, y)        
        
    PLT_Set_Fonts()
    AX_Config(ax2)
 
    ax2.plot(XX, YY, '-go', linewidth=1,  )
    ax2.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    canvasAgg2.draw()    # перерисовать "составной" холст
        
    freq2 += 3*sin(3*xxx/180.0)
    
    cnt_xxx += 1
    if(cnt_xxx > points):
        XX = XX[1:]
        YY = YY[1:]
        #cnt_xxx = 0
    return


#--- Функции клавиш -------------------------------------------------------------------       

def Graph_button_click(event):
    print("Была нажата кнопка Graphics") 
    
def G_raph_key_click(event):
    print("Была нажата клавиша Space")      
    
def Item_prihod(eventData):
    eventData.wait()
    print("EVENT!!!")    
    
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
    Get_SystemFonts()    
    #fnt_tab_head = font.Font(family= "Arial", size=18, weight="bold", slant="roman", underline=True, overstrike=True)
    #fnt_statusbar = font.Font(family= "Verdana", size=16, weight="bold", slant="roman", underline=True, overstrike=True)
    
    sWIN = str(WIN_L)+"x"+str(WIN_H)+"+"+str(WIN_X)+"+"+str(WIN_Y)    
    root.geometry(sWIN)      # Размеры и привязка окна к Л.В. углу
    #root.minsize(WIN_L,WIN_H)      # мин размеры
    #root.maxsize(WIN_L,WIN_H)      # макс размеры
    root.resizable(False, False)    # Разрешить/Запретить растягивать окно
        
    root.title(MAIN_TITLE)          # Заголовок окна

    icon = PhotoImage(file = MAIN_ICON)   # Иконка окна
    root.iconphoto(False, icon)

def Create_Conteiners():
    global frm_top
    global frm_top_L
    global frm_top_R
    global frm_bot
    global frm_bot_L
    global frm_bot_R
    global frm_status
    
    global frm_bot_top 
    
    #--- Верх и низ поля дисплея ------------------------------------------------------
    frm_top = ttk.Frame(master=root, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_top.pack(side=TOP, expand=False, fill=BOTH,  anchor="nw")
    
    #--- Левая верхняя площадка для Canvas слева-вверху -------------------------------
    frm_top_L = ttk.Frame(master=frm_top, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_top_L.pack(side=LEFT, expand=True, fill=Y, anchor="nw")
    
    #--- Правая верхняя площадка для NoteBook с вкладками -----------------------------
    frm_top_R = ttk.Frame(master=frm_top, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_top_R.pack(side=LEFT, expand=True, fill=X, anchor="nw")   
    
    
    #--- Низ
    frm_bot = ttk.Frame(master=root, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot.pack(side=TOP, expand=True, fill=BOTH, anchor="nw")
    
    #--- Левая нижняя площадка для Canvas слева-внизу ---------------------------------
    frm_bot_L = ttk.Frame(master=frm_bot, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_L.pack(side=LEFT, expand=True, fill=Y, anchor="nw")
    
    #--- Правая нижняя площадка для набора вкладок для графиков  
    frm_bot_R = ttk.Frame(master=frm_bot, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_R.pack(side=LEFT, expand=True, fill=X, anchor="nw")  
    
    #----------------------------------------------------------------------------------
    #--- Временная Правая нижняя площадка для вывода данных из ком порта  
    if(DEBUG_PORT == True):
        frm_bot_Temp = ttk.Frame(master=frm_bot, borderwidth=1, relief=SOLID, padding=[0, 0])
        frm_bot_Temp.pack(side=LEFT, expand=True, fill=X, anchor="nw")  
    
        text = Text(master=frm_bot_Temp, width=86, height=35, bg="gray", fg='yellow', wrap=WORD) 
        text.pack(side=LEFT)
        scroll = Scrollbar(master=frm_bot_Temp,command=text.yview)
        scroll.pack(side=LEFT, fill=Y) 
        text.config(yscrollcommand=scroll.set)
    
        cnt = 1.0  
        for el in range(80):
            s = "Create test-string <==========================> for Out to Text window value: "
            s += str(el)
            s += "\n"
            text.insert(cnt,s)
            cnt += 1.0    
    #----------------------------------------------------------------------------------
    
    #--- Status frm -------------------------------------------------------------------
    frm_status = ttk.Frame(master=root, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_status.pack(side=BOTTOM, expand=True, fill=BOTH, anchor="sw")  
    
    #--- Левая нижняя малая 1-я площадка для дополнительной информации ----------------
    frm_bot_top = ttk.Frame(master=frm_bot_L, borderwidth=1, relief=SOLID, padding=[0, 0])
    frm_bot_top.pack(side=TOP, expand=True, fill=X, anchor="nw") 
  
    
def Image_to_frm(frm, w, h, bcolor, pht):
    canv = tk.Canvas(master=frm, bg=bcolor, width=w, height=h)
    canv.pack(anchor="nw", expand=0)
    imgH = canv.create_image(0, 0, anchor='nw',image=pht)
    
def Create_Notebook_for_Tables(frm):
    global frameH1
    global frameH2
    notebookH_tab = ttk.Notebook(frm, style="TNotebook")
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
    
def Create_Notebook_for_Graphics(frm):
    global frameL1
    global frameL2    
    notebookL_tab = ttk.Notebook(frm,style="TNotebook")
    notebookL_tab.pack(side=LEFT, expand=True, fill=X, anchor="nw")
    if(DEBUG_PORT == False):
        notebookL_tab.configure(width=1150, height=537,)
    else:    
        notebookL_tab.configure(width=400, height=537,) ###---###-------------------
 
    # создаем пару фреймвов
    frameL1 = ttk.Frame(notebookL_tab)
    frameL2 = ttk.Frame(notebookL_tab)
 
    frameL1.pack(fill=BOTH, expand=True)
    frameL2.pack(fill=BOTH, expand=True)
 
    # добавляем фреймы в качестве вкладок
    notebookL_tab.add(frameL1, text="Current measurements")
    notebookL_tab.add(frameL2, text="Memory content")
    
    
def Create_Graph_1():
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
    
    
def Create_Graph_2():    
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
    
    
    
def Table_to_tabs(trvw, measurements, columns, colwidth, scrollbar):
    trvw.pack(fill=BOTH, expand=1, anchor="se")    
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
        
def Item_to_table():
    global q
    global SEMAPHORE
    global tree
    global COUNT
    while True:      
       if( (len(q) > 0) and (SEMAPHORE == True) ):                    
           itm = q.popleft() 
           print(itm)
           
           if(COUNT % 2 == 0):
               tree.insert("", tk.END, values=item, tags=('evenrow',)) 
           elif(COUNT % 2 != 0):
               tree.insert("", tk.END, values=item, tags=('oddrow',))   
           COUNT += 1 
           
           sleep(0.001)
           SEMAPHORE = False
           itm.clear()
 
def create_XLSX_name(basename):
    dt = date.today().strftime("%d-%m-%Y") 
    tm = datetime.datetime.now().strftime("%H-%M-%S")
    name = basename
    name += "_"
    name += dt
    name += "_"
    name += tm
    name += ".xlsx" 
    return name
 
def Save_to_xlsx(path, sheet, datalist, colnames):
    df = pd.DataFrame(datalist, columns = colnames)
    print(df)
    #df.to_excel(r'data.xlsx', sheet_name='Main_data', index=False)
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet, index=False)
    writer.save()              
    
#=== Точка входа ======================================================================    
def main():    
    global tree 
   
    #--- Загрузить нвстройки ----------------------------------------------------------
    loadConfig()
    
    #--- Найти устройство на шине -----------------------------------------------------   
    Echo_to_USB()   
    
    #--- Создать главное окно ---------------------------------------------------------
    MainFrame_Create()   

    #--- Вначале порт закрыт - отобразить ---------------------------------------------
    Port_Info(stat_port)
    
    #--- Создание иерархии меню -------------------------------------------------------
    #--- Info: https://metanit.com/python/tkinter/2.18.php
    #----------------------------------------------------------------------------------
    Memu_create(root, main_menu)

    #=== Добавить контейнеры для контейнеров внутри =================================== 
    #--- Info: https://younglinux.info/tkinter/grid
    #---------------------------------------------------------------------------------- 
    Create_Conteiners()
    
    #--- Canvas слева-вверху на Левой верхней площадке --------------------------------
    phtH = ImageTk.PhotoImage(Image.open(path_img_left_top))
    Image_to_frm(frm_top_L, 440, 503, "lightyellow", phtH)
    #----------------------------------------------------------------------------------
    
    #--- Canvas слева-внизу на Левой нижней площадке-----------------------------------
    phtL = ImageTk.PhotoImage(Image.open(path_img_left_bot))
    Image_to_frm(frm_bot_L, 440, 433, "lightblue", phtL)
    #----------------------------------------------------------------------------------      

    #--- создаем набор вкладок для таблицы на Правой верхней площадке -----------------
    #--- https://metanit.com/python/tkinter/2.19.php
    #----------------------------------------------------------------------------------      
    Create_Notebook_for_Tables(frm_top_R)

    #--- создаем набор вкладок для графика на Правой нижней площадке ------------------
    #--- https://metanit.com/python/tkinter/2.19.php
    #---------------------------------------------------------------------------------- 
    Create_Notebook_for_Graphics(frm_bot_R)    

    #... Добавить графическое полотно и поле построения fig ...........................
    #--- Info:  https://www.codecamp.ru/blog/change-font-size-matplotlib/
    #----------------------------------------------------------------------------------
    Create_Graph_1()

    #... Добавить графическое полотно и поле построения fig ...........................
    #--- Info:  https://www.codecamp.ru/blog/change-font-size-matplotlib/
    #----------------------------------------------------------------------------------
    Create_Graph_2()

    #=== Таблицы ======================================================================
    #--- Info: http://grep.cs.msu.ru/python3.8_RU/digitology.tech/docs/python_3/library/tkinter.ttk.html
    #----------------------------------------------------------------------------------  
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
    
    # определяем данные для отображения 
    dt = date.today().strftime("%d-%m-%Y") 
    tm = datetime.datetime.now().strftime("%H:%M:%S")
    # данные таблицы будем получать из порта и после преобразрвания
    if(DEBUG_DEMO == False):
        measurements = []
    elif(DEBUG_DEMO == True):
        measurements = [    
            (1, dt, tm, 1280, 2678, 12.34, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),        
            (2, dt, tm, 1280, 2678, 12.32, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
            (3, dt, tm, 1280, 2678, 12.24, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
            (4, dt, tm, 1280, 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
            (5, dt, tm, 1280, 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
            (6, dt, tm, 1280, 2678, 12.35, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
            (7, dt, tm, 1280, 2678, 12.24, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35),
            (8, dt, tm, 1280, 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
            (9, dt, tm, 1280, 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
            (10, dt, tm, 1280, 2678, 12.35, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
            (11, dt, tm, 1280, 2678, 12.45, "dBm", 1000, "dBm", "Pass", 1.04, 0.82, 1.35), 
            (12, dt, tm, 1280, 2678, 10.31, "dBm", 1000, "dBm", "Fail", 0.04, 0.22, 0.35), 
        ]
        Save_to_xlsx(create_XLSX_name("Result"), 'Main_data', measurements, colnamesEN)
    
    print(dt)
    print(tm)    


    #--- первая закладка -------------------------------------------------------------- 
    scrollbar = ttk.Scrollbar(master=frameH1, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree = ttk.Treeview(master=frameH1, show="headings", columns=name_columns, 
                        yscrollcommand=scrollbar.set, height=17)
    scrollbar.config(command=tree.yview)    
    Table_to_tabs(tree, measurements, name_columns, colwidth, scrollbar)
    
    #--- вторая закладка --------------------------------------------------------------
    scrollbar2 = ttk.Scrollbar(master=frameH2, orient="vertical")
    scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    tree2 = ttk.Treeview(master=frameH2, show="headings", columns=name_columns, 
                         yscrollcommand=scrollbar2.set, height=17)
    scrollbar2.config(command=tree2.yview)     
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
    imglogo1 = ImageTk.PhotoImage(Image.open("img\\logoL.tif"))
    logoL = Label(frm_bot_bot, image = imglogo1,  bd=1, relief=tk.SUNKEN, anchor="sw")
    logoL.pack(side=tk.LEFT)    
    #--- Заводской номер
    InfoLabe3 = tk.Label(frm_bot_bot, textvariable=NameDevText,  bd=1, relief=tk.SUNKEN, anchor="c")
    InfoLabe3.config(font = "Arial 16 bold", bg = "khaki3", fg="navy")
    InfoLabe3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  
    #--- логотип правый
    imglogo2 = ImageTk.PhotoImage(Image.open("img\\logoR.tif"))
    logoR = Label(frm_bot_bot, image = imglogo2,  bd=1, relief=tk.SUNKEN, anchor="sw")
    logoR.pack(side=tk.RIGHT) 
    
    
    #--- Площадка под StatusBar (см. вверху) ------------------------------------------
    #--- А вот и сам StatusBar
    statusbar = tk.Label(frm_status, textvariable=statPortText,  bd=1, relief=tk.SUNKEN, anchor=tk.W)
    statusbar.config(font = "Arial 10 bold", bg = "lightgray", fg="black")
    statusbar.pack(side=tk.LEFT, fill=tk.X) 
    
    
    #--- Опыт с графиками -------------------------------------------------------------
    btn_G = tk.Button(frm_status, text="Graphics", width=10, height=16) 
    btn_G.config(state='disabled', bg = "gray", fg="red", anchor="w")
    btn_G.bind("<Button-1>", evaluate)
    btn_G.pack(side=tk.LEFT, fill=tk.X)
    
    ###--- OR:
    root.bind("<space>", evaluate2    )
    #----------------------------------------------------------------------------------
    
    img_svetofor = ImageTk.PhotoImage(Image.open("img\\svetofor_20.tif"))
    svetofor = tk.Label(frm_status, image = img_svetofor,  bd=1, relief=tk.SUNKEN, anchor="e")
    svetofor.pack(side=tk.RIGHT) 
    #----------------------------------------------------------------------------------

    # Регистрация события закрытия окна и привязка к функции
    root.protocol("WM_DELETE_WINDOW", finish)

    root.mainloop()                       # Перерисовка окна  
 
###====================================================================================
###====================================================================================
###====================================================================================

#--- Функции определения USB ----------------------------------------------------------
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
    
    #win32api.Beep(500, 500)
    # find our device
    dev = usb.core.find(idVendor=venId, idProduct=prodId)
    # was it found?
    if dev is None:
        raise ValueError('Device not found')
        sys.exit()
    else:
        stdev = str(dev)
        #print(stdev)
        print("------------------------------------------------------------")
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

def Echo_to_USB():
    global Device_ID
    global Serial_N
    global InfoAddText
    global NameDevText
    global ind_mova
    
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
    
    
#--- Функции порта --------------------------------------------------------------------

#def ComPort_Work(ser): 
def ComPort_Work():
    global q    
    global SEMAPHORE
    global ser
    global count
    global tree 
    global text    

    #--- По приходу bBegin {0x7E} переводим start = 1
    #--- потом ждем 2-й байт с количеством байт в посылке
    start = 0
    fl_stop = 0   
    #--- должно быть в приходе        
    quantity_bytes = 0
    #--- реально пришлых байт
    cnt_bytes = 0
    
    #--- Сбрасываем буфер приема
    ser.flushInput()
    
    #--- Цикл вычитывания посылки и ее обработка 
    while fl_stop == 0:        

        #--- буфер для прихода
        lst = []

        #--- Забрать данные из буфера порта, как только появятся  
        if (ser.in_waiting > 0):
            lin = ser.read(ser.in_waiting)            

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
                Print_Codes(lst)
               
            #--- Парсерить приход -----------------------------------
            dct = {}
            dct = prs.Parser(lst)
            #--------------------------------------------------------

            if(dct["sMode"]=='INDICATION'):
                dt = date.today().strftime("%d-%m-%Y") 
                tm = datetime.datetime.now().strftime("%H:%M:%S")            
                item.append(count)
                item.append(dt)
                item.append(tm)
                item.append(dct['sFM_NAME'])
                item.append(dct['len_wave'])
                item.append(dct['Val_1'])
                item.append(dct['unit_1'])
                item.append(dct['Val_2'])
                item.append(dct['unit_2'])
                item.append(dct['sBell'])
                BothReading = 1
                
            if(dct["sMode"]=='AKK'): 
                mvlt = dct['mvolts[]']
                item.append(mvlt[0]/1000.)
                item.append(mvlt[1]/1000.)
                item.append(mvlt[2]/1000.)              
                BothReading = 2

            if(BothReading == 2):
                if( (len(q) == 0) and (SEMAPHORE == False) ):                  
                    q.append(item)                    
                    BothReading = 0                      
                    sleep(0.002)                    
                    SEMAPHORE = True                  
                count += 1  
            #--------------------------------------------------------
                  
            #--- Сбросить переменные и флажки для начала нового цикла                  
            cnt_bytes = 0
            start = 0
            fl_stop = 0
            
            ser.reset_input_buffer()
            ser.flushInput()
            

def change_port():
    str_c.zagolovok('Get port from list:')
    nmport = 0
    my_ports = []
    
    TEMPLATE = "USB-SERIAL CH340"
    DEV_ID = "USB\\VID_0x1a86&PID_0x7523"

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

    
        if(Device_ID == DEV_ID):
        #if(prt2 == TEMPLATE):
            print(prt2)    
            print("%5s -> %d" % (st_port, nmport))
            return st_port , full_name
        
        else:
            nmport += 1

    return "COM0"


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
    global stat_port    
    global ser
    global PORT

    st, full_name_port = change_port()
    if(st == "COM0"):  
         print("Device not found")
    else:     
         PORT = st
         ser = ComPort_Open(PORT)
         #--- Убрать вывод в GUI табличку ---
         full_name_port += "\n"
         InfoAddText.set(full_name_port)
         #-----------------------------------
         stat_port = "1"    
         changePortText(stat_port, PORT)

         #===========================================
         if(DEBUG_DEMO == False):
             Thread(target=ComPort_Work, args=()).start()
             sleep(0.25)
             Thread(target=Item_to_table, args=()).start()  
         elif(DEBUG_DEMO == True):
             pass   
         #===========================================

    
def Port_Close():
    global ser
    global PORT
    global stat_port
    #--- Убрать вывод в GUI табличку ---
    full_name_port = "Device closed\n"
    InfoAddText.set(full_name_port)
    #----------------------------------=
    if(stat_port == "1"):
        stat_port = "0"
        changePortText(stat_port, PORT)     
        print('\nЗакрываем порт')
        ser.close()


def changePortText(stat_port, prt):
    str_comm = "Port " + prt + dict_stat_port.get(stat_port)
    statPortText.set(str_comm)
    
def Port_Info(stat_port):
    #--- Вначале порт закрыт
    if(stat_port == "0"):
        changePortText(stat_port, "COMxx") 
    print("stat_port = %s\t{%s}" % (stat_port, dict_stat_port.get(stat_port) ) )    
    
###--------------------------------------------------------------------------

def Print_Codes(lst):
    print("< ", end = ' ')
    for el in lst:        
        print(hex(el),end=' ')
    print(" >\n")  
    
#--- Функции работы с меню и функциями реакции ---------------------------------------- 
def finish():                     # Функция для 
    Port_Close() 
    root.destroy()                # ручного закрытие окна и всего приложения
    print("Закрытие приложения")

def open_click():
    Port_Open()
    
def close_click():
    Port_Close()
    
def save_click():
    empty()
    
def exit_click():
    finish()

def save_config():
    saveConfig()

def period1_click():
    global period
    period = 1   
    print_debug()
def period5_click():
    global period
    period = 5  
    print_debug()
def period10_click():
    global period
    period = 10  
    print_debug()
def period30_click():
    global period
    period = 30  
    print_debug()
def period60_click():
    global period
    period = 60  
    print_debug()     

def points25_click():  
    global points
    points = 25   
    print_debug()
def points50_click(): 
    global points
    points = 50  
    print_debug()      
def points100_click():   
    global points
    points = 100   
    print_debug()
def points200_click():   
    global points
    points = 200 
    print_debug()

    
def line_click():
    global t_line
    if(t_line == 0):
        t_line = 1
    else:
        t_line = 0        
def bar_click():
    global t_bar
    if(t_bar == 0):
        t_bar = 1
    else:
        t_bar = 0
      
def value_click():
    global t_value
    if(t_value == 0):
        t_value = 1
    else:
        t_value = 0        
def view3D_click():
    global t_view3D
    if(t_view3D == 0):
        t_view3D = 1
    else:
        t_view3D = 0
        
def dbm1080_click():
    pass
def dbm3060_click():
    pass
def auto_click():
    pass

def author_click():
    s="Programmer Senior\n"
    s+="Starmark LN\n"
    s+="e-mail: ln.starmark@ekatra.io\n"
    s+="e-mail: ln.starmark@gmail.com\n"
    s+="tel: +380 66 9805661"    
    showinfo(title="About author:", message=s)
    
def owner_click():
    s="ДП МОУ\n"
    s+="Науковый центер\n"
    s+="{v 1.01}\n"
    showinfo(title="Owner:", message=s)
    
def rules_click():
    s="This application is being developed as\n"
    s+="a mock design to control the operation\n"
    s+="of fiber optic cable testers.\n"
    s+="The exact positions of the design elements\n"
    s+="their number and names are not specified here.\n"
    s+="This appendix is ​​to serve as a basis\n"
    s+="for further discussions."
    showinfo(title="Forewarning:", message=s)
    
def confPort_click():
    empty()

def langUA_click():
    global ind_mova
    ind_mova = 1
    print_debug()    
def langEN_click():
    global ind_mova
    ind_mova = 0
    print_debug() 
    

def print_debug():
    print("period: %d\tpoints: %d\t mova: %s" % (period, points, MOVA[ind_mova]))
    
    
def Memu_create(master, main_menu):
    #--- Создание иерархии меню -------------------------------------------------------
    #--- Info: https://metanit.com/python/tkinter/2.18.php
    #----------------------------------------------------------------------------------
    file_menu = Menu(tearoff=0)    
    file_menu.add_command(label="Open port", command=open_click)
    file_menu.add_command(label="Close port", command=close_click)
    file_menu.add_command(label="Save XLS", command=save_click)
    file_menu.add_command(label="Save Config", command=save_config)    
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_click)
 

   
    Language_menu = Menu(tearoff=0) 
    Language_menu.add_command(label="UA", command=langUA_click)
    Language_menu.add_command(label="EN", command=langEN_click)  
    
    config_menu = Menu(tearoff=0)  
    config_menu.add_command(label="Port USB", command=confPort_click)
    config_menu.add_separator()
    config_menu.add_cascade(label="Language", menu=Language_menu) 
    
    
    
    Period_menu = Menu(tearoff=0) 
    Period_menu.add_command(label="1 sec", command=period1_click)
    Period_menu.add_command(label="5 sec", command=period5_click)
    Period_menu.add_command(label="10 sec", command=period10_click)
    Period_menu.add_command(label="30 sec", command=period30_click)
    Period_menu.add_command(label="60 sec", command=period60_click)    
    
    Points_menu = Menu(tearoff=0) 
    Points_menu.add_command(label="25", command=points25_click)
    Points_menu.add_command(label="50", command=points50_click)
    Points_menu.add_command(label="100", command=points100_click)
    Points_menu.add_command(label="200", command=points200_click)       
    
    meas_menu = Menu(tearoff=0)  
    meas_menu.add_cascade(label="Period", menu=Period_menu)
    meas_menu.add_cascade(label="Points", menu=Points_menu)

   
    
    chkmenuview = Menu(tearoff=0)
    chkmenuview.add_checkbutton(label='line', command=line_click)
    chkmenuview.add_checkbutton(label='Bar', command=bar_click)
    chkmenuview.invoke(chkmenuview.index('line'))
    
    chkmenureflection = Menu(tearoff=0)
    chkmenureflection.add_checkbutton(label='Value', command=value_click)
    chkmenureflection.add_checkbutton(label='View_3D', command=view3D_click)
    chkmenureflection.invoke(chkmenureflection.index('Value')) 
    
    scale_menu = Menu(tearoff=0) 
    scale_menu.add_command(label="10...-80dBm (10...1E-8 mWt)", command=dbm1080_click)
    scale_menu.add_command(label="30...-60dBm (30...1E-6 mWt)", command=dbm3060_click)    
    scale_menu.add_command(label="Auto", command=auto_click)  

#    view_menu = Menu(tearoff=0) 
#    view_menu.add_cascade(label="chkmenuview", menu=chkmenuview)
#    view_menu.add_command(label="line", command=line_click)
#    view_menu.add_command(label="Bar", command=bar_click)    
 
#    reflection_menu = Menu(tearoff=0) 
#    reflection_menu.add_command(label="Value", command=value_click)
#    reflection_menu.add_command(label="View_3D", command=view3D_click)
   
    trend_menu = Menu(tearoff=0)    
    trend_menu.add_cascade(label="View", menu=chkmenuview)    
    trend_menu.add_cascade(label="Reflection", menu=chkmenureflection)    
    trend_menu.add_separator()
    trend_menu.add_cascade(label="Scale", menu=scale_menu)



    about_menu = Menu(tearoff=0)  
    about_menu.add_command(label="Rules", command=rules_click)
    about_menu.add_command(label="Owner", command=owner_click)
    about_menu.add_separator()
    about_menu.add_command(label="Author", command=author_click)   

    
    # Создано и передано как параметр main_menu
    main_menu.configure(bg = "lightgray")
    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Config", menu=config_menu)
    main_menu.add_cascade(label="Measurements", menu=meas_menu)
    main_menu.add_cascade(label="Trend", menu=trend_menu)    
    main_menu.add_cascade(label="About", menu=about_menu)

    master.config(menu=main_menu)           # И установить его    
    
  
 
###====================================================================================
if __name__ == "__main__":
    main()       
