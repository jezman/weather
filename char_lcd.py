#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_CharLCD as LCD
import psycopg2
from pyowm import OWM
from time import sleep

# В ПОМЕЩЕНИИ
msg_in_room = ('\x42 \xA8\x4F\x4D\x45\xE2\x45\x48\xA5\xA5')
# ВЛАЖНОСТЬ
msg_humidity = ('\x42\xA7\x41\xA3\x48\x4F\x43\x54\x62')
# ОБНОВЛЕНО В
msg_update_time = ('\x4F\xA0\x48\x4F\x42\xA7\x45\x48\x4F \x42')
# ЗА БОРТОМ
msg_outside = ('\xA4\x41 \xA0\x4F\x50\x54\x4F\x4D')
# СКОРОСТЬ ВЕТРА
msg_wind_speed = ('\x42\x45\x54\x45\x50')

lcd_rs = 7
lcd_en = 8
lcd_d4 = 24
lcd_d5 = 17
lcd_d6 = 27
lcd_d7 = 22
lcd_backlight = 23

lcd_columns = 20
lcd_rows = 4

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                           lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

API_key = 'your open weather map API key'
owm = OWM(API_key, language='en')
obs = owm.weather_at_place('Moscow,ru')


def select():
    connect = psycopg2.connect(database='db_name', user='user_name',
                               host='ip_addr', password='password')
    sel = connect.cursor()
    sql_select = ('SELECT temp, humidity, time FROM week_temp\
                   order by time desc limit 1;')
    sel.execute(sql_select)
    return sel.fetchone()
    connect.close()


def show_message(message):
    lcd.message(message)
    sleep(14)
    lcd.clear()


current = obs.get_weather()
current_humidity = current.get_humidity()
current_wind = current.get_wind()
current_temp = current.get_temperature(unit='celsius')
current_status = current.get_status()

hourly_time = []
hourly_temp = []
hourly_status = []
forecast_hourly = owm.three_hours_forecast('Moscow,ru')
hourly = forecast_hourly.get_forecast()

forecast_time = []
forecast_temp = []
forecast_status = []
forecast_daily = owm.daily_forecast('Moscow,ru', limit=4)
daily = forecast_daily.get_forecast()


def forecast(time, temp, status, range):
    for weather in range:
        time.append(weather.get_reference_time('iso'))
        temp.append(weather.get_temperature(unit='celsius'))
        status.append(weather.get_status())


try:
    temp_in_room = ('{in_room}: {temp}\x99\x43\n\
                     {msg_hum}: {humidity}%\n\n{msg_time}: {data}'
                    .format(temp=select()[0],
                            humidity=select()[1],
                            data=select()[2][11:16],
                            in_room=msg_in_room,
                            msg_hum=msg_humidity,
                            msg_time=msg_update_time))
except:
    temp_in_room = ('Temperature server\nis unavailable')

temp_today = ('{outside}: {temp:.0f}\x99C\n\
               {wind}: {speed:.0f}\xBC/c\n\
               {msg_hum}: {humidity}%\n{status}'
              .format(outside=msg_outside,
                      temp=current_temp['temp'],
                      wind=msg_wind_speed,
                      speed=current_wind['speed'],
                      msg_hum=msg_humidity,
                      humidity=current_humidity,
                      status=current_status.upper()))


forecast(hourly_time, hourly_temp, hourly_status, hourly)

forecast_hourly = ('{data_0}: {temp_0:.0f}\x99C {status_0}\n\
                    {data_1}: {temp_1:.0f}\x99C {status_1}\n\
                    {data_2}: {temp_2:.0f}\x99C {status_2}\n\
                    {data_3}: {temp_3:.0f}\x99C {status_3}'
                   .format(data_0=hourly_time[0][11:16],
                           temp_0=hourly_temp[0]['temp'],
                           status_0=hourly_status[0].upper(),
                           data_1=hourly_time[1][11:16],
                           temp_1=hourly_temp[1]['temp'],
                           status_1=hourly_status[1].upper(),
                           data_2=hourly_time[2][11:16],
                           temp_2=hourly_temp[2]['temp'],
                           status_2=hourly_status[2].upper(),
                           data_3=hourly_time[3][11:16],
                           temp_3=hourly_temp[3]['temp'],
                           status_3=hourly_status[3].upper()))


forecast(forecast_time, forecast_temp, forecast_status, daily)

forecast_daily = ('{data_0}: {min_0:.0f}-{max_0:.0f}\x99C {status_0}\n\
                   {data_1}: {min_1:.0f}-{max_1:.0f}\x99C {status_1}\n\
                   {data_2}: {min_2:.0f}-{max_2:.0f}\x99C {status_2}\n\
                   {data_3}: {min_3:.0f}-{max_3:.0f}\x99C {status_3}'
                  .format(data_0=forecast_time[0][5:10],
                          min_0=forecast_time[0]['min'],
                          max_0=forecast_time[0]['max'],
                          status_0=forecast_time[0].upper(),
                          data_1=forecast_time[1][5:10],
                          min_1=forecast_time[1]['min'],
                          max_1=forecast_time[1]['max'],
                          status_1=forecast_time[1].upper(),
                          data_2=forecast_time[2][5:10],
                          min_2=forecast_time[2]['min'],
                          max_2=forecast_time[2]['max'],
                          status_2=forecast_time[2].upper(),
                          data_3=forecast_time[3][5:10],
                          min_3=forecast_time[3]['min'],
                          max_3=forecast_time[3]['max'],
                          status_3=forecast_time[3].upper()))


show_message(temp_in_room)
show_message(temp_today)
show_message(forecast_hourly)
show_message(forecast_daily)
