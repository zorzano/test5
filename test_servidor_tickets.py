import unittest
import socket
import threading
import time
from servidor_tickets import ServidorTickets

class TestServidorTickets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = '127.0.0.1'
        cls.port = 12346 # Puerto diferente para pruebas
        cls.server = ServidorTickets(host=cls.host, port=cls.port)
        # Iniciamos el servidor en un hilo separado
        cls.server_thread = threading.Thread(target=cls.server.start, daemon=True)
        cls.server_thread.start()
        # Damos un pequeño margen para que el socket se abra
        time.sleep(0.5)

    def test_servidor_entrega_tickets(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1.0)
        
        # Pedir 3 tickets y verificar que son correlativos
        client_socket.sendto(b"3", (self.host, self.port))
        data, _ = client_socket.recvfrom(1024)
        tickets = [int(x) for x in data.decode('utf-8').split(',')]
        self.assertEqual(len(tickets), 3)
        self.assertEqual(tickets[1], tickets[0] + 1)
        self.assertEqual(tickets[2], tickets[1] + 1)
        
        # Pedir 2 tickets más y verificar correlatividad con los anteriores
        ultimo_anterior = tickets[-1]
        client_socket.sendto(b"2", (self.host, self.port))
        data, _ = client_socket.recvfrom(1024)
        nuevos_tickets = [int(x) for x in data.decode('utf-8').split(',')]
        self.assertEqual(len(nuevos_tickets), 2)
        self.assertEqual(nuevos_tickets[0], ultimo_anterior + 1)
        self.assertEqual(nuevos_tickets[1], nuevos_tickets[0] + 1)
        
        client_socket.close()

    def test_servidor_entrada_invalida(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1.0)
        
        # Enviar algo que no es un número
        client_socket.sendto(b"hola", (self.host, self.port))
        data, _ = client_socket.recvfrom(1024)
        self.assertEqual(data, b"")
        
        # Enviar un número fuera de rango (101)
        client_socket.sendto(b"101", (self.host, self.port))
        data, _ = client_socket.recvfrom(1024)
        self.assertEqual(data, b"")
        
        client_socket.close()

    def test_cliente_tickets_class(self):
        from cliente_tickets import ClienteTickets
        cliente = ClienteTickets(host=self.host, port=self.port)
        
        # Pedir 5 tickets (deberían ser del 6 al 10 si los tests anteriores corrieron)
        # Nota: setUpClass solo corre una vez, por lo que el estado se mantiene entre métodos de test
        resultado = cliente.pedir_tickets(5)
        # Verificamos que al menos recibimos 5 números separados por comas
        self.assertEqual(len(resultado.split(',')), 5)

if __name__ == '__main__':
    unittest.main()
