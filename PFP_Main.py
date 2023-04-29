# -*- coding: utf-8 -*-
"""
Программа чтения бинарного файла 
и расшифровка данных по протоколу
Created on Mon Feb 24 01:36:29 2023

MAIN

@author: ln.starmark@ekatra.io
       : ln.starmark@gmail.com
"""

import os
import sys
import usb
import usb.core
import usb.util
#import win32api

import serial
from serial.tools import list_ports
from time import sleep

import PFP_Parser as prs
import str_common as str_c

DEBUG = False

#--- Мова --------------------------------------
MOVA = ("EN","UA")
ind_mova = 0

#--- Для распознавания своего драйвера ---------
#VENDOR_ID = 0x0483      # vendor ID
#PRODUCT_ID = 0x374B     # Device product name

VENDOR_ID = 0x1A86      # vendor ID
PRODUCT_ID = 0x7523     # Device product name

#--- Setup program -----------------------------
NUMPORTS = 40
BAUDRATE = 19200
TIMEOUT  = 0.002

MAX_REPEAT = 8

#--- Global variables --------------------------
PORT = ''
ser = None

Device_ID = ""
Serial_N = ""

###==========================================================================
###--- Функции
###==========================================================================
    
def os_work():
    str_c.clear()
    cur_path = os.getcwd()  
    print("Current directory: %s" % cur_path)  
    
###==========================================================================
#--- Функции определения USB ----------------------------------------------------------
def USB_GetID(venId, prodId):
    #--- Требуется сформировать
    #--- USB\VID_07E5&PID_7530\IZM-105.21.04  = Вимірювач
    #--- USB\VID_07E5&PID_7530\L-103.21.04  = Джерело випромінювання
    tell1 = "USB\\VID_"    
    tell2 = "&PID_"  
    tell3 = "\\"         
    tellVID = ""
    tellPID = ""
    tellSerialNumber = ""
    
    #win32api.Beep(500, 500)
    # find our device
    dev = usb.core.find(idVendor=venId, idProduct=prodId)
    # was it found?
    if dev is None:
        raise ValueError('Device not found')
        sys.exit()
    else:
        stdev = str(dev)
        #print(stdev)
        print("------------------------------------------------------------")
        lst_dev = stdev.split("\n")
        sl_dev = lst_dev[:15]
        for el in sl_dev:
            print(el)
            ind = el.find("idVendor", 0)         
            if(ind > -1):
                el.strip() 
                tellVID = el[-6:]
            ind = el.find("idProduct", 0)         
            if(ind > -1):
                el.strip() 
                tellPID = el[-6:]
            ind = el.find("iSerialNumber", 0)         
            if(ind > -1):
                el.strip() 
                ind2 = el.find("0x", 0) 
                if(ind2 > -1):
                    tellSerialNumber = el[(-1)*ind2+4:]
            
    path_to_instance_device = []
    path_to_instance_device.append(tell1)
    path_to_instance_device.append(tellVID)
    path_to_instance_device.append(tell2)
    path_to_instance_device.append(tellPID)
    path_to_instance_device.append(tell3)
    path_to_instance_device.append(tellSerialNumber)
    
    Dev_ID = path_to_instance_device[0]+\
             path_to_instance_device[1]+\
             path_to_instance_device[2]+\
             path_to_instance_device[3]
    Ser_N = path_to_instance_device[5]    
     
    return Dev_ID, Ser_N   

def Echo_to_USB():
    global Device_ID
    global Serial_N
    global InfoAddText
    global NameDevText
    global ind_mova
    
    Device_ID, Serial_N = USB_GetID(VENDOR_ID, PRODUCT_ID)
    print("Device: %s;\tSerial: %s" % (Device_ID, Serial_N) ) 
    
    if(ind_mova == 1):
        full_name_port = "Вимірювач\n"+Device_ID
    elif(ind_mova == 0):
        full_name_port = "Meter\n"+Device_ID
#    InfoAddText = tk.StringVar()
#    InfoAddText.set(full_name_port)

    if(ind_mova == 1):  
        full_name_dev = "Серійний №:\n"+Serial_N
    elif(ind_mova == 0):                   
        full_name_dev = "Serial N:\n"+Serial_N 
#    NameDevText = tk.StringVar()
#    NameDevText.set(full_name_dev)

def change_port():
    str_c.zagolovok('Get port from list:')
    nmport = 0
    my_ports = []
    
    TEMPLATE = "USB-SERIAL CH340"
    DEV_ID = "USB\\VID_0x1a86&PID_0x7523"

    listports = list_ports.comports()
    
    for port in listports:
        st_port = str(port)
        full_name = st_port
        
        st_port = st_port[:st_port.index(' ')]
        my_ports.append(st_port)        
    
        prt = str(port)
        ind_tire = prt.find(" - ")
    
    
        ind_beg = ind_tire+3
        prt1 = prt[ind_beg:]
    
        ind_scoba = prt1.find(" (")
        prt2 = prt1[:ind_scoba]

    
        if(Device_ID == DEV_ID):
        #if(prt2 == TEMPLATE):
            print(prt2)    
            print("%5s -> %d" % (st_port, nmport))
            return st_port , full_name
        
        else:
            nmport += 1

    return "COM0"


def ComPort_Open(Port):
    str_c.zagolovok('Port opening:')
  
    try:
      ser = serial.Serial(      
        port = Port,
        baudrate = BAUDRATE,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 0.001, #TIMEOUT, 
        #inter_byte_timeout=0.1
      ) 
 
      ser.setDTR(False) 
      ser.setRTS(False)       

      print('\nСоединение удалось.\n') 
      return ser 

    except serial.SerialException:
      print('\n--- Error: Соединение не удалось ---')
      print() 
      sys.exit()  
###==========================================================================    

def ComPort_Work(ser):  
    #--- По приходу bBegin {0x7E} переводим start = 1
    #--- потом ждем 2-й байт с количеством байт в посылке
    start = 0
    fl_stop = 0   
    #--- должно быть в приходе        
    quantity_bytes = 0
    #--- реально пришлых байт
    cnt_bytes = 0
    
    #--- Сбрасываем буфер приема
    ser.flushInput()
    
    #--- Цикл вычитывания посылки и ее обработка 
    while fl_stop == 0:
        
        #--- буфер для прихода
        lst = []
        #--- Забрать данные из буфера порта, как только появятся  
        if (ser.in_waiting > 0):
            lin = ser.read(ser.in_waiting)
            
            for el in lin:   
                if (el == prs.bBEGIN and start == 0):
                    #--- Наконец встречен стартовый символ. Старт!!!
                    lst.append(el)
                    #--- наращивая количество принятых реально байт
                    cnt_bytes += 1
                    #--- Взвод флажка и переход к ловле блох
                    start = 1                      
                else:
                    #--- Запомнить оглашенное в посылке к-во бвйт
                    if(cnt_bytes == 1):                     
                        quantity_bytes = prs.Get_Quantity(el)
                    #--- и продолжить наполнять список    
                    lst.append(el)
                    #--- наращивая количество принятых реально байт
                    cnt_bytes += 1
                    #--- ставим точки от скуки
                    if(DEBUG == True):
                        print(".", end = " ")                     
                    
                      
            sleep(0.002) 
            
            if(DEBUG == True):
                print("cnt_bytes = %d" % cnt_bytes)                
    
            #--- Обрезаем лишние байты с конца списка
            lst = lst[0:quantity_bytes]
            #--- Показать приход  
            if(DEBUG == True):
                Print_Codes(lst)
               
            #--- Парсерить приход -----------------------------------
            dct = {}
            dct = prs.Parser(lst)  
            #prs.Parser(lst) 
            print(dct)
            #--------------------------------------------------------
                  
            #--- Сбросить переменные и флажки для начала нового цикла                  
            cnt_bytes = 0
            start = 0
            fl_stop = 0
            
            ser.reset_input_buffer()
            ser.flushInput()

###--------------------------------------------------------------------------
  
def ComPort_Stop(ser):
      print('\nЗакрываем порт')
      ser.close() 

###--------------------------------------------------------------------------

def Print_Codes(lst):
    print("< ", end = ' ')
    for el in lst:        
        print(hex(el),end=' ')
    print(" >\n")  
          
###--------------------------------------------------------------------------    
    
def main():
    os_work() 
 
    Echo_to_USB()  
      
    FullNamePORT = change_port()
    print(FullNamePORT)
    PORT = FullNamePORT[0]    
    
    cnt = MAX_REPEAT
    while cnt:    
        ser = ComPort_Open(PORT)
        ComPort_Work(ser)        
        ComPort_Stop(ser)        
        cnt-=1    
           
###==========================================================================
if __name__ == "__main__":
    # выполнить только в том случае, если выполняется как сценарий
    main()

