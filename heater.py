import time
import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
import urllib.request

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
p = GPIO.PWM(16, 50)
p.start(0)

THINGSPEAKKEY = 'RCV6DZ63J9D824GG'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

while True:
    try:
        humidity, temperature = DHT.read_retry(11, 10)
        print('Temp: {} C  Humidity: {}%'.format(temperature, humidity))
        urllib.request.urlopen('{}?api_key={}&field1={}&field2={}'.format(THINGSPEAKURL, THINGSPEAKKEY, temperature, humidity))
        if temperature < 20:
            p.ChangeDutyCycle(25)
            urllib.request.urlopen('{}?api_key={}&field3={}'.format(THINGSPEAKURL, THINGSPEAKKEY, 75))
        elif temperature > 22:
            p.ChangeDutyCycle(75)
            urllib.request.urlopen('{}?api_key={}&field3={}'.format(THINGSPEAKURL, THINGSPEAKKEY, 25))
        else:
            p.ChangeDutyCycle(0)
            urllib.request.urlopen('{}?api_key={}&field3={}'.format(THINGSPEAKURL, THINGSPEAKKEY, 100))
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
