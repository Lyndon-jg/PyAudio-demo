
from socket import *
import threading
import pyaudio
import struct
import pickle
import sys
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.5


class AudioServer(threading.Thread):
    def __init__(self) :
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.ADDR = ('', 10087)
        self.my_udp_socket = socket(AF_INET ,SOCK_DGRAM)

        self.voice = pyaudio.PyAudio()
        self.stream = None

    def __del__(self):
        # self.my_tcp_socket.close()
        self.my_udp_socket.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.voice.terminate()

    def run(self):
        print("AUDIO server starts...")
        self.my_udp_socket.bind(self.ADDR)
        self.stream = self.voice.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer = CHUNK
                                  )

        while True:
            data, addr = self.my_udp_socket.recvfrom(4096)
            self.stream.write(data, CHUNK)
            '''
            while len(data) < payload_size:
                # data += connect_socket.recv(81920)
                d, addr = self.my_udp_socket.recvfrom(102400)
                print(len(d))
                data += d

            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]

            while len(data) < msg_size:
                d, addr= self.my_udp_socket.recvfrom(102400)
                data += d

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frames = pickle.loads(frame_data)
            for frame in frames:
                self.stream.write(frame, CHUNK)

        while True:
            data, addr = self.my_udp_socket.recvfrom(102400)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            frame_data = data[:msg_size]
            frames = pickle.loads(frame_data)
            print("frames type:",type(frames))
            for frame in frames:
                print("frame type:",type(frame))
                self.stream.write(frame, CHUNK)
        '''




if __name__ == '__main__':
    aserver = AudioServer()
    aserver.start()
    while True:
        time.sleep(1)
        if not aserver.isAlive():
            print("aserver game over...")
            sys.exit(0)