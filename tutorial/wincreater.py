# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 11:36:03 2023

@author: admin
"""

import configparser as cfprs


import numpy as np 
import math as mt

#--- для работы по выводу в xlsx
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import font

from tkinter import font
from tkinter import messagebox
from tkinter.messagebox import showerror, showwarning, showinfo
import warnings

import str_common as str_c

###============================================================================

'''
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
'''
        

PADDING = 3
BAZE_X = 1500
BAZE_Y = 1000  
SHFT_X = 10
SHFT_Y = 10    
    
def create_WIN_SIZE(b_x, b_y, sh_x, sh_y):
    res = ""
    res += str(b_x)
    res += "x"
    res += str(b_y)
    res += "+"
    res += str(sh_x)
    res += "+"
    res += str(sh_x)
    return res         

def Pan(mast, sid, fil, anch, wdth, hght):   
    frm = ttk.Frame(master=mast, style='TFrame', width=wdth, height=hght,
                    borderwidth=1, relief=tk.SOLID, padding=[PADDING, PADDING])
    frm.pack(side=sid, expand=True, fill=fil, anchor=anch) 
    frm.pack_propagate()
    return frm

def Lab(mast, sid, fil, anch, name):    
    lab = tk.Label(master=mast, text=name, font=font_lab,
                   bg="azure4", fg="antiquewhite1", 
                   bd=1, relief=tk.SUNKEN, anchor="c")   
    lab.pack(side=sid, expand=True, fill=fil) 

###===========================================================================   
str_c.titleprogram("GUI application", 
                   "Program template window-application", 
                   "LN Starmark", mult = str_c.MULT1)   

root = tk.Tk()
root.geometry(create_WIN_SIZE(BAZE_X,BAZE_Y,SHFT_X,SHFT_Y) ) 

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame",
                background="gray20", 
                foreground="yellow",
               )

font_lab = font.Font(family= "Arial", 
                     size=11, weight="bold", 
                     slant="roman", 
                     underline=False, overstrike=False)




pan0 = root 
lab0 = Lab(pan0, tk.TOP, tk.X, "nw", "main_panel 0")


pan01 = Pan(pan0, tk.LEFT, tk.BOTH, "nw", BAZE_X/3-2*PADDING, BAZE_Y-2*PADDING)
lab01 = Lab(pan01, tk.TOP, tk.X, "nw", "panel 01")

pan02 = Pan(pan0, tk.LEFT, tk.BOTH, "nw", 2*BAZE_X/3-2*PADDING, BAZE_Y-2*PADDING)
lab02 = Lab(pan02, tk.TOP, tk.X, "nw", "panel 02")


pan011 = Pan(pan01, tk.TOP, tk.BOTH, "nw", BAZE_X/3-2*PADDING, 3*BAZE_Y/4-2*PADDING)
lab011 = Lab(pan011, tk.TOP, tk.X, "nw", "panel 011")
pan0111 = Pan(pan011, tk.TOP, tk.BOTH, "nw", BAZE_X/3-4*PADDING, 3*BAZE_Y/4-4*PADDING)

pan012 = Pan(pan01, tk.TOP, tk.BOTH, "nw", BAZE_X/3-2*PADDING, BAZE_Y/4-2*PADDING)
lab012 = Lab(pan012, tk.TOP, tk.X, "nw", "panel 012")
pan0121 = Pan(pan012, tk.TOP, tk.BOTH, "nw", BAZE_X/3-4*PADDING, BAZE_Y/4-4*PADDING)


pan021 = Pan(pan02, tk.TOP, tk.BOTH, "nw", 2*BAZE_X/3-2*PADDING, BAZE_Y/4-2*PADDING)
lab021 = Lab(pan021, tk.TOP, tk.X, "nw", "panel 021")
pan0211 = Pan(pan021, tk.TOP, tk.BOTH, "nw", 2*BAZE_X/3-4*PADDING, BAZE_Y/4-4*PADDING)

pan022 = Pan(pan02, tk.TOP, tk.BOTH, "nw", 2*BAZE_X/3-2*PADDING, 3*BAZE_Y/4-2*PADDING)
lab022 = Lab(pan022, tk.TOP, tk.X, "nw", "panel 022")
pan0221 = Pan(pan022, tk.TOP, tk.BOTH, "nw", 2*BAZE_X/3-4*PADDING, 3*BAZE_Y/4-4*PADDING)




root.mainloop() 
###===========================================================================    