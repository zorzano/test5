import socket
from dispensador_tickets import DispensadorTickets

class ServidorTickets:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.dispensador = DispensadorTickets()
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"Servidor de tickets escuchando en {self.host}:{self.port}")
        
        try:
            while True:
                data, addr = self.socket.recvfrom(1024)
                try:
                    n = int(data.decode('utf-8').strip())
                    tickets = self.dispensador.dameTicket(n)
                    respuesta = ",".join(map(str, tickets))
                    self.socket.sendto(respuesta.encode('utf-8'), addr)
                except ValueError:
                    self.socket.sendto(b"", addr)
        except KeyboardInterrupt:
            print("\nServidor detenido.")
        finally:
            self.socket.close()

if __name__ == "__main__":
    server = ServidorTickets()
    server.start()
