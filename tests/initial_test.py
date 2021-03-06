import os, sys, math, time

from rak811 import Mode, Rak811
import serial

def test_rx(frequency):
    pass

    lora = Rak811()
    lora.hard_reset()
    lora.mode = Mode.LoRaP2P

    lora.rf_config = {
        'sf': 9,
        'freq': frequency,
        'pwr': 16
    }

    print('config created')
    wait = 30


    lora.rxc()

    while True:
        print(f'LoRa set to receive; waiting for {wait}s')

        lora.rx_get(wait)
        while lora.nb_downlinks > 0:
            message = lora.get_downlink()    
            data = message['data']

            print(data)
            print(type(data))
            print('RSSI: {}, SNR: {}'.format(message['rssi'], message['snr']))





def main():
    print('main')
    test_rx(915.0)

if __name__ == "__main__":
    main()
