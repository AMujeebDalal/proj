import time
from gpiozero import LightSensor, LED

ldr = LightSensor(4)
led = LED(17)

while True:
    light = ldr.value
    if light < .1:
        led.on()
    else:
        led.off()
    print(ldr.value)
