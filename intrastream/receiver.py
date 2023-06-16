import socket
import pyaudio
from PIL import Image
import io

UDP_IP = '192.168.1.12'  # Use the IP address of the computer running the server
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

while True:
    data, addr = sock.recvfrom(65507)
    frame_bytes = data[:len(data) - CHUNK]  # Extract frame bytes from received data
    audio_data = data[len(data) - CHUNK:]  # Extract audio data from received data

    image = Image.open(io.BytesIO(frame_bytes))
    image.show()

    stream.write(audio_data)
