from machine import ADC, Pin
from time import sleep
r_pin = ADC(Pin(32))
r_pin.atten(ADC.ATTN_0DB)

print(r_pin.read())
thresh = 3
stop = False
reads = []

while not stop:
    x = r_pin.read()
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
        x = r_pin.read()
        reads.append(x)
        if len(reads) > thresh:
            reads.pop(0)
        if sum(reads) < 1:
            stop = True
            print('bang')



while True:
    detect()
    sleep(1)


