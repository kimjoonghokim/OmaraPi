import bluetooth
import time
import RPi.GPIO as GPIO
from newMRC522 import SimpleMFRC522
from HR8825 import HR8825


reader = SimpleMFRC522() # Create an object of the class MFRC522
motor = HR8825(dir_pin=33, step_pin=35, enable_pin=32, mode_pins=(36, 11, 38)) # Create motor object


# findItem: takes in string representing item name, spins the motor 
# until the item is found (i.e RFID sensor reads the item) 
# Stops the motor and ends when item is found

def findItem(item):
    isDetected = False
    countCycle = 0
    while not isDetected:
        countCycle = countCycle + 1
        motor.TurnStep(Dir='forward', steps=25, stepdelay = 0.005)
        id, text = reader.read_no_block()
        modifiedText = str(text).replace(" ", "")
        modifiedItem = str(item).replace(" ", "")
        if id is not None:
            if str(modifiedText) == str(modifiedItem):
                motor.Stop()
                print(item+" found")
                isDetected = True
                break
            if str(modifiedText) != str(modifiedItem):
                print("Not "+item+", instead "+modifiedText)
        if countCycle > 750:
            motor.Stop()
            print("ERR: Item not found")
            isDetected = True
            break
            
            

# addItem: takes in string representing item name, writes the item to the RFID tag
def addItem(item):
   
        print("Called addItem")
        print("Now place your tag to write")
        reader.write(item)
        print("Written")
        


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 0
server_sock.bind(("", port))
server_sock.listen(1)
print("listening on port 0")
bluetooth.advertise_service(server_sock, "FooBar Service", "1e0ca4ea-299d-4335-93eb-27fcfe7fa848")
client_sock, address = server_sock.accept()
print("Accepted connection from ", address)
isConnected = True
try:
    while isConnected:
        data = client_sock.recv(1024).decode()
        print("Received: %s" % data)
        datasplit = data.split(":")
        if ("write:" in data):
            client_sock.send("Thanks")
            addItem(datasplit[1])
            client_sock.send("ACK")
        if("read:" in data):
            client_sock.send("Thanks")
            findItem(datasplit[1])
            client_sock.send("ACK")
        data = ""
        
    client_sock.close()
    server_sock.close()

finally:
    GPIO.cleanup()
    motor.Stop()
