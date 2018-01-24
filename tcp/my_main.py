import sys
import time
from my_achat_client import AudioClient
from my_achat_server import AudioServer

IP = "127.0.0.1"
PORT = 10087

if __name__ == '__main__':
    aclient = AudioClient(IP, PORT)
    aserver = AudioServer(PORT)

    aserver.start()
    time.sleep(1)
    aclient.start()
    while True:
        time.sleep(1)
        if not aserver.isAlive() or not aclient.isAlive():
            print(aserver.isAlive(), aclient.isAlive())
            print("Audio connection lost...")
            sys.exit(0)
