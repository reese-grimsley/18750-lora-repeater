###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option
import sys, os, time, itertools, csv
import messages
import rak811v2
import Adafruit_DHT
Rak811v2 = rak811v2.Rak811v2



if not os.path.isfile('results_client.csv'):
    with open('results_client.csv', 'w') as f:
        line = 'TIMESTAMP_SEND,SENDER_ADDRESS,DESTINATION_ADDRESS,FRAME_COUNT,TEMPERATURE,HUMIDITY,RAW_MESSAGE\r\n'
        f.write(line)

## Device address
dev_addr = 0x03 ## Client

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

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 27
#### End of configs

### Messages to transmit

i=1
while True:
    print()
    print('loop iter %d' % i)
    print()
    
    # str_to_send = "Hello World! msg cnt: %d, time: " % i
    # print('Sending "%s"' % str_to_send)
    # bytes_to_send = messages.str_to_bytes(str_to_send)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    print(temperature)
    print(humidity)
    print('Temperature and Humidity: \t %f, \t %f' % (temperature, humidity))
    timestamp_send = time.time()
    bytes_to_send = messages.double_to_bytes(temperature)
    bytes_to_send += messages.double_to_bytes(humidity)
    bytes_to_send += messages.double_to_bytes(timestamp_send)
    # bytes_to_send += messages.str_to_bytes('\r\n')


    # message = messages.TXMessage(i, dest_addr, dev_addr, str_to_send)
    message = messages.TXMessage(i, dest_addr, dev_addr, bytes_to_send)
    tx_bytes = message.get_bytes()

    ##TODO: log information into csv as well

    # lora.send_lorap2p(str_to_send)
    lora.send_lorap2p(tx_bytes)
                    
    row = [timestamp_send, dev_addr, dest_addr, message.frame_count, temperature, humidity, message.payload_bytes]                
    with open('results_client.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(row)


    print('Sent')

    time.sleep(30)
    i+=1