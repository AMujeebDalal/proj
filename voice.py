import socket
import bluetooth
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BULB = 21
GPIO.setup(BULB, GPIO.OUT)
GPIO.output(BULB, GPIO.HIGH)
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(('', 1))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print('Accepted connection from: ', address)

while True:
    data = client_socket.recv(2, socket.MSG_WAITALL).lower()
    print('Received: ', data)
    if data == b'go':
        print('LED ON')
        GPIO.output(BULB, GPIO.LOW)
    elif data == b'no':
        print('LED OFF')
        GPIO.output(BULB, GPIO.HIGH)
    elif data == b'qq':
        print('Quit')
        GPIO.cleanup()
        break

client_socket.close()
server_socket.close()
