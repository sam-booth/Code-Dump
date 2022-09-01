import ntptime
from machine import RTC
import time
import utime

# Connect to wifi first

rtc = RTC()
ntptime.settime()
print (rtc.datetime()) # get date and time

year = utime.localtime()[0]
month = utime.localtime()[1]
day = utime.localtime()[2]
hourMin = (str(utime.localtime()[3]) + f'{utime.localtime()[4]:02}')

result = (str(year) + "/" + f'{month:02}' + "/" + str(day) + "/" + str(number))
