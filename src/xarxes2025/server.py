import socket
import time

class RTSP_RTP_Server:
    def __init__(self, rtsp_host='127.0.0.1', rtsp_port=554, rtp_port=5004):
        self.rtsp_host = rtsp_host
        self.rtsp_port = rtsp_port
        self.rtp_port = rtp_port
        self.rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.state = 'INIT'

    def handle_rtsp(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"RTSP Request: {data}")
            if "SETUP" in data:
                self.state = 'READY'
                response = "RTSP/1.0 200 OK\nCSeq: 1\nSession: 12345\n"
                client_socket.send(response.encode())
            elif "PLAY" in data:
                self.state = 'PLAYING'
                response = "RTSP/1.0 200 OK\nCSeq: 2\nSession: 12345\n"
                client_socket.send(response.encode())
                self.send_rtp_packets(('127.0.0.1', self.rtp_port))  # RTP destí
            elif "PAUSE" in data:
                self.state = 'READY'
                response = "RTSP/1.0 200 OK\nCSeq: 3\nSession: 12345\n"
                client_socket.send(response.encode())
            elif "TEARDOWN" in data:
                self.state = 'INIT'
                response = "RTSP/1.0 200 OK\nCSeq: 4\nSession: 12345\n"
                client_socket.send(response.encode())
                break

    def send_rtp_packets(self, client_address):
        frame_number = 0
        while self.state == 'PLAYING':
            frame_data = f"Frame {frame_number}".encode()
            self.rtp_socket.sendto(frame_data, client_address)
            print(f"Sent RTP Packet: Frame {frame_number}")
            frame_number += 1
            time.sleep(0.04)  # 25 FPS

    def start(self):
        # Iniciar RTSP Server
        self.rtsp_socket.bind((self.rtsp_host, self.rtsp_port))
        self.rtsp_socket.listen(1)
        print(f"RTSP Server listening on {self.rtsp_host}:{self.rtsp_port}")
        client_socket, addr = self.rtsp_socket.accept()
        print(f"Client connected: {addr}")
        self.handle_rtsp(client_socket)
        client_socket.close()
