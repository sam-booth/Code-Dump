import rp2
import network
import machine

rp2.country('UK')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "SSSH_SECRET")
print(wlan.ifconfig())

do_whatever()
