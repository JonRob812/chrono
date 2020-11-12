
from machine import ADC, Pin, freq
from time import sleep, ticks_ms, ticks_diff

freq(240000000)
dist = 3

eye_1 = ADC(Pin(32))
eye_2 = ADC(Pin(33))
eye_1.atten(ADC.ATTN_0DB)
eye_2.atten(ADC.ATTN_0DB)

detect_lim = 200
detect_count = 2

print(eye_1.read())


def detect(eye):
    thresh = 3
    reads = []
    while True:
        x = eye.read()
        reads.append(x)
        if len(reads) > thresh:
            reads.pop(0)
        if sum(reads) < 1:
            return ticks_ms()

def fps(ms, d=dist):
    seconds = ms / 1000
    d_feet = d / 12
    print('seconds', seconds, 'feet', d_feet)
    return (1 / seconds) * d_feet


def main():
    while True:
        eye_1_break = detect(eye_1)
        eye_2_break = detect(eye_2)
        time_ms = ticks_diff(eye_2_break, eye_1_break)

        print(fps(time_ms))









