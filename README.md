LCD Screen [MT-20S4A 20x4](http://www.melt.com.ru/docs/MT-20S4A.pdf) (Made in Russia). Based on HD44780.

| LCD Pin| Pin assignment | Raspberry Pi 2/3 |
|:---:|:-----------------:|:--------------:|
| 1  | GND                |            GND |
| 2  | +3V/5V             |           +5V  |
| 3  | Uo                 | GPIO 23/Pin 16 |
| 4  | Ao                 | GPIO 7/Pin 26  |
| 5  | R/W                |            GND |
| 6  | E                  |  GPIO 8/Pin 24 |
| 11 | DB4                | GPIO 24/Pin 18 |
| 12 | DB5                | GPIO 17/Pin 11 |
| 13 | DB6                | GPIO 27/Pin 14 |
| 14 | DB7                | GPIO 22/Pin 15 |
| 15 | +LED               | GPIO 18/ Pin 12|
| 16 | -LED               |           GND  |

* LCD Pin 7-10 not used.

### Relay switch to NC (normal closed)
```python
#!/usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(4, GPIO.OUT) # GPIO 4/ Pin 7 - Ralay.
GPIO.output(4, False)
GPIO.cleanup(4)
```
### Relay switch to NO (normal open)
```python
#!/usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(4, GPIO.OUT) # GPIO 4/ Pin 7 - Ralay.
GPIO.output(4, True)
```

### Brightness control
```python
#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

lcd_pin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lcd_pin, GPIO.OUT)

p = GPIO.PWM(lcd_pin, 50)
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup(18)
```
