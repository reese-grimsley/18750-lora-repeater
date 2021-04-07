###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option

import time
import rak811v2
import messages

Rak811v2 = rak811v2.Rak811v2

## Device address
dev_addr = 0x01 ## Client


### Setting configs
print('init')

lora = Rak811v2()

print('Reset radio')
lora.hard_reset()

print('Get version')
v = lora.version
print(v[0])


print('\nSet configuration modes for LoRa p2p')
lora.set_config('lora:work_mode:1')
resp = lora.get_info()
# print(resp)
for x in resp:
    print('\t',x)


print('\nSet self as receiver mode')
lora.set_config('lorap2p:transfer_mode:1')
resp = lora.get_info()
# print(resp)
for x in resp:
    print('\t',x)


print('\nSet P2P parameters')
lora.set_config('lorap2p:915000000:10:0:1:8:16')
resp = lora.get_info()
for x in resp:
    print('\t',x)


### Receiving
print('print recv events')
i=0
while True:
    print()
    print('loop iter %d' % i)
    print()
    try: 
        events = lora.get_events(timeout=5)
        for event in events:
            print(event)
            if 'at+recv' in event:
                #we received a message. Let's decode. 
                ## e.g. at+recv=-72,7,26:48656C6C6F20576F726C6421206D736720636E743A2032310D0A; -72 is RSSI, 7 is SNR, and 26 is #bytes
                header = event.split('=')[-1].split(':')[0].split(',')
                rssi = header[0]
                snr = header[1]
                num_bytes = header[2]

                data = event.split(':')[-1] #get what's to th e righ o the parameters
                print(f'Data is supposed to be {num_bytes} and we have {len(data)} hex characters')

                # decoded_data = bytes.fromhex(data).decode('ASCII')
                # print('Received: %s' % decoded_data)


                message = messages.RXMessage(data)

                # only if dev address and dest address in packet matches, else discard
                if message.get_addr() == dev_addr:
                    decoded_data = message.get_payload()
                    print('Received: %s' % decoded_data)


    except rak811v2.serial.Rak811v2TimeoutError as e:
        print('timeout on RX')
        # print(e)

    i+=1