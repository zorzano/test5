import socket
import sys

class ClienteTickets:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port

    def pedir_tickets(self, n):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(2.0)
        try:
            client_socket.sendto(str(n).encode('utf-8'), (self.host, self.port))
            data, _ = client_socket.recvfrom(1024)
            return data.decode('utf-8')
        except socket.timeout:
            return "Error: Tiempo de espera agotado"
        except Exception as e:
            return f"Error: {e}"
        finally:
            client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 cliente_tickets.py <numero_de_tickets>")
        sys.exit(1)
    
    try:
        n_tickets = int(sys.argv[1])
        cliente = ClienteTickets()
        resultado = cliente.pedir_tickets(n_tickets)
        if resultado == "":
            print("Error: El servidor devolvió una respuesta vacía (posible número fuera de rango)")
        else:
            print(resultado)
    except ValueError:
        print("Error: El parámetro debe ser un número entero")
