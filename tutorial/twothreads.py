# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 18:01:26 2023

@author: admin
"""
import numpy as np
from threading import Thread, Event
from collections import deque
#from queue import Queue

from time import sleep, time

import tkinter as tk
from tkinter import ttk

from tkinter import *

from tkinter import font
from tkinter import messagebox
from tkinter.messagebox import showerror

DELAY = .5
COUNT = 0

'''
LARGE_FONT = 10
MON_FONTSIZE = 12
NOTEBOOK_FONTSIZE = 8
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
'''


root = tk.Tk()

scrollbar = ttk.Scrollbar(root, orient="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13",)
trvw = ttk.Treeview(show="headings", columns=columns, 
                    yscrollcommand=scrollbar.set, selectmode="browse", height=25)
scrollbar.config(command=trvw.yview)

trvw.tag_configure('lightgreen', background='lightgreen')
trvw.tag_configure('lightyellow', background='lightyellow')

trvw.pack(fill=tk.BOTH, expand=1, anchor="se")

trvw.heading("#1", text="NN",anchor="c")
trvw.heading("#2", text="Field2",anchor="c")
trvw.heading("#3", text="Field3",anchor="c")
trvw.heading("#4", text="Field4",anchor="c")
trvw.heading("#5", text="Field5",anchor="c")
trvw.heading("#6", text="Field6",anchor="c")
trvw.heading("#7", text="Field7",anchor="c")
trvw.heading("#8", text="Field8",anchor="c")
trvw.heading("#9", text="Field9",anchor="c")
trvw.heading("#10", text="Field10",anchor="c")
trvw.heading("#11", text="Field11",anchor="c")
trvw.heading("#12", text="Field12",anchor="c")
trvw.heading("#13", text="Field13",anchor="c")
trvw.column("#1",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#2",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#3",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#4",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#5",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#6",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#7",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#8",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#9",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#10",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#11",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#12",  stretch=tk.NO, width=50, anchor="c")
trvw.column("#13",  stretch=tk.NO, width=50, anchor="c")

    

def Gen_Data():
    args = range(1000000)
    lst = []
    for el in args:
        lst.append(el)
        lst.append(np.round(el*el/(el+1)))
        lst.append(np.round(el*np.sin(3*el*3.1415/180.)))
        lst.append(np.round(el*el/(el+1)))
        lst.append(np.round(el*np.sin(3*el*3.1415/180.)))
        lst.append(np.round(el*el/(el+1)))
        lst.append(np.round(el*np.sin(3*el*3.1415/180.)))
        lst.append(np.round(el*el/(el+1)))
        lst.append(np.round(el*np.sin(3*el*3.1415/180.)))
        lst.append(np.round(el*el/(el+1)))
        lst.append(np.round(el*np.sin(3*el*3.1415/180.)))
        lst.append(np.round(el*el/(el+1)))
        lst.append(np.round(el*np.sin(3*el*3.1415/180.)))        
        yield  lst
        lst.clear()
 
mygen = Gen_Data() 
q = deque()       
 
def Producer():
    global q
    for el in mygen:        
        q.append(el)
        sleep(DELAY)        
        
def Consumer():
    global q
    while True:      
        if len(q) > 0:
            print("Consumer: ", q.popleft())
        sleep(DELAY)          
        
def InsToTree():
    global q
    global trvw
    global COUNT
    trvw.tag_configure("evenrow",background='lightblue',foreground='navy')
    trvw.tag_configure("oddrow",background='lightyellow',foreground='brown')
    while True:      
       if len(q) > 0:
           item = q.popleft()
           if(COUNT == 0):
               trvw.insert("", tk.END, values=item, tags=('evenrow',)) 
               COUNT = 1
           elif(COUNT == 1):
               trvw.insert("", tk.END, values=item, tags=('oddrow',))  
               COUNT = 0
           sleep(DELAY)          
  
        
t1 = Thread(target=Producer, args=())  
t1.start()
sleep(0.11)
t2 = Thread(target=InsToTree, args=())
t2.start()      

sWIN = "800x600"    
root.geometry(sWIN)     

root.mainloop()