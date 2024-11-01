import sys
from src.vista.InterfazCajaSeguridad import App_CajaDeSeguridad
from src.logica.LogicaCaja import LogicaCaja

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = LogicaCaja()

    app = AppCajaDeSeguridad(sys.argv, logica)
    sys.exit(app.exec_())