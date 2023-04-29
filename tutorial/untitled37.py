# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 07:24:02 2023

@author: admin
"""

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

import numpy as np 
import math as mt

import random 

def hMeterC(nowValue,x,y,widgLen,widgHigh,maxValue,outerColor,nameValue):
     c = tk.Canvas(root,width=widgLen+50,height=widgHigh+40,bg="black",bd=0, highlightthickness=0, relief='ridge')
     c.place(x=x, y=y)
     return (c,'hmeter',x,y,widgLen,widgHigh,maxValue,outerColor,nameValue)

def hMeter(c,nowValue,x,y,widgLen,widgHigh,maxValue,outerColor,nameValue):
 
     if(nowValue > maxValue): nowValue=maxValue-1
     devValue=float(widgLen) / float(maxValue) 
     mesureValue = devValue * nowValue 
     c.create_rectangle(1,1,widgLen,widgHigh,fill='black',outline=outerColor)
     c.create_rectangle(2,2,int(mesureValue),widgHigh-1,fill=outerColor,outline=outerColor)
     c.create_line(1,widgHigh,1,widgHigh+5,width=1,fill=outerColor) 
     c.create_line(widgLen,widgHigh,widgLen,widgHigh+5,width=1,fill=outerColor)
     c.create_line(1+widgLen/4,widgHigh,1+widgLen/4 ,widgHigh+5,width=1,fill=outerColor)
     c.create_line(1+widgLen/2,widgHigh,1+widgLen/2 ,widgHigh+5,width=1,fill=outerColor) 
     c.create_line(1+widgLen-widgLen/4,widgHigh,1+widgLen-widgLen/4 ,widgHigh+5,width=1,fill=outerColor)
     c.create_text(0,widgHigh+10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill='white',text='0') 
     c.create_text(widgLen -10,widgHigh+10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill='white',text=str(maxValue))
     c.create_text(widgLen/2 -10,widgHigh+10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill='white',text=str(int(maxValue/2)))
     c.create_text(widgLen/4-10,widgHigh+10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill='white',text=str(int(maxValue/4))) 
     c.create_text(widgLen-widgLen/4-10,widgHigh+10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill='white',text=str(int(maxValue-maxValue/4)))
     c.create_text(widgLen +10,widgHigh-8,font="Verdana 12",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(int(nowValue)))
     c.create_text(1,widgHigh+21,font="Verdana 10",anchor="w",justify=tk.CENTER,fill='white',text=nameValue) 

'''
def vMeterC(nowValue,x,y,widgLen,widgHigh,maxValue,outerColor,nameValue):
         c = tk.Canvas(root,width=widgLen+50,height=widgHigh+40,bg="black",bd=0, highlightthickness=0, relief='ridge')
         c.place(x=x, y=y)
         return (c,'vmeter',x,y,widgLen,widgHigh,maxValue,outerColor,nameValue)

def vMeter(c,nowValue,x,y,widgLen,widgHigh,maxValue,outerColor,nameValue):
         if(nowValue > maxValue): nowValue=maxValue-1
         devValue=float(widgHigh) / float(maxValue)
         mesureValue = devValue * nowValue
         c.create_rectangle(1,1,widgLen,widgHigh,fill='black',outline=outerColor)
         c.create_rectangle(widgLen-1,widgHigh,2,widgHigh-int(mesureValue),fill=outerColor,outline=outerColor)
         c.create_line(widgLen,widgHigh,widgLen+10,widgHigh,width=1,fill=outerColor)
         c.create_line(widgLen,widgHigh/4,widgLen+10,widgHigh/4,width=1,fill=outerColor)
         c.create_line(widgLen,widgHigh/2,widgLen+10,widgHigh/2,width=1,fill=outerColor)
         c.create_line(widgLen,widgHigh-widgHigh/4,widgLen+10,widgHigh-widgHigh/4,width=1,fill=outerColor)
         c.create_line(widgLen,1,widgLen+10,1,width=1,fill=outerColor)
         c.create_line(widgLen+10,widgHigh,widgLen+10 ,widgHigh,width=1,fill=outerColor)
         c.create_text(widgLen+12,widgHigh,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text='0')
         c.create_text(widgLen+12,10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue))
         c.create_text(widgLen+12,widgHigh/2,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue/2))
         c.create_text(widgLen+12,widgHigh-widgHigh/4,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue/4))
         c.create_text(widgLen+12,widgHigh/4,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue-maxValue/4))
         c.create_text(2,widgHigh+15,font="Verdana 12",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(nowValue))
'''

def aMeterC(nowValue,x,y,widgLen,widgHigh,maxValue,outerColor,nameValue):
         c = tk.Canvas(root,width=widgLen,height=widgHigh,bg="black",bd=0, highlightthickness=0, relief='ridge')
         c.place(x=x, y=y)
         return (c,'ameter',x,y,widgLen,widgHigh,maxValue,outerColor,nameValue)

def aMeter(c,nowValue,x,y,widgLen,widgHigh,maxValue,outerColor,nameValue):
         if(nowValue > maxValue): nowValue=maxValue-1
         devValue=float(180) / float(maxValue)
         mesureValue = devValue * nowValue
         x1 = widgLen/2
         y1 = widgHigh/2 + 10
         x2 = 10
         y2 = widgHigh/2 + 10
         angle = mt.pi * int(mesureValue) / 180;
         newx = ((x2-x1)*mt.cos(angle)-(y2-y1)*mt.sin(angle)) + x1
         newy = ((x2-x1)*mt.sin(angle)+(y2-y1)*mt.cos(angle)) + y1
         c.create_oval(1 , 1,widgLen-1 ,widgHigh-1,width=2,fill='black',outline=outerColor)
         c.create_text(7,y1,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text='0')
         c.create_text(widgLen-30,y1,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue))
         c.create_text(widgLen/2-10,10,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue/2))
         c.create_text(widgLen/8,widgHigh/4,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue/4))
         c.create_text(widgLen/2+widgLen/4,widgHigh/4,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(maxValue-maxValue/4))
         c.create_text(widgLen/2-20,widgHigh-40,font="Verdana 14",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(nowValue))
         c.create_rectangle(0,widgHigh/2+18,widgLen ,widgHigh,fill='black',outline='black')
         c.create_text(widgLen/2-20,widgHigh-40,font="Verdana 14",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(nowValue))
         c.create_text(6,widgHigh-20,font="Verdana 10",anchor="w",justify=tk.CENTER,fill=outerColor,text=str(nameValue))
         c.create_oval(x1 - 10, y1 - 10, x1+ 10,y1 + 10,fill=outerColor,outline=outerColor)
         c.create_line(x1,y1,newx,newy,width=5,fill=outerColor)

def jobMeter():
    analogFig[0].delete("all")    
    aMeter(analogFig[0],random.randint(30, 800),analogFig[2],analogFig[3],analogFig[4],analogFig[5],analogFig[6],analogFig[7],analogFig[8])
    #hMeter(analogFig[0],random.randint(30, 800),analogFig[2],analogFig[3],analogFig[4],analogFig[5],analogFig[6],analogFig[7],analogFig[8])
    #vMeter(analogFig[0],random.randint(30, 800),analogFig[2],analogFig[3],analogFig[4],analogFig[5],analogFig[6],analogFig[7],analogFig[8])
    root.after(100, jobMeter)
 
#создаем родительский объект
root = tk.Tk()
canv = tk.Canvas(root,width=1900,height=950,bg="black")
canv.place(x=0, y=25)

#analogFig=hMeterC(250,20,50,300,20,1000,'red','analog Meter')
#analogFig=vMeterC(250,20,50,300,20,1000,'red','analog Meter')
analogFig=aMeterC(250,20,50,300,20,1000,'red','analog Meter')

root.after(100, jobMeter)
root.mainloop() 