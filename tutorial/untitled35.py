# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:57:56 2023

@author: admin
"""

import threading
import time

def thread_function(number):
    print(f"Thread {number}: starting\n")
    for el in range(100):
        print("number[%d]: %d" % (number,el))
        time.sleep(2)
    print(f"Thread {number}: finishing\n")

threads = list()

for index in range(100):
    print(f"Create and start thread {index}\n")
    x = threading.Thread(target=thread_function, args=(index,))
    threads.append(x)
    x.start()

for i,thread in enumerate (threads):
    print (f'Join thread {i} \n')
    thread.join()