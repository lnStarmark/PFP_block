# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 16:51:13 2023

@author: admin
"""

import threading, time
from collections import namedtuple

import operator


def wait_event():
    print('Старт WAIT_EVENT()\t')
    event.wait()
    print('\n........Код обработки по событию в WAIT_EVENT()')

def wait_timeout(time_out):
    print('Старт WAIT_TIMEOUT()')
    while not event.is_set():
        is_set = event.wait(timeout=time_out)
        print(f'TimeOut {time_out} секунды истек')
        if is_set:
            print('\n........Код обработки по событию в WAIT_TIMEOUT()')
        else:
            print('Пока ждем события, код обработки чего-то другого')
            time.sleep(3)

# установка глобального события
event = threading.Event()

print(operator)

student = namedtuple('Person', ['name', 'age', 'gender'])
students = [student("Malevich",20,"male"),
            student("Kusturitca",25,"male"),
            student("Glasha",18,"female"),
            student("Nikifor",27,"male"),
            student("Valia",22,"female"),            
           ]
  
summa = 0
for el in students:
    if( el.gender == "male"): 
        print(f"{el.name} {el.age}, gender: {el.gender}")
        summa += 1
print(f"Vsego male: {summa}")

print()

summa = 0
for el in students:
    if( el.gender == "female"): 
        print(f"{el.name} {el.age}, gender: {el.gender}")
        summa += 1
print(f"Vsego female: {summa}")

'''
t1 = threading.Thread(name='blocking', 
                  target=wait_event)
t1.start()

t2 = threading.Thread(name='non-blocking', 
                  target=wait_timeout, 
                  args=(4,))
t2.start()

print('Ожидание перед вызовом Event.set()')
time.sleep(3)
event.set()
print('Установлено событие в основном потоке\t')
'''

# Старт WAIT_EVENT()
# Старт WAIT_TIMEOUT() 
# Ожидание перед вызовом Event.set()
# TimeOut 2 секунды истек
# Пока ждем события, код обработки чего-то другого
# Установлено событие в основном потоке
# Код обработки по событию в WAIT_EVENT()
# TimeOut 2 секунды истек
# Код обработки по событию в WAIT_TIMEOUT()