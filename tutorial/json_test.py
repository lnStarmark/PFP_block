# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:29:48 2023

@author: admin
"""

# -*- coding: utf-8 -*-
#!usr/bin/env python

import tkinter as tk
from tkinter import ttk

import json as js

dct = {
    "name":{
        "firstName": "Jane", 
        "lastName": "Doe",
    },
    
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": 
    [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}
jsd = js.dumps(dct, indent=4)    


with open("data_file.json", "w") as w_file:
    js.dump(dct, w_file)  
    
with open("data_s_file.json", "w") as w_s_file:
    js.dump(jsd, w_s_file)   
    

with open("data_file.json", "r") as r_file:
    data = js.load(r_file)
print(data)    

print()

with open("data_s_file.json", "r") as r_s_file:
    datas = js.load(r_s_file)
print(datas) 

#--- словарь фкнкций -----------------
dctf = {}

def fn_square(arg):
    print(f"working fn = {arg*arg}")

def fn_sum(arg):
    print(f"working fn = {arg+arg}")

def fn_sub(arg1, arg2):
    print(f"working fn = {arg1-arg2}")  

f1 = fn_square(1)
f2 = fn_sum(7)
f3 = fn_sub(12,4)

dctf["1"]=f1
dctf["2"]=f2
dctf["3"]=f3

for key in dctf:
    dctf[key]
    



 
