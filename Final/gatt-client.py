#!/usr/bin/python

import argparse
import dbus
import gobject
import sys

from dbus.mainloop.glib import DBusGMainLoop

bus = None
mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'

HR_SVC_UUID =        '12345678-1234-5678-1234-56789abcdef0'
HR_MSRMT_UUID =      '12345678-1234-5678-1234-56789abcdef1'

# The objects that we interact with.
pos_service = None
pos_msrmt_chrc = None


def generic_error_cb(error):
    print('D-Bus call failed: ' + str(error))
    mainloop.quit()

def position_val_cb(value):
    if len(value) != 1:
        print "Invalid position value: "+ repr(value)
        return

    print 'Position value: ' + repr(value)

def start_client():
    pos_msrmt_chrc.ReadValue(reply_handler=position_val_cb,
            error_handler=generic_error_cb,
            dbus_interface=GATT_CHRC_IFACE)
