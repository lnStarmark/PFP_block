# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:56:35 2023

@author: admin
"""
import time

def gen_factory():
    state = None
    while True:
        print("state:", state)
        state = yield state

gen = gen_factory()

def nextCube(acc):
    # Бесконечный цикл
    while True:
        yield acc**3                
        acc += 1 # После повторного обращения
                # исполнение продолжится отсюда
 
# Ниже мы запрашиваем у генератора 
# и выводим ровно 15 чисел
count = 1
for num in nextCube(3):
    if count > 15:
        break   
    print(num)
    count += 1
    
import re

# Этот генератор создает последовательность
# значений True: по одному на каждое
# найденное слово pythonru
# Также для наглядности он выводит
# обработанные слова
def get_pythonru (text) :
    text = re.split('[., ]+', text)
    for word in text:
        print(word)
        if word == "pythonru":
            yield True
 
# Инициализация строки, содержащей текст для поиска
text = "В Интернете есть множество сайтов, \
            но только один pythonru. \
            Программа никогда не прочтет \
            последнее предложение."

# Инициализация переменной с результатом
result = "не найден"

# Цикл произведет единственную итерацию
# в случае наличия в тексте pythonru и 
# не сделает ни одной, если таких слов нет
for j in get_pythonru(text):
    result = "найден"
    break

print ('Результат поиска: %s' % result)    



print('The time is:', time.time())
print('The time is:', time.ctime())
