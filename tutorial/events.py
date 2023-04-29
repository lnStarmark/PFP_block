# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:48:20 2023

@author: admin
"""

from threading import Thread, Event
from time import sleep, time

event = Event()

def worker(name: str): 
    print(f"Worker start: {name}")
    event.wait()
    print(f"Worker stop: {name}")


# Clear event
event.clear()

# Create and start workers
workers = [Thread(target=worker, args=(f"wrk {i}",)) for i in range(5)]

for w in workers:
   w.start()

print("Main thread")

event.set()