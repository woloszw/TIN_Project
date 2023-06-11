import serial
from time import sleep
import io

SERIAL_INIT_CONFIG = "C\rS8\rO\r"
SERIAL_PORT = "COM7"
SERIAL_BAUD_RATE = 1000000
NUMBER_OF_BYTES = 19
DELAY = 0.5

frame = "t7023010100\r"

my_serial = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_BAUD_RATE, bytesize=8, parity=serial.PARITY_NONE,
                          stopbits=1,
                          timeout=0.05, xonxoff=True)
def init():
    my_serial.write(SERIAL_INIT_CONFIG.encode(encoding='UTF-8'))
    sleep(DELAY)

def test_on():
    print("Test #1 - turning on the relays")
    for i in range(0, 5):
        frame = "t70230" + str(i) + "0100\r"
        my_serial.write(frame.encode(encoding='UTF-8'))
        sleep(DELAY)
    my_serial.readline().decode(encoding='UTF-8').strip()
    sleep(DELAY)
    s = my_serial.readline().decode(encoding='UTF-8').strip()
    #print("Read status frame:" + s[0:19])
    if (s[5:7] == "1F"):
        return 1
    else:
        return 0

def test_off():
    print("Test #2 - turning off the relays")
    for i in range(0, 5):
        frame = "t70230" + str(i) + "0000\r"
        my_serial.write(frame.encode(encoding='UTF-8'))
        sleep(DELAY)
    my_serial.readline().decode(encoding='UTF-8').strip()
    sleep(DELAY)
    s = my_serial.readline().decode(encoding='UTF-8').strip()
    #print("Read status frame:" + s[0:19])
    if (s[5:7] == "00"):
        return 1
    else:
        return 0


def test_wrong_relay():
    print("Test #3 - Setting wrong relay")
    frame = "t70230" + str(9) + "0000\r"
    my_serial.write(frame.encode(encoding='UTF-8'))
    sleep(DELAY)
    my_serial.readline().decode(encoding='UTF-8').strip()
    sleep(DELAY)
    s = my_serial.readline().decode(encoding='UTF-8').strip()
    if(s[0:7] == "t301104"):
        return 1
    return 0

def test_wrong_state():
    print("Test #4 - Setting wrong relay state")
    frame = "t7023000" + "5" + "00\r"
    my_serial.write(frame.encode(encoding='UTF-8'))
    sleep(DELAY)
    my_serial.readline().decode(encoding='UTF-8').strip()
    sleep(DELAY)
    s = my_serial.readline().decode(encoding='UTF-8').strip()
    if(s[0:7] == "t301105"):
        return 1
    return 0


init()

while(1):
    input("Press any key to launch tests:")
    if (test_on() == 1):
        print("All good!")
    else:
        print("Shit's fucked!")

    if (test_off() == 1):
        print("All good!")
    else:
        print("Shit's fucked!")

    if(test_wrong_relay()):
        print("All good!")
    else:
        print("Shit's fucked!")

    if(test_wrong_state()):
        print("All good!")
    else:
        print("Shit's fucked!")

