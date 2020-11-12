from machine import ADC, Pin
from time import sleep
eye_1 = ADC(Pin(32))
eye_2 = ADC(Pin(33))
eye_1.atten(ADC.ATTN_0DB)
eye_2.atten(ADC.ATTN_0DB)


while True:
    print(eye_1.read(), ' | ', eye_2.read())


print(eye_1.read())
thresh = 3
stop = False
reads = []

while not stop:
    x = eye_1.read()
    reads.append(x)
    if len(reads) > thresh:
        reads.pop(0)
    if sum(reads) < 1:
        stop = True

def detect():
    thresh = 3
    stop = False
    reads = []

    while not stop:
        x = eye_1.read()
        reads.append(x)
        if len(reads) > thresh:
            reads.pop(0)
        if sum(reads) < 1:
            stop = True
            print('bang')



while True:
    detect()
    sleep(1)


