# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:10:11 2023

USB_finder

@author: ln.starmark@ekatra.io
       : ln.starmark@gmail.com
"""

'''
import sys
import usb.core
import usb.util
import usb.backend.libusb1
'''

import wmi

#--- Я подключаю вот такой виртуал ком порт
#--- USB\VID_1A86&PID_7523\7&32E82906&0&3

VENDOR_ID = 0x1a86      # OnTrak Control Systems Inc. vendor ID
PRODUCT_ID = 0x7523     # Device product name

'''
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if device is None:
    raise ValueError('Device not found. Please ensure it is connected to the tablet.')
    print('Device not found. Please ensure it is connected to the tablet.')
    sys.exit(1)
else:
    print(device)
'''

c = wmi.WMI()
for os in c.Win32_OperatingSystem():
    print(os.Caption)

'''
for s in c.Win32_Service ():
    if s.State == 'Stopped':
        print(s.Caption, s.State)
'''       
'''
# Construct the query to find the device
query = f'SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE "%VID_{VENDOR_ID}%&PID_{PRODUCT_ID}%"'

# Execute the query and iterate through the results
for device in c.query(query):
    # Print the attributes of the USB device
    print(f"Device ID: {device.DeviceID}")
    print(f"Name: {device.Name}")
    print(f"Description: {device.Description}")
    print(f"Manufacturer: {device.Manufacturer}")
    print(f"Hardware ID: {device.HardwareID}")
    print("Serial number: " + device.PNPDeviceID.split('\\')[-1])
    print()
'''    