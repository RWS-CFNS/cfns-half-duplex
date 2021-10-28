import serial
''''
project: Half-Duplex
author: Alfred Espinosa Encarnación
date: 30-03-2021

Description: Read data from a serial interface (UART). 
It receives AIS messages from the RX Receiver and prints them out.
'''
# Configurate serial connection
COM = "COM4"
ser = serial.Serial(
    port=COM, baudrate=38400, bytesize=8, stopbits=serial.STOPBITS_ONE
)
ser.flushInput()

print("Serial is open: " + str(ser.isOpen()))

print("Now starting loop")
while True:
    try:
        ser_bytes = ser.readline()
        print(ser_bytes)
    except:
        print("Keyboard Interrupt")
        break
