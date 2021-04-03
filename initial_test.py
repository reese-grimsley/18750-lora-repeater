import os, sys, math, time

from rak811 import Mode, Rak811
import serial

def test_rx(frequency):
    pass

    lora = Rak811()
    lora.hard_reset()
    lora.mode = Mode.



def main():
    print('main')
    test_rx(930000000)

if __name__ == "__main__":
    main()
