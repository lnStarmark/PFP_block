# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:50:41 2023

@author: admin
"""
import sys
import usb
import usb.core
import usb.util
import win32api

#VENDOR_ID = 0x1A86      # vendor ID
#PRODUCT_ID = 0x7523     # Device product name

VENDOR_ID = 07E5
PRODUCT_ID = 7530
###IZM-105.21.04  = Вимірювач
###L-103.21.04  = Джерело випромінювання

Device_ID = ""
Serial_N = ""

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
    
    win32api.Beep(500, 500)
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
     
    return Dev_ID, Ser_N , stdev  

def Echo_to_USB():
    global Device_ID
    global Serial_N
    global InfoAddText
    global NameDevText
    global ind_mova
    
    Device_ID, Serial_N , full_info = USB_GetID(VENDOR_ID, PRODUCT_ID)
    
    print(full_info ) 
    #print("Device: %s;\tSerial: %s" % (Device_ID, Serial_N) ) 
    
    with open('result.txt', 'w+') as f:
        f.write(full_info)
    
    
    
def main():
    Echo_to_USB()
    
###==========================================================================
if __name__ == "__main__":
    # выполнить только в том случае, если выполняется как сценарий
    main()    