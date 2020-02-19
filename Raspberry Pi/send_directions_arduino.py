import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.printDetails()

message = list("LEFT")
while len(message) < 32:
    message.append(0)

try:
    while True:
        start = time.time()
        radio.write(message)
        print("Sent the message: {}".format(message))
        time.sleep(1)

except KeyboardInterrupt:
    print("All done!")

except:
    print("Something bad happened...")

finally:
    GPIO.cleanup()
