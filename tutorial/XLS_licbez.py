# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 22:48:23 2023

@author: admin
"""

import os

# Retrieve current working directory (`cwd`)
cwd = os.getcwd()
print(cwd)

# Change directory 
os.chdir("star")
cwd = os.getcwd()
print(cwd)

# List all files and directories in current directory
lstdir = os.listdir('.')
print(lstdir)
#print(dir(os))