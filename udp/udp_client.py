from socket import *
import threading
import pyaudio
import time
import sys

CHUNK = 1024
# 取样值的量化格式
FORMAT = pyaudio.paInt16
# 声道数
CHANNELS = 2
# 取样频率
RATE = 44100

RECORD_SECONDS = 0.5

class AudioClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.SERVER_ADDR = ("127.0.0.1", 10087)
        self.my_udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.voice = pyaudio.PyAudio()

        self.stream = None

    def __del__(self) :
        self.my_udp_socket.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        # pyaudio 资源
        self.voice.terminate()


    def run(self):
        print("AUDIO client starts...")
        self.stream = self.voice.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        while self.stream.is_active():
            try:
                self.my_udp_socket.sendto(self.stream.read(CHUNK), self.SERVER_ADDR)
            except:
                print("find error fuck ")
                break
            '''
            print("is active ?")
            # frames = []
            # print(type(frames))
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                # data = self.stream.read(CHUNK)
                # print(type(data))  <class 'bytes'>
                # print(len(data))  4096
                try:
                    self.my_udp_socket.sendto(self.stream.read(CHUNK), self.SERVER_ADDR)
                except:
                    print("find error fuck ")
                    break

                frames.append(data)
            senddata = pickle.dumps(data)
            print("senddata type: ", type(senddata))
            try:
                self.my_udp_socket.sendto(struct.pack("L", len(senddata)) + senddata, self.SERVER_ADDR)
            except:
                print("find error fuck ")
                break
            '''

if __name__ == '__main__':
    aclient = AudioClient()
    aclient.start()
    while True:
        time.sleep(1)
        if not aclient.isAlive():
            print("aclient game over...")
            sys.exit(0)