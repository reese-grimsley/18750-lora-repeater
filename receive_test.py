###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option

import time
import rak811v2
Rak811v2 = rak811v2.Rak811v2

print('init')

lora = Rak811v2()

print('Reset radio')
lora.hard_reset()

print('Get version')
v = lora.version
print(v[0])
print(v[1])


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


print('print recv events')
i=0
while True:
    print()
    print('loop iter %d' % i)
    print()
    try: 
        events = lora.get_events(timeout=5)
        for event in events:
            for x in event:
                print('\t',x)
    
    except Rak811v2.serial.Rak811v2TimeoutError as e:
        print('timeout on RX')
        print(e)


    # resp = lora.get_response(timeout=1)
    # for x in resp:
    #     print('\t',x)

    i+=1