###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option

import time
from rak811v2 import Rak811v2

print('init')

lora = Rak811v2()
print(lora._serial)
print(lora._serial._serial)
print(lora._serial._serial.port)
lora._serial._logger.setLevel(0)

lora.hard_reset()

lora._serial.send_command('help')


resp = lora.get_info()
# print(resp)
for x in resp:
    print('\t',x)


time.sleep(1)
print('try to set configuration modes for LoRa p2p')

lora.set_config('lora:work_mode:1')
resp = lora.get_info()
# print(resp)
for x in resp:
    print('\t',x)


print('try to set self as receiver')
lora.set_confg('lorap2p:transfer_mode:1')
resp = lora.get_info()
# print(resp)
for x in resp:
    print('\t',x)



lora.set_config('lorap2p:915000000:10:0:1:8:16')
resp = lora.get_info()
print(resp)
for x in resp:
    print('\t',x)


print('print recv events')
i=0
while True:
    print('loop iter %d' % i)
    event = lora.get_event(timeout=5)
    for x in event:
        print('\t',x)

    resp = lora.get_response(timeout=1)
    for x in resp:
        print('\t',x)

    i+=1