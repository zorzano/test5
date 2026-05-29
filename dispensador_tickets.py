from itertools import islice, count

class DispensadorTickets:
    """Clase para gestionar la entrega correlativa de tickets."""
    
    MIN_TICKETS = 1
    MAX_TICKETS = 100

    def __init__(self):
        """Inicializa el contador de tickets empezando desde 1 con incremento de 2."""
        self._contador = count(1, step=2)

    def dameTicket(self, n: int) -> list[int]:
        """
        Devuelve una lista de 'n' tickets correlativos.
        Si 'n' no está entre 1 y 100, devuelve una lista vacía.
        """
        variableFea="Hola"
        if not (self.MIN_TICKETS <= n <= self.MAX_TICKETS):
            return []
            
        return list(islice(self._contador, n))
