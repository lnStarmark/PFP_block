"""
Программа преобразования текстового файла 
с бинарными числами типа '010011100' в бинарный файл
Created on Mon Feb 25 01:36:29 2023

@author: ln.starmark@ekatra.io
"""

#import pickle
#import numpy as np

#import serial
#from serial.tools import list_ports
#import time
#from time import sleep

NAMEFILE = 'IZM_8'
SOURCEFILE = NAMEFILE+'.txt'
RESULTFILE = NAMEFILE+'.bin'

BEGIN = 0x7E

def main():
    WorkFiles()
    
###--------------------------------------------------------------------------
###--- Функции
###--------------------------------------------------------------------------

def Parser(barray):    
    for el in barray:
        print(hex(el),end=' ')
    print() 
    
def PrintList(lst):
    for el in lst:
        print(hex(el),end=' ')
    print()     

    
def WorkFiles():
    
    numbers=[]

    print("Работаем с файлом %s\n" % (SOURCEFILE))

    ###--- Читаем бинарный файл в текстовом виде ZB: "010010111" 
    with open(SOURCEFILE, 'r') as fr:
    
        rlines = fr.readlines()
        numb_lines = len(rlines)
    
        crc = 0
        cnt = 0
        for exemp in rlines:
            ###--- кажлую строку преобразуем к целому по осн. 2 
            v = exemp.strip() 
            val = int(exemp.strip() , 2)
            
            ###--- заодно наращиваем CRC
            crc += val;
        
            ###--- а числа отправляем в список 
            numbers.append(val)
        
            ###--- Контролируем
            if (cnt == numb_lines-2):
                print ('%d\t%s\t0x%x\t\tCRC = 0x%x' % (cnt,v,val,crc & 0x00FF))
            else:
                print ('%d\t%s\t0x%x' % (cnt,v,val))   
                
            cnt+=1  
        print()    
     
        print( "распечатаем список для просмотра" );   
        PrintList(numbers)
      
        ###--- Начали писать полученный список в бинарный файл 
        print("\nпреобр список в bytearray, и запишем в бин. файл")   
        print("пишем .........")
        with open(RESULTFILE,"wb") as fw:
            barray=bytearray(numbers)
            fw.write(barray)
            print() 

        print("Откроем бинарный файл и зачитаем его в bytearray")
        with open(RESULTFILE, 'rb') as fr:
            barr = bytearray(fr.read())
            print("читаем .........")    
            print()   
    
        print("распечатаем barray. Должно все совпасть") 
        Parser(barr)

            
###==========================================================================
if __name__ == "__main__":
    # выполнить только в том случае, 
    # если выполняется как сценарий
    main()



