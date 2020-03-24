from time import sleep
from machine import Pin

led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)

print('blinking the LEDs...')
i = 0

while True:
    i += 1
    led1.on()
    led2.off()
    sleep(0.5)
    led1.off()
    led2.on()
    sleep(0.5)
    print(i)

