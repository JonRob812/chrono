import home_wifi
from machine import ADC, Pin, freq, Timer
from time import sleep, ticks_ms, ticks_diff, ticks_us
from mqtt_simple import MQTTClient
import gc
gc.collect()

server = '192.168.0.60'

freq(240000000)
eye_dist = 3

eye_1 = ADC(Pin(32))
eye_2 = ADC(Pin(33))
eye_1.atten(ADC.ATTN_0DB)
eye_2.atten(ADC.ATTN_0DB)

client = MQTTClient('Chr0n0', server)
connected = False
sleep(25)
try:
    client.connect()
    connected = True
    print('connected')
except:
    print('no connect')
    pass


def fps(us, d=eye_dist):
    seconds = us / 1000000
    d_feet = d / 12
    print('seconds', seconds, 'feet', d_feet)
    return (1 / seconds) * d_feet


def detect_simple(eye, low_thresh):
    while eye.read() > low_thresh:
        pass
    return ticks_us()


def detect(eye, low_thresh):
    if eye.read() < low_thresh:
        return ticks_us()
    else:
        return False


def detect_loop(low_thresh, us_period):

    while True:
        eye_1_detect = detect(eye_1, low_thresh)
        if eye_1_detect:
            while ticks_diff(ticks_us(), eye_1_detect) < us_period:
                eye_2_detect = detect(eye_2, low_thresh)
                if eye_2_detect:
                    print(ticks_diff(eye_2_detect, eye_1_detect))
                    return fps(ticks_diff(eye_2_detect, eye_1_detect))


def measure_loop_forever():
    while True:
        feet_per_second = detect_loop(50, 50000)
        print(feet_per_second)
        if connected:
            client.publish(b'chrono', str(round(feet_per_second,2)).encode())
        sleep(1)


measure_loop_forever()



