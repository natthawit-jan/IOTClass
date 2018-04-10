# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 13:25:46 2017

@author: glassbox
"""

"""Module importation"""
import warnings
import serial
import serial.tools.list_ports
import time
import tkinter as tk
import simpleaudio as sa

def connect_arduino(baudrate=9600): # a more civilized way to connect to arduino
    def is_arduino(p):

        # need more comprehensive test
        return p.manufacturer is not None and 'arduino' in p.manufacturer.lower()

    ports = serial.tools.list_ports.comports()
    arduino_ports = [p for p in ports if is_arduino(p)]


    def port2str(p):
        return "%s - %s (%s)" % (p.device, p.description, p.manufacturer)

    if not arduino_ports:
        portlist = "\n".join([port2str(p) for p in ports])
        raise IOError("No Arduino found\n" + portlist)

    if len(arduino_ports) > 1:
        portlist = "\n".join([port2str(p) for p in ports])
        warnings.warn('Multiple Arduinos found - using the first\n' + portlist)

    selected_port = arduino_ports[0]
    print("Using %s" % port2str(selected_port))
    print(selected_port.device)
    ser = serial.Serial(selected_port.device, baudrate)
    time.sleep(2)  # this is important it takes time to handshake
    return ser

with connect_arduino() as ser:
    while True:

        data_in = ser.readline()
        print(data_in)


        if data_in == b'0\r\n':
            print("enter this")
            wave_obj = sa.WaveObject.from_wave_file("c1.wav")
            play_obj = wave_obj.play()
            print (data_in)



        elif data_in == b'1\r\n':
            wave_obj = sa.WaveObject.from_wave_file("d1.wav")
            play_obj = wave_obj.play()

        elif data_in == b'2\r\n':
            wave_obj = sa.WaveObject.from_wave_file("e1.wav")
            play_obj = wave_obj.play()

        elif data_in == b'3\r\n':
            wave_obj = sa.WaveObject.from_wave_file("f1.wav")
            play_obj = wave_obj.play()
