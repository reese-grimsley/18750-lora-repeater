###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option

import sys, os, time
import rak811v2
import messages
import csv, itertools

Rak811v2 = rak811v2.Rak811v2

if not os.path.isfile('results_repeater.csv'):
    with open('results_repeater.csv', 'w') as f:
        headers = 'TIMESTAMP_SEND,TIMESTAMP_RECEIVE,RSSI,SNR,SENDER_ADDRESS,DESTINATION_ADDRESS,FRAME_COUNT,TEMPERATURE,HUMIDITY,RAW_MESSAGE\r\n'
        f.write(headers)

## Device address
dev_addr = 0x02 ## Repeater


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
lora.set_config('lorap2p:915000000:12:0:1:10:20')
resp = lora.get_info()
for x in resp:
    print('\t',x)

### Receiving
print('print recv events')
i=0
while True:
    print()
    print('loop iter %d' % i)
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

                # decoded_data = bytes.fromhex(data).decode('ASCII')
                # print('Received: %s' % decoded_data)


                message = messages.RXMessage(data)
                ##Log to CSV, with timestamp, frame_count, dest_addr, sender_address, RSSI, SNR, and the payload bytes

                payload_bytes = message.get_payload_bytes()
                if len(payload_bytes) >= 24:
                    temperature = messages.bytes_to_double(payload_bytes[0:8])
                    humidity = messages.bytes_to_double(payload_bytes[8:16])
                    timestamp = messages.bytes_to_double(payload_bytes[16:24])

                    now = time.time()
                    timediff = now - timestamp
                    row = [timestamp, now, rssi, snr, message.get_sender_addr(),message.get_dest_addr(), message.get_frame_counter(), temperature, humidity, payload_bytes]

                    with open('results_repeater.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)


                    print(f'Temperature: {temperature};\thumidity: {humidity};\ttimestamp: {timestamp}')

                # only if dev address and dest address in packet matches, else retransmit
                if message.get_dest_addr() == dev_addr:
                    decoded_data = message.get_payload()
                    print('Received: %s' % decoded_data)

                else:

                    # Set in Tx mode
                    ##What if we received 2 messages in this timeframe? Perhaps we should keep a list of the messages we received, and then send them all after we're doing processing received events
                    print(f'Repeating message from sender {message.get_sender_addr()} to {message.get_dest_addr()}')

                    print('\nSet self as sender mode')
                    lora.set_config('lorap2p:transfer_mode:2')
                    resp = lora.get_info()
                    # print(resp)
                    for x in resp:
                        print('\t',x)

                    # Create message
                    received_bytes = message.get_payload_bytes()
                    message_re = messages.TXMessage(message.get_frame_counter(), message.get_dest_addr(), dev_addr, received_bytes)
                    tx_bytes = message_re.get_bytes()   
                    lora.send_lorap2p(tx_bytes)
                    if message.get_payload() == "INVALID ASCII; USE payload_bytes INSTEAD":
                        print('Repeated (bytes): %s' % str(message.get_payload_bytes()))
                    else:
                        print('Repeated %s' % message.get_payload())  
                    

                    # Set in Rx mode

                    print('\nSet self as receiver mode')
                    lora.set_config('lorap2p:transfer_mode:1')
                    resp = lora.get_info()
                    # print(resp)
                    for x in resp:
                        print('\t',x) 

                    time.sleep(2)          


    except rak811v2.serial.Rak811v2TimeoutError as e:
        print('timeout on RX')
        # print(e)

    i+=1