###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option

import messages
import time
import rak811v2
Rak811v2 = rak811v2.Rak811v2


## Device address
dev_addr = 0x02 ## Client

### Destination address
dest_addr = 0x01 ## Gateway

#### Setting configs
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


print('\nSet self as sender mode')
lora.set_config('lorap2p:transfer_mode:2')
resp = lora.get_info()
# print(resp)
for x in resp:
    print('\t',x)


print('\nSet P2P parameters')
lora.set_config('lorap2p:915000000:10:0:1:8:16')
resp = lora.get_info()
for x in resp:
    print('\t',x)


#### End of configs

### Messages to transmit

i=1
while True:
    print()
    print('loop iter %d' % i)
    print()
    
    str_to_send = "Hello World! msg cnt: %d\r\n" % i
    print('Sending "%s"' % str_to_send)

    ##Insert temeperature sensing code
    ##take timestamp time.time() or datetime (former is sufficient, and produces a double; units are seconds)
    ##Configure message to send as either a string or a sequence of 'bytes'; bytes will be more compact 
    ##Log to CSV, with timestamp, frame_count, dest_addr, this address, and the payload bytes

    message = messages.TXMessage(i, dest_addr, dev_addr, str_to_send)
    tx_bytes = message.get_bytes()

    # lora.send_lorap2p(str_to_send)
    lora.send_lorap2p(tx_bytes)
    print('Sent')

    time.sleep(30)
    i+=1