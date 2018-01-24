from socket import *
import threading
import pyaudio
import struct
import pickle
import time

CHUNK = 1024
# 取样值的量化格式
FORMAT = pyaudio.paInt16
# 声道数
CHANNELS = 2
# 取样频率
RATE = 44100

RECORD_SECONDS = 0.5

class AudioClient(threading.Thread):
    def __init__(self ,server_ip, server_port):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.SERVER_ADDR = (server_ip, server_port)
        self.my_tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.voice = pyaudio.PyAudio()

        self.stream = None

    def __del__(self) :
        self.my_tcp_socket.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        # pyaudio 资源
        self.voice.terminate()


    def run(self):
        print("AUDIO client starts...")
        while True:
            try:
                self.my_tcp_socket.connect(self.SERVER_ADDR)
                break
            except:
                time.sleep(2)
                continue
        print("AUDIO client connected...")

        self.stream = self.voice.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)

        while self.stream.is_active():
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                frames.append(data)
            senddata = pickle.dumps(frames)
            try:
                print(len(senddata))
                self.my_tcp_socket.sendall(struct.pack("L", len(senddata)) + senddata)
            except:
                break
