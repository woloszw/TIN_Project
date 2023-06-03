import serial
from time import sleep
import io

SERIAL_INIT_CONFIG = "C\rS8\rO\r"
SERIAL_PORT = "COM7"
SERIAL_BAUD_RATE = 1000000
NUMBER_OF_BYTES = 19


frame = "t7023010100\r"

my_serial = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_BAUD_RATE, bytesize=8, parity=serial.PARITY_NONE,
                          stopbits=1,
                          timeout=0.05, xonxoff=True)

my_serial.write(SERIAL_INIT_CONFIG.encode(encoding='UTF-8'))
sleep(1)

for i in range(5):
    frame = "t70230" + str(i) + "0100\r"
    my_serial.write(frame.encode(encoding='UTF-8'))
    sleep(0.1)

# for i in range(5):
#     frame = "t70230" + str(i) + "0000\r"
#     my_serial.write(frame.encode(encoding='UTF-8'))
#     sleep(1)


count = 0
while(1):
    s = my_serial.readline().decode(encoding='UTF-8').strip()
    s = s[0:19]
    sleep(0.1)
    print("count #" + str(count) + ": " + s)
    count = count+1
