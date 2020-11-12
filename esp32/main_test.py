from machine import ADC, Pin, freq, Timer
from time import sleep, ticks_ms, ticks_diff
from mqtt_simple import MQTTClient
import gc
gc.collect()

freq(240000000)
dist = 3

eye_1 = ADC(Pin(32))
eye_2 = ADC(Pin(33))
eye_1.atten(ADC.ATTN_0DB)
eye_2.atten(ADC.ATTN_0DB)

detect_lim = 200
detect_count = 2


eye_1_last = None
eye_2_last = None


def timer_callback(t):
    global eye_1_last, eye_2_last
    x = detect(eye_1, detect_lim)
    y = detect(eye_2, detect_lim)
    if x:
        eye_1_last = x
    if y:
        eye_2_last = y
        diff = ticks_diff(eye_2_last, eye_1_last)
        f = fps(diff)
        print(f)


sense_timer = Timer(0)
sense_timer.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)


def fps(ms, d=dist):
    seconds = ms / 1000
    d_feet = d / 12
    print('seconds', seconds, 'feet', d_feet)
    return (1 / seconds) * d_feet


def detect_sum(eye):
    thresh = 3
    reads = []
    while True:
        x = eye.read()
        reads.append(x)
        if len(reads) > thresh:
            reads.pop(0)
        if sum(reads) < 1:
            return ticks_ms()


def detect_simple(eye, low_thresh):
    while eye.read() > low_thresh:
        pass
    return ticks_ms()


def detect(eye, low_thresh):
    if eye.read() < low_thresh:
        return ticks_ms()
    else:
        return False


def detect_loop(low_thresh, ms_period):
    while True:
        eye_1_detect = detect(eye_1, low_thresh)
        if eye_1_detect:
            while ticks_diff(ticks_ms(), eye_1_detect) < ms_period:
                eye_2_detect = detect(eye_2, low_thresh)
                if eye_2_detect:
                    f = fps(ticks_diff(eye_2_detect, eye_1_detect))
                    print('fps', f)


def detect_loop_simple():
    while True:
        eye_1_break = detect_sum(eye_1)
        eye_2_break = detect_sum(eye_2)
        time_ms = ticks_diff(eye_2_break, eye_1_break)

        print(fps(time_ms))









