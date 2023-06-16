import socket
import pyautogui
import pyaudio

UDP_IP = '192.168.1.12'  # Use the IP address of the computer running the server
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

screen_width, screen_height = pyautogui.size()

CHUNK = 8192  # Adjust the chunk size as needed
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

while True:
    # Capture the screen frame
    screenshot = pyautogui.screenshot()
    screenshot.thumbnail((screen_width, screen_height))
    frame_bytes = screenshot.tobytes()

    # Split frame into smaller packets
    frame_packets = [frame_bytes[i:i+CHUNK] for i in range(0, len(frame_bytes), CHUNK)]

    # Read audio data from the stream
    audio_data = stream.read(CHUNK)

    # Split audio data into smaller packets
    audio_packets = [audio_data[i:i+CHUNK] for i in range(0, len(audio_data), CHUNK)]

    # Send each frame packet and audio packet over UDP
    for frame_packet, audio_packet in zip(frame_packets, audio_packets):
        sock.sendto(frame_packet + audio_packet, (UDP_IP, UDP_PORT))
