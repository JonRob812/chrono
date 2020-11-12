import home_wifi
from machine import ADC, Pin, freq, Timer
from time import sleep, ticks_ms, ticks_diff, time
from mqtt_simple import MQTTClient
import gc
gc.collect()

server = '192.168.0.0'

freq(240000000)
eye_dist = 3

eye_1 = ADC(Pin(32))
eye_2 = ADC(Pin(33))
eye_1.atten(ADC.ATTN_0DB)
eye_2.atten(ADC.ATTN_0DB)

client = MQTTClient('Chr0n0', server)
connected = False
try:
    client.connect()
    connected = True
except:
    pass


def fps(ms, d=eye_dist):
    seconds = ms / 1000
    d_feet = d / 12
    print('seconds', seconds, 'feet', d_feet)
    return (1 / seconds) * d_feet


def detect(eye, low_thresh):
    if eye.read() < low_thresh:
        return ticks_ms()
    else:
        return False


def smart_detect(low_thresh, ms_period):
    while True:
        eye_1_detect = detect(eye_1, low_thresh)
        if eye_1_detect:
            while ticks_diff(ticks_ms(), eye_1_detect) < ms_period:
                eye_2_detect = detect(eye_2, low_thresh)
                if eye_2_detect:
                    f = fps(ticks_diff(eye_2_detect, eye_1_detect))
                    print('fps', f)
                    return f


def measure_loop_forever():
    while True:
        feet_per_second = smart_detect(200, 100)
        print(feet_per_second)
        """do the magic"""
        if connected:
            client.publish(b'chrono', str(fps).encode())


measure_loop_forever()



