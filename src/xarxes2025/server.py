import socket  
from loguru import logger                                       # Llibreria per gestionar registres de missatges (logging)
from xarxes2025.videoprocessor import VideoProcessor            # Processador de vídeo per gestionar fotogrames
from xarxes2025.udpdatagram import UDPDatagram                  # Classe per encapsular fotogrames en paquets UDP

class Server:
    def __init__(self, port):
        """
        Constructor de la classe Server.
        Configura els paràmetres inicials del servidor.

        :param port: El port en el qual el servidor escoltarà.
        """
        self.port = port                                                                        # Port on el servidor escoltarà
        self.video = VideoProcessor()                                                           # Instància del processador de vídeo
        self.frame_number = 0                                                                   # Comptador de fotogrames enviats
        self.socketudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                       # Crear un socket UDP
        self.address = "127.0.0.1"                                                              # Exemple: adreça IP del client destinatari (provisional)
        logger.debug(f"Server initialized on port {self.port}")                                 # Registre de depuració

    def get_frame_number(self):
        """
        Incrementa i retorna el número del següent fotograma.
        Aquesta funció assegura que cada fotograma té un identificador únic.

        :return: Número del fotograma actual.
        """
        self.frame_number += 1
        return self.frame_number

    def send_udp_frame(self):
        """
        Llegeix el següent fotograma del vídeo, l'encapsula en un paquet UDP i l'envia al client.
        """
        
        data = self.video.next_frame()                                                      # Obté el següent fotograma del vídeo
        if data and len(data) > 0:                                                          # Comprova si el fotograma no és buit
            frame_number = self.get_frame_number()                                          # Obté el número de fotograma
            udp_datagram = UDPDatagram(frame_number, data).get_datagram()                   # Prepara el paquet UDP
            self.socketudp.sendto(udp_datagram, (self.address, self.port))                  # Envia el paquet UDP al client especificat (adreça i port)
           
            logger.debug(f"Sent frame {frame_number} to {self.address}:{self.port}")        # Registre d'informació sobre el fotograma enviat

    def start(self):
        """
        Inicia el bucle principal del servidor.
        Envia contínuament fotogrames fins que es detingui manualment.
        """
        try:
            logger.info("Starting server...")                                           # Mostra un missatge indicant que el servidor comença
            while True:                                                                 # Bucle infinit per enviar fotogrames
                self.send_udp_frame()
        except KeyboardInterrupt:                                                       # Captura la interrupció manual (Ctrl+C) per detenir el servidor
            logger.info("Server shutting down...")
            self.close()

    def close(self):
        """
        Tanca el socket del servidor per alliberar recursos.
        """
        self.socketudp
