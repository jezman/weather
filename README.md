1. Raspberry Pi 3
2. [LCD Screen MT-20S4A 20x4](http://www.melt.com.ru/docs/MT-20S4A.pdf) (Made in Russia). Based on HD44780.
3. [Ralay switch RTD14005](http://www.mouser.com/ds/2/418/NG_DS_RT1_1014-729126.pdf)
4. [DHT11 Humidity & Temperature Sensor](http://www.dfrobot.com/image/data/DFR0067/DFR0067_DS_10_en.pdf)

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

current_time = time.strftime('%H')
br = GPIO.PWM(lcd_pin, 50)
br.start(0)

try:
    while True:
        if '07' < current_time < '17':
            br.ChangeDutyCycle(100)
        else:
            br.ChangeDutyCycle(50)
    time.sleep(900)
except KeyboardInterrput:
    pass

br.stop()
GPIO.cleanup(18)
```
