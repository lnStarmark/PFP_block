# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:14:29 2023

@author: admin
"""

import usb.core
import usb.util
import win32api

VENDOR_ID = 0x0483      # OnTrak Control Systems Inc. vendor ID
PRODUCT_ID = 0x374B     # Device product name

#VENDOR_ID = 0x1a86      # OnTrak Control Systems Inc. vendor ID
#PRODUCT_ID = 0x7523     # Device product name

#VENDOR_ID = 0x10c4      # OnTrak Control Systems Inc. vendor ID
#PRODUCT_ID = 0xea60     # Device product name

win32api.Beep(500, 500)

# find our device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)


# was it found?
if dev is None:
    raise ValueError('Device not found')
else:
    stdev = str(dev)
    print(stdev)
    print("-----------------------------------------------------------------")
    lst_dev = stdev.split("\n")
    sl_dev = lst_dev[:15]
    for el in sl_dev:
        print(el)
    #print(lst_dev)
  
    
    
'''
USB\VID_1A86&PID_7523\7&32E82906&0&3

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')


oem50.inf:WinChipHead.NTamd64:CH341SER_Inst.NTamd64:3.4.2014.8:usb\vid_1a86&pid_7523

'''