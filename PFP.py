# -*- coding: utf-8 -*-
"""
Программа чтения бинарного файла 
и расшифровка данных по протоколу
Created on Mon Feb 24 01:36:29 2023

@author: ln.starmark@ekatra.io
       : ln.starmark@gmail.com
"""

#import pickle
import numpy as np

import os
import sys
#import tempfile

import serial
from serial.tools import list_ports
import time
#import timeit
from time import sleep

import str_common as str_c

#--- Setup program -----------------------------
DIR_NAME = "./"+"TESTDIR"
FILE_EXT = ".txt"

NUMPORTS = 40
BAUDRATE = 19200
TIMEOUT  = 0.002

MAX_REPEAT = 8

#--- Шаблоны для парсера -----------------------

#--- byte 1 ---------------------------
bBEGIN    = 0x7E

#--- byte 2 ---------------------------
bMODE_EMIT = 0x10
sMODE_EMIT = "EMITTION"

bMODE_LSCAN = 0x20
sMODE_LSCAN = "LSCAN"

bMODE_IND = 0x40
sMODE_IND = "INDICATION"

bMODE_SCAN = 0x60
sMODE_SCAN = "SCAN"

bMODE_AKK = 0x70
sMODE_AKK = "AKK"

bMODE_STACK_IND = 0xF1
sMODE_STACK_IND = "STACK_IND"

bMODE_STACK_SCAN = 0xF2
sMODE_STACK_SCAN = "STACK_SCAN"

mode = 0
quantity_bytes = 0
dctMode = {bMODE_EMIT:sMODE_EMIT, 
           bMODE_LSCAN:sMODE_LSCAN, 
           bMODE_IND:sMODE_IND, 
           bMODE_SCAN:sMODE_SCAN, 
           bMODE_AKK:sMODE_AKK, 
           bMODE_STACK_IND:sMODE_STACK_IND,
           bMODE_STACK_SCAN:sMODE_STACK_SCAN}

add_val_EMIT  = 0
add_val_LSCAN  = 0

add_val_IND  = 10
add_val_SCAN  = 10

add_val_INDAKK  = 10
add_val_LAKK = 0
#--------------------------------------

#--- byte 3 ---------------------------
BELL_PASS = 0x00
BELL_FAIL = 0x80
sBELL_PASS = "PASS"
sBELL_FAIL = "FAIL"
bell = 0

fm = 0
FM_270 = 0x00
FM_330 = 0x01
FM_1000= 0x02
FM_2000= 0x03
FM_CW  = 0x04 
FM_NA  = 0x05
sFM_NAME = ["270 Hz", "330 Hz", "1 kHz", "2 kHz", "CW", "N/A"]

num_scan = 0
SCAN_1 = 0x01
SCAN_2 = 0x02
SCAN_3 = 0x03
SCAN_4 = 0x04 
sSCAN_N = ["SCAN_1", "SCAN_2", "SCAN_3", "SCAN_4"] 
#--------------------------------------

#--- byte 4 ---------------------------
#=== Первое число со знаком и типом индикации mode INDICATION
val_1 = 0.0
unit_1 = 0
type_ind_1 = 0

IND5 = 0x00      #формат числа  1.234
IND6 = 0x20      #формат числа  12.34 
IND7 = 0x40      #формат числа  123.4

UNIT0 = 0x00
UNIT2 = 0x20
UNIT4 = 0x40
UNIT6 = 0x60
UNIT8 = 0x80
sUNIT = ["mW", "", "mkW", "", "nW", "", "dBm", "", "dB"]


timeauto = 0
timeeco = 0

tauto_stat = 0
teco_stat = 0

sTAUTO_STAT_ON = "ON"
sTECO_STAT_ON = "ON"

sTAUTO_STAT_OFF = "OFF"
sTECO_STAT_OFF = "OFF"

val2 = 0
len_wave = 0
EmitLenWave = 0

#--- Мощность из оперативной ячейки памяти mode INDICATION 
val_2 = 0.0
unit_2 = 0
type_ind_2 = 0

#--- Первое число со знаком и типом индикации mode SCAN
val_3 = 0.0
unit_3 = 0
type_ind_3 = 0

#--- Мощность принятая по оптическому каналу  mode SCAN
val_4 = 0.0
unit_4 = 0
type_ind_4 = 0

#val3 = 0.0

#--- Для работы с AKK --------------------
type_AKK = 0 ###--- 0 для IND; 1 для EMIT
MAME_AKK = ["AKK_B","AKK_A","AKK_C"]

#--- хранить в списке
mvolts = []
#--- хранить в списке
emit_volts = []

full_status = 0
bit_SCAN = 0x80
bit_USB = 0x20
bit_SIMMETR = 0x04
bit_AKKDATA = 0x01

#--- Сохрвнять в список
sStatus = []
sON_SCAN = "SCAN ON"
sON_USB = "USB ON"
sON_SIMMETR = "SIMMETR ON"
sON_AKKDATA = "DATA READY"

sOFF_SCAN = "SCAN OFF"
sOFF_USB = "USB OFF"
sOFF_SIMMETR = "SIMMETR OFF"
sOFF_AKKDATA = "DATA NOT READY"

#--- Global variables --------------------------
PORT = ''

###==========================================================================
###--- Функции
###==========================================================================

def Parser(lst):
#def Parser(lst, mode):
    np_array = np.asarray (lst) 
        
    str_c.zagolovok('Парсинг данных:')      
    
    print("1\tИсходные данные из порта подготавливаем к обработке: ") 
    CRC_Control(np_array)
    
        
    print("\n3\tРежим и количество байт:",end='  ')     
    mode, quantity_bytes, type_AKK = Get_ModeQuantity(np_array, 1)
    Out_ModeQuantity(mode, quantity_bytes)
    print()
    
    
    if(mode == bMODE_IND):
        print("\n4\tЧастота и прозвонка:",end='\t') 
        fm, bell = Get_FmBell(np_array, 2)
        Out_FmBell(fm, bell) 
        
        print("\n5\tПервое число со знаком и типом индикации:",end='\t') 
        val_1, type_ind_1, unit_1 = Get_FloatFormat(np_array, 3, mode)
        Out_FloatFormat(val_1, type_ind_1, unit_1)
        
        print("\n6\tЗнач. уст. времени  до  АВТОВЫКЛЮЧЕНИЯ:",end='\t') 
        tauto_stat, timeauto = Get_AutoStat(np_array, 6)
        Out_AutoStat(tauto_stat, timeauto)

        print("\n7\tЗнач. време. до перех. в режим ЭКОНОМ:",end='\t')
        teco_stat, timeeco = Get_EcoStat(np_array, 7)
        Out_EcoStat(teco_stat, timeeco)

        print("\n8\tВторое число индикации Длина волны:\t\t",end='\t') 
        #Print_LenWave(np_array, 8)
        len_wave = Get_LenWave(np_array, 8)
        Out_LenWave(len_wave)
               
        print("\n9\tМощность из оперативной ячейки памяти:\t",end='\t') 
        val_2, type_ind_2, unit_2 = Get_FloatFormat(np_array, 11, mode)
        Out_FloatFormat(val_2, type_ind_2, unit_2)        

        
    elif(mode == bMODE_SCAN):
        print("4\tЧастота и номер SCAN:",end='\t') 
        fm, num_scan = Get_FmNumscan(np_array, 2)
        Out_FmNumscan(fm, num_scan)  
        
        print("\n5\tПервое число со знаком и типом индикации:",end='\t') 
        val_3, type_ind_3, unit_3 = Get_FloatFormat(np_array, 3, mode)
        Out_FloatFormat(val_3, type_ind_3, unit_3)
        
        print("\n6\tВторое число индикации Длина волны:\t\t",end='\t') 
        #Print_LenWave(np_array, 6)
        len_wave = Get_LenWave(np_array, 6)
        Out_LenWave(len_wave)
        
        print("\n7\tМощность принятая по оптическому каналу:",end='\t') 
        val_4, type_ind_4, unit_4 = Get_FloatFormat(np_array, 9, mode)
        Out_FloatFormat(val_4, type_ind_4, unit_4)
        
        
    elif(mode == bMODE_AKK):
        print("4   Напряжение на %s :\tMode{%s}" % (dctMode.get(mode), hex(mode)) ) 
        if(type_AKK == 0):   
            mvolts = Get_AkkVolts(np_array, 2)
            Out_AkkVolts(mvolts)
        elif(type_AKK == 1):
            mvolts = Get_AkkVolts(np_array, 2)
            Out_AkkVolts(mvolts)
            
        print("5   Состояние контроллера: ",end='\t' )     
        full_status, sStatus = Get_FullStatus(np_array, 8)
        Out_FullStatus(sStatus)
        
    elif(mode == bMODE_EMIT):  
        print("4\tЧастота FM:",end='\t') 
        fm, form = Get_FmEmit(np_array, 2)
        Out_FmEmit(fm, form) 
        
        print("\n5\tВыходная мощность излучения:",end='\t') 
        val, type_ind, unit = Get_PowerEmit(np_array, 5)  
        Out_PowerEmit(val, type_ind, unit )  
        
    elif(mode == bMODE_LSCAN):
        print("\n4\tЧастота FM и номер LSCAN:",end='\t') 
        fm, num_scan = Get_EmitFmNumscan(np_array, 2)
        Out_EmitFmNumscan(fm, num_scan)    
        
        print("\n5\tПорядковый номер емиттера:",end='\t') 
        num_emit = Get_NumEmit(np_array, 4)
        Out_NumEmit(num_emit)  
        
        print("\n6\tДлина волны емиттера:",end='\t\t\t') 
        EmitLenWave = Get_EmitLenWave(np_array, 6)
        Out_EmitLenWave(EmitLenWave)
        
        print("\n7\tВыходная мощность излучения:",end='\t') 
        val, type_ind, unit = Get_PowerEmit(np_array, 7)  
        Out_PowerEmit(val, type_ind, unit )         
     
    str_c.zagolovok('Конец парсинга данных')      
       
###==========================================================================

def CRC_Control(nparray):   
    
    ln = len(nparray)   
    
    if(ln == 0):
        print("\t\t--- Read error ---")
        sys.exit()
    
    else:
        last_crc = nparray[ln-1]
        sm_crc = (sum(nparray) - last_crc ) & 0x00FF
     

        sMode = dctMode.get(nparray[1] & 0xF0)

        print("\n2\tПроверка CRC mode{%s}: " % (sMode), end=' ' )     
        if( sm_crc == last_crc ):
            print("\tCRC: 0x%x == lastCRC: 0x%x " % (sm_crc, last_crc) )    
        else:
            print("\t\t--- CRC error ---")
            return 1

###-------------------------------------------------------------------------- 

def Get_ModeQuantity(nparray, index):
    type_AKK = -1
    mode = nparray[index] & 0xF0
    
    if( mode == bMODE_IND ): 
        quantity_bytes = (nparray[index] & 0x0F) + add_val_IND 
    elif(mode == bMODE_SCAN):    
        quantity_bytes = (nparray[index] & 0x0F) + add_val_SCAN 
    elif(mode == bMODE_AKK):
        if(nparray[index] & 0x0F == 0):
            quantity_bytes = (nparray[index]) + add_val_INDAKK
            type_AKK = 0
        else:
            quantity_bytes = (nparray[index]) + add_val_LAKK
            type_AKK = 1
    elif(mode == bMODE_STACK_IND):    
        quantity_bytes = 0
    elif(mode == bMODE_STACK_SCAN):    
        quantity_bytes = 0  
        
    elif( mode == bMODE_EMIT ): 
        quantity_bytes = (nparray[index] & 0x0F) + add_val_EMIT 
    elif(mode == bMODE_LSCAN):    
        quantity_bytes = (nparray[index] & 0x0F) + add_val_LSCAN 
        
    else:
        print("\tMode = 0x%x --- Mode error ---" % mode)
        sys.exit()
        
    return mode, quantity_bytes, type_AKK 

def Out_ModeQuantity(mode, quantity_bytes):
    print("Mode:{0x%x}\t" % mode, end='')
    print("%s\t" % dctMode.get(mode), end='')
    if( (mode == bMODE_EMIT) or 
        (mode == bMODE_SCAN) or
        (mode == bMODE_IND) or 
        (mode == bMODE_SCAN) or 
        (mode == bMODE_AKK) ):
        print("Quantity bytes: %d" % quantity_bytes)
        
def Out_Mode_Quantity(mode, quantity_bytes):
    print("Mode:{0x%x}\t" % mode, end='')
    print("%s\t" % dctMode.get(mode), end='')
    print("Quantity bytes: %d" % quantity_bytes)        

###--------------------------------------------------------------------------   
  
def Get_FmBell(nparray, index):
    bell = nparray[index] & 0x80
    fm = nparray[index] & 0x0F        
    return fm, bell

def Out_FmBell(fm, bell):
    if( bell == BELL_PASS ): 
        print("\tBell: %s" % sBELL_PASS, end='')
    else:
        print("\tBell: %s" % sBELL_FAIL, end='')
    print("\tFM: %d\t\t%s" % (fm, sFM_NAME[fm]))
    
###--------------------------------------------------------------------------    

def Get_FmNumscan(nparray, index):
    num_scan = nparray[index] & 0x0F
    fm = (nparray[index] & 0xF0) >> 4        
    return fm, num_scan  
    
def Out_FmNumscan(fm, num_scan):            
    ###print("\n4\tnum_SCAN и FM: ", end=' ' ) 
    print("\tNumSCAN:{%d}\t\t %s" % (num_scan, sSCAN_N[num_scan-1]), end = '')  
    print("\tFM:{%d}\t\t%s" % (fm, sFM_NAME[fm]))

###--------------------------------------------------------------------------

def Get_FmEmit(nparray, index):
    form = nparray[index] & 0x0F
    fm = nparray[index+1] * 256
    fm = fm | nparray[index+2]         
    return fm, form
    
def Out_FmEmit(fm, form): 
    print("\tFM: %d\t\t%s" % (fm, sFM_NAME[form]))
    
###--------------------------------------------------------------------------

def Get_FloatFormat(nparray, index, mode):    
    sign = nparray[index] & 0x80
    type_ind = nparray[index] & 0x60
    if(mode == bMODE_IND):    
        unit = (nparray[index+1] & 0xF0) >> 4 
    elif(mode == bMODE_SCAN):
        unit = UNIT6 >> 4

    val = (nparray[index] & 0x0F)*1000.0
    val = val + (nparray[index+1] & 0x0F)*100.0
    val = val + ((nparray[index+2] & 0xF0) >> 4 )*10.0
    val = val + (nparray[index+2] & 0x0F)
    
    if(type_ind == IND5):
        val = val / 1000.0
    elif(type_ind == IND6):
        val = val / 100.0
    elif(type_ind == IND7):
        val = val / 10.0 
        
    if( sign != 0x80 ): 
        val = val * (-1.0)    
  
    return val, type_ind, unit 
  
def Out_FloatFormat(val, type_ind, unit):    
    if(type_ind == IND5):
        print("%4.3f" % val, end=' ')  
    elif(type_ind == IND6):
        print("%4.2f" % val, end=' ')  
    elif(type_ind == IND7):
        print("%4.1f" % val, end=' ')  
    else:
        print("%4.0f" % val, end=' ') 
        
    print("%s" % sUNIT[unit])    

###--------------------------------------------------------------------------    

def Get_EmitFmNumscan(nparray, index):
    fm = (nparray[index] & 0x0F) 
    num_scan = nparray[index+1] & 0x0F       
    return fm, num_scan  
    
def Out_EmitFmNumscan(fm, num_scan):            
    ###print("\n4\tnum_SCAN и FM: ", end=' ' ) 
    print("\tNumSCAN:{%d}\t\t %s" % (num_scan, sSCAN_N[num_scan-1]), end = '')  
    print("\tFM:{%d}\t\t%s" % (fm, sFM_NAME[fm]))
    
###--------------------------------------------------------------------------
    
def Get_PowerEmit(nparray, index):    
    sign = nparray[index] & 0x80
    type_ind =IND5      #--- Только этот формат!!!
    unit = UNIT6 >> 4   #--- Только эти ед. изм.

    val = (nparray[index] & 0x7F)*1000
    val = val + ((nparray[index+1] & 0xF0) >> 4) * 100
    val = val + (nparray[index+1] & 0x0F) * 10
    
    if(type_ind == IND5):
        val = val / 1000.0
    elif(type_ind == IND6):
        val = val / 100.0
    elif(type_ind == IND7):
        val = val / 10.0         
        
    if( sign != 0x80 ): 
        val = val * (-1.0)    
  
    return val, type_ind, unit 
  
def Out_PowerEmit(val, type_ind, unit):    
    if(type_ind == IND5):
        print("%4.3f" % val, end=' ')  
        
    print("%s" % sUNIT[unit])        
    
###--------------------------------------------------------------------------
    
def Get_NumEmit(nparray, index):
    return nparray[index]

def Out_NumEmit(num_emit):
    print("\tNumber emitter:  %d" % num_emit) 
    
###--------------------------------------------------------------------------    

def Get_EmitLenWave(nparray, index):
    val = nparray[index] * 256
    val = val + (nparray[index+1])
    return val  

def Out_EmitLenWave(val): 
    print("Emit LEN_WAVE:\t %d" % val)      
        
###-------------------------------------------------------------------------- 

def Get_AutoStat(nparray, index):
    tauto_stat = nparray[index] & 0x80 
    timeauto = nparray[index] & 0x0F 
    return tauto_stat, timeauto

def Out_AutoStat(tauto_stat, timeauto):    
    if( tauto_stat == 0x80 ): 
        print("\tЗаряд: %s" % sTAUTO_STAT_ON, end='\t')
    else:
        print("\tЗаряд: %s" % sTAUTO_STAT_OFF, end='\t')
    print("\tTIME_AUTO: %d" % timeauto)      

###-------------------------------------------------------------------------- 

def Get_EcoStat(nparray, index):
    teco_stat = nparray[index] & 0x80 
    timeeco = nparray[index] & 0x0F 
    return teco_stat, timeeco

def Out_EcoStat(teco_stat, timeeco):    
    if( teco_stat == 0x80 ): 
        print("\tКанал USB: %s" % sTECO_STAT_ON, end='\t')
    else:
        print("\tКанал USB: %s" % sTECO_STAT_OFF, end='\t')
    print("TIME_ECO: %d" % timeeco) 

###--------------------------------------------------------------------------    

def Get_LenWave(nparray, index):
    val = nparray[index] * 1000
    val = val + (nparray[index+1] & 0x0F) * 100
    val = val + (nparray[index+2] >> 4) * 10
    val += (nparray[index+2] & 0x0F)       
    return val  

def Out_LenWave(val): 
    print("LEN_WAVE: %d" % val)  

###--------------------------------------------------------------------------
'''    
def Get_AkkVolt(nparray, index):
    val16 = nparray[index] * 256
    val16 += nparray[index+1]                
    return val16

def Out_AkkVolt(mvolt):
    print("\t\tMvolt: %4.2f v" % (mvolt / 1000.0) )      
    
    
def Get_EmitAkkVolt(nparray, index):
    emit_val = (nparray[index] & 0x0F) * 100
    emit_val += ((nparray[index+1] & 0xF0) >> 4) * 10
    emit_val += (nparray[index+1] & 0x0F)
    return emit_val

def Out_EmitAkkVolt(mvolt):
    print("\t\tMvolt: %4.2f v" % (mvolt / 100.0) )  
'''
    
###--- AKK {надо заменить на сохранение в список !!!} -----------------------
def Get_AkkVolts(nparray, index):
    lst = []
    val16 = nparray[index] * 256
    val16 += nparray[index+1] 
    lst.append(val16)   
    val16 = nparray[index+2] * 256
    val16 += nparray[index+3] 
    lst.append(val16)
    val16 = nparray[index+4] * 256
    val16 += nparray[index+5] 
    lst.append(val16)              
    return lst 

def Out_AkkVolts(mvolts):
    i = 0
    for el in mvolts:
        print("\t\tMvolt[%i]: %4.2f v" % (i, el / 1000.0) )     
        i += 1
    
###--------------------------------------------------------------------------
   
def Get_FullStatus(nparray, index):
    sStatus = []
    stat = nparray[index]
    if(stat & bit_SCAN == bit_SCAN):
        sStatus.append(sON_SCAN)
    else:
        sStatus.append(sOFF_SCAN)    
    if(stat & bit_USB == bit_USB):
        sStatus.append(sON_USB)
    else:
        sStatus.append(sOFF_USB)            
    if(stat & bit_SIMMETR == bit_SIMMETR):
        sStatus.append(sON_SIMMETR)
    else:
        sStatus.append(sOFF_SIMMETR)          
    if(stat & bit_AKKDATA == bit_AKKDATA):
        sStatus.append(sON_AKKDATA)
    else:
        sStatus.append(sOFF_AKKDATA) 
            
    return stat, sStatus
 
def Out_FullStatus(sStatus):
    print(sStatus)
        
###========================================================================== 
    
def os_work():
    str_c.clear()
    cur_path = os.getcwd()  
    print("Current directory: %s" % cur_path)  
    
###--------------------------------------------------------------------------    
    
def change_port():
    str_c.zagolovok('Get port from list:')
    nmport = 0
    my_ports = []
    if(os.name=="posix") :
        for i in range(NUMPORTS):
            ###self.comboBox.addItem("/dev/ttyACM{}".format(i))
            pass
    else:
        #--- Windows
        listports = list_ports.comports()
        for port in listports:
            st_port = str(port)
            st_port = st_port[:st_port.index(' ')]
            my_ports.append(st_port)
            print("%5s -> %d" % (st_port, nmport))
            nmport += 1

    err = 0
    while err == 0:
        numport = int(input('Get port by numb:'))
        if(numport < nmport):
            err = 1
            prt = my_ports[numport]
            print('Now port is: %s' % (prt))
            print()
        else:
            print('Err: Noch einmall!')
        
    return prt

###--------------------------------------------------------------------------

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
      #ser.close() 
      sys.exit()        

###--------------------------------------------------------------------------    

def ComPort_Work(ser):  

    #--- До прихода bBegin байта {0x7E} и переводим start = 1
    #--- потом ждем 2-го байта с количеством байт в посылке
    start = 0
    fl_stop = 0   
    #--- должно быть в приходе        
    quantity_bytes = 0
    #--- реально пришлых байт
    cnt_bytes = 0
    
    ser.flushInput()
    
    #--- Цикл вычитывания посылки и ее обработка 
    while fl_stop == 0:
        
        #--- буфер для прихода
        lst = []
        #--- Забрать данные из буфера порта, как только появятся  
        if (ser.in_waiting > 0):
            lin = ser.read(ser.in_waiting)
            
            for el in lin:   
                if (el == bBEGIN and start == 0):
                    #--- Наконец встречен стартовый символ. Старт!!!
                    lst.append(el)
                    #--- наращивая количество принятых реально байт
                    cnt_bytes += 1
                    #--- Взвод флажка и переход к ловле блох
                    start = 1  
                    
                else:
                    #--- Запомнить оглашенное в посылке к-во бвйт
                    if(cnt_bytes == 1):
                        if(el & 0xF0 == bMODE_AKK):
                            if(el & 0x0F == 0):
                                quantity_bytes = (el & 0x0F) + add_val_INDAKK
                            else:
                                quantity_bytes = (el & 0x0F) + add_val_LAKK
                        elif(el & 0xF0 == bMODE_IND):  
                            quantity_bytes = (el & 0x0F) + add_val_IND 
                        elif(el & 0xF0 == bMODE_SCAN):    
                            quantity_bytes = (el & 0x0F) + add_val_SCAN 
                        elif(el & 0xF0 == bMODE_EMIT):  
                            quantity_bytes = (el & 0x0F) + add_val_EMIT  
                        elif(el & 0xF0 == bMODE_LSCAN):  
                            quantity_bytes = (el & 0x0F) + add_val_LSCAN    
       
                    #--- и продолжить наполнять список    
                    lst.append(el)
                    #--- наращивая количество принятых реально байт
                    cnt_bytes += 1
                    #--- ставим точки от скуки
                    print(".", end = " ")                     
                    
                      
            sleep(0.002) 
                
            print("cnt_bytes = %d" % cnt_bytes)                
    
            #--- Обрезаем лишние байты с конца списка
            lst = lst[0:quantity_bytes]
            #--- Показать приход      
            Print_Codes(lst)
               
            #--- Парсерить приход 
            Parser(lst)
                  
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
    #str_c.clear()
    os_work() 
  
    PORT = change_port()

    cnt = MAX_REPEAT
    while cnt:    
        ser = ComPort_Open(PORT)
        ComPort_Work(ser)        
        ComPort_Stop(ser)
        
        cnt-=1    

           
###==========================================================================
if __name__ == "__main__":
    # выполнить только в том случае, 
    # если выполняется как сценарий
    main()

