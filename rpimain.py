import bluetooth

#!/usr/bin/env python
import serial
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import bluetooth

#ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)
#ser.reset_input_buffer()
#reader = SimpleMFRC522()

def detectItem(text):
    boolDetected = False
    try:
        #ser.write(b"start\n")
        while (not boolDetected):
            id, text = reader.read()
            var = str(text).replace(" ", "")
            print(var)
            if(var == text):
                print(id)
                print(text)
                time.sleep(1)
                boolDetected = True
            else:
                print("Wrong Article")
    finally:
        GPIO.cleanup()

def addItem(text):
    try:
        print("Called addItem")
        #print("Now place your tag to write")
        #reader.write(text)
        #print("Written")
    finally:
        GPIO.cleanup()

isConnected = False
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 0
server_sock.bind(("", port))
server_sock.listen(1)
print("listening on port 0")
bluetooth.advertise_service(server_sock, "FooBar Service", "1e0ca4ea-299d-4335-93eb-27fcfe7fa848")
client_sock, address = server_sock.accept()
print("Accepted connection from ", address)
isConnected = True
while isConnected:
    data = client_sock.recv(1024).decode()
    print("Received: %s" % data)
    datasplit = data.split(":")
    if ("write:" in data):
        addItem(datasplit[1])
        client_sock.send("Thanks")
    if("read:" in data):
        detectItem(datasplit[1])
    data = ""

client_sock.close()
server_sock.close()

