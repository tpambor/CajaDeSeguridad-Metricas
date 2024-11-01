#
# Pruebas unitarias para lógica mock
#

import unittest
from src.logica.LogicaMock import LogicaMock

class LogicaMockTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaMock()

    # Prueba para verificar que la lógica retorna la clave maestra
    def test_clave_maestra(self):
        self.assertEqual(self.logica.clave_maestra, self.logica.dar_clave_maestra())