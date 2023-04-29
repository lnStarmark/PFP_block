# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:11:37 2023

@author: admin
"""

import usb.core
import usb.util
import sys
#import swd
import usb

def main ():
    devices = []
    # dev = usb.core.find(idVendor = 0x0483, idProduct = 0x374B, iProduct = 0x5, find_all = True)
#    dev = usb.core.find(find_all = True)
    dev = usb.core.find(idVendor=0x1a86, idProduct=0x7523)
    dev.reset() 
    for device in dev:
        try:
            devices.append (device)
            print (hex(dev.idVendor), hex(dev.idProduct), dev.serial_number)
        except:
            pass
        
    # STLink = swd.Swd (swd_frequency=4000000, serial_no='')
    # print (STLink)


if  __name__ == 'main':
    sys.exit(main())