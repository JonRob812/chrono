from machine import ADC, Pin, freq, Timer
from time import sleep, ticks_ms, ticks_us, ticks_diff
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


def fps(us, d=dist):
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
                    f = fps(ticks_diff(eye_2_detect, eye_1_detect))
                    print('fps', f)
                    sleep(1)


def do():
    x = ticks_us()
    sleep(.03)
    print(ticks_diff(ticks_us(), x))


while True:
    print(eye_1.read(), ' | ', eye_2.read())







