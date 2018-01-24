
from socket import *
import threading
import pyaudio
import struct
import pickle

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.5


class AudioServer(threading.Thread):
    def __init__(self, port) :
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.ADDR = ('', port)
        self.my_tcp_socket = socket(AF_INET ,SOCK_STREAM)

        self.voice = pyaudio.PyAudio()
        self.stream = None

    def __del__(self):
        self.my_tcp_socket.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.voice.terminate()

    def run(self):
        print("AUDIO server starts...")
        self.my_tcp_socket.bind(self.ADDR)
        self.my_tcp_socket.listen(1)
        connect_socket, addr = self.my_tcp_socket.accept()
        print("remote AUDIO client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        self.stream = self.voice.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer = CHUNK
                                  )
        while True:
            while len(data) < payload_size:
                data += connect_socket.recv(81920)

            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]

            while len(data) < msg_size:
                data += connect_socket.recv(81920)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frames = pickle.loads(frame_data)
            for frame in frames:
                self.stream.write(frame, CHUNK)
