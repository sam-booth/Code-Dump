# Clock example with NTP synchronization
#
# This abomination is a melding of Pimoroni's example clock and rainbow projects
# While mostly copied code, it was annoying enough to create I belive
# It's worth jotting down here for future reference.
#

# Clock example with NTP synchronization
#
# Create a secrets.py with your Wifi details to be able to get the time
# when the Galactic Unicorn isn't connected to Thonny.
#
# secrets.py should contain:
# WIFI_SSID = "Your WiFi SSID"
# WIFI_PASSWORD = "Your WiFi password"
#
# Clock synchronizes time on start, and resynchronizes if you press the A button

import rp2
import time
import math
import machine
import network
import ntptime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

wifi_available = True


# create galactic object and graphics surface for drawing
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# create the rtc object
rtc = machine.RTC()

width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

# set up some pens to use later
WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0, 0, 0)


hue_map = [from_hsv(x / width, 1.0, 1.0) for x in range(width)]
hue_offset = 0.0
# Adjust the level of rainbow
stripe_width = 9

# set the font & brightness
graphics.set_font("bitmap8")
gu.set_brightness(0.3)

@micropython.native  # noqa: F821
def from_hsv(h, s, v):
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    i = int(i) % 6
    if i == 0:
        return int(v), int(t), int(p)
    if i == 1:
        return int(q), int(v), int(p)
    if i == 2:
        return int(p), int(v), int(t)
    if i == 3:
        return int(p), int(q), int(v)
    if i == 4:
        return int(t), int(p), int(v)
    if i == 5:
        return int(v), int(p), int(q)


# function for drawing a gradient background
@micropython.native  # noqa: F821
def gradient_background():
    global hue_offset, phase
    phase_percent = phase / 1
    for x in range(width):
        colour = hue_map[int((x + (hue_offset * width)) % width)]
        for y in range(height):
            v = (math.sin((x + y) / stripe_width + phase_percent) + 1.5) / 2.5

            graphics.set_pen(
                graphics.create_pen(
                    int(colour[0] * v), int(colour[1] * v), int(colour[2] * v)
                )
            )
            graphics.pixel(x, y)
gu.update(graphics)


# function for drawing outlined text
def outline_text(text, x, y):
    graphics.set_pen(BLACK)
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)

    graphics.set_pen(WHITE)
    graphics.text(text, x, y, -1, 1)


# Connect to wifi and synchronize the RTC time from NTP
def sync_time():
    if not wifi_available:
        return

    # Start connection

    rp2.country('UK')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect("lol", "nope")
    print(wlan.ifconfig())

    # Wait for connect success or failure
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(0.2)

        redraw_display_if_reqd()
        gu.update(graphics)

    if max_wait > 0:
        print("Connected")

        try:
            ntptime.settime()
            print("Time set")
        except OSError:
            pass

    wlan.disconnect()
    wlan.active(False)

utc_offset = 1

year, month, day, wd, hour, minute, second, _ = rtc.datetime()
last_second = second
phase = 0

# Check whether the RTC time has changed and if so redraw the display
def redraw_display_if_reqd():
    global year, month, day, wd, hour, minute, second, last_second

    year, month, day, wd, hour, minute, second, _ = rtc.datetime()
    if second != last_second:
        gradient_background()
        hour = (hour + utc_offset) % 24
        clock = "{:02}:{:02}:{:02}".format(hour, minute, second)
        # calculate text position so that it is centred
        w = graphics.measure_text(clock, 1)
        x = int(width / 2 - w / 2 + 1)
        y = 2
        outline_text(clock, x, y)

    last_second = second

sync_time()

while True:
    redraw_display_if_reqd()
    # update the display
    gu.update(graphics)
    time.sleep(0.05)
