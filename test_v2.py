###There's something wrong with the normal rak811 library for the recently produced set of parts we purchased... supposedly this is an option


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
print(resp)
for x in resp:
    print('\t',x)