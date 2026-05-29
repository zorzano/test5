import unittest
from dispensador_tickets import DispensadorTickets

class TestDispensadorTickets(unittest.TestCase):
    def setUp(self):
        self.dispensador = DispensadorTickets()

    def tearDown(self):
        del self.dispensador

    def test_dame_ticket_returns_list(self):
        resultado = self.dispensador.dameTicket(1)
        self.assertIsInstance(resultado, list)

    def test_dame_ticket_returns_correct_sequence(self):
        resultado = self.dispensador.dameTicket(3)
        self.assertEqual(resultado, [1, 2, 3])

    def test_dame_ticket_consecutive_calls(self):
        self.dispensador.dameTicket(2)
        resultado = self.dispensador.dameTicket(1)
        self.assertEqual(resultado, [3])

    def test_dame_ticket_max_valid(self):
        resultado = self.dispensador.dameTicket(100)
        self.assertEqual(len(resultado), 100)
        self.assertEqual(resultado[0], 1)
        self.assertEqual(resultado[-1], 100)

    def test_dame_ticket_over_max(self):
        resultado = self.dispensador.dameTicket(101)
        self.assertEqual(resultado, [])

    def test_dame_ticket_zero(self):
        resultado = self.dispensador.dameTicket(0)
        self.assertEqual(resultado, [])

    def test_dame_ticket_negative(self):
        resultado = self.dispensador.dameTicket(-1)
        self.assertEqual(resultado, [])

    def test_dame_ticket_continuity(self):
        primera_llamada = self.dispensador.dameTicket(2)
        segunda_llamada = self.dispensador.dameTicket(4)
        total = primera_llamada + segunda_llamada
        self.assertEqual(total, [1, 2, 3, 4, 5, 6])

if __name__ == '__main__':
    unittest.main()
