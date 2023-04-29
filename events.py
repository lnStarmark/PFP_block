# -*- coding: utf-8 -*-
"""
Комбинированный тест таймера и события от threads модуля

Created on Thu Mar 23 21:48:20 2023

@author:  Starmark LN
@e-mail1: ln.starmark@ekatra.io
@e-mail2: ln.starmark@ekatra.io
"""

from threading import Thread, Event, Timer
from time import sleep, time

cnt = 0

START_OK = False

event = Event()

def worker(ind, name: str): 
    print(f"Worker start: {name}\tindex: {ind}")
    event.wait()
    slp = ((ind+1)*3)/1 
    sleep(slp)
    print(f"Worker stop: {name}\tsleep: {slp}")


def start_event_test():
    global START_OK
    print("Message from Timer: Start_event_test!")
    START_OK = True


#==========================================================================

#--- запуск таймера для включения:  START_OK = True -----------------------
print("Start_Timer!")
timer = Timer(interval=3,function=start_event_test)
timer.start()


#--- Основной поток: Ждем включения по отработке тамера -------------------     
sleep(0.1)
while not START_OK:
    print("Main thread befor start timer")
    sleep(0.25)

#--- Получили разрешения начать работу с Event ----------------------------
# Clear event -----------------
event.clear()
    
# Create and start workers ----
workers = [Thread(target=worker, args=(i, f"wrk {i}",)) for i in range(8)]
    
for w in workers:
    sleep(0.01) 
    w.start()
    
event.set()

#--- Основной поток: Ждем включения по отработке тамера -------------------     
sleep(0.1)
while cnt<100:
    print("Main thread after start timer")
    sleep(0.25)
    cnt += 1
    
    


    
