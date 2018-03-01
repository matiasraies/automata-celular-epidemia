import threading
import time
from enum import Enum

from core.configuration import Configuration
from model.grid import Grid
from model.person import State


# Estados permitidos para las personas
class Type(Enum):
    INTERFACE = 1
    CONSOLE = 2


# Class singleton
class Simulator(object):
    class __Simulator:
        def __init__(self):
            # Inicializo cuadrícula
            self.grid = Grid()

        def getGrid(self):
            return self.grid

        # Configurar el simulador
        def setUp(self, rows, columns):

            # Configuro cuadricula
            self.grid.setRows(rows)
            self.grid.setColumns(columns)
            self.grid.fillGridWithPerson(State.SUSCEPTIBLE)

        def generateInfection(self, x, y):
            try:
                self.grid.getPersonByRowColumn(x, y).setState(State.INFECTADO)
            except:
                print('Coordenadas incorrectas')

        # Comienzo de simulación
        def start(self):

            # Hilo 1 de procesamiento y simulación
            thread_core_one = threading.Thread(target=self.core, args=(0, self.grid.getRows(), 0, self.grid.getColumns()))
            thread_core_one.start()

            # Hilo 2 de procesamiento y simulación
            # thread_core_two = threading.Thread(target=self.core, args=(0, self.grid.getRows(), 0, self.grid.getColumns()))
            # thread_core_two.start()

            # Hilo de estadisticas
            thread_stats = threading.Thread(target=self.stats)
            thread_stats.start()

        # Procesamiento y simulador
        def core(self, x_min_range, x_max_range, y_min_range, y_max_range):
            while True:
                # Por cada elemento de la cuadrícula obtengo su vecindad y calculo el estado de la célula
                # si no es posible calcular la vecindad, se sigue con la próxima celula
                for x in range(x_min_range, x_max_range):
                    for y in range(y_min_range, y_max_range):
                        try:
                            neighborhood = self.grid.getNeighborhoodM(x, y)
                            self.grid.getPersonByRowColumn(x, y).verifyState(neighborhood)
                        except:
                            pass
                time.sleep(Configuration().getTimeDaySeg())

        # Estadisticas
        def stats(self):
            nDay = 0
            print(f'################# Estadisticas por dia #################')
            while True:
                print(f'\n[INFO] ###################### Dia {nDay} ######################\n'
                      f'[INFO] Cantidad de gente Susceptible: {self.grid.countForState(State.SUSCEPTIBLE)}\n'
                      f'[INFO] Cantidad de gente Expuesta: {self.grid.countForState(State.EXPUESTO)}\n'
                      f'[INFO] Cantidad de gente Infectada: {self.grid.countForState(State.INFECTADO)}\n'
                      f'[INFO] Cantidad de gente Inmune: {self.grid.countForState(State.RECUPERADO)}')
                nDay += 1
                time.sleep(Configuration().getTimeDaySeg())

        def show(self, type):
            if type == Type.CONSOLE:
                self.showConsole()

        def showConsole(self):
            while True:
                print(self.grid)
                # tiempo pactado de la duración del dia
                time.sleep(Configuration().getTimeDaySeg())

    instance = None

    def __new__(cls):
        if not Simulator.instance:
            Simulator.instance = Simulator.__Simulator()
        return Simulator.instance

    def __getattr__(self, grid):
        return getattr(self.instance, grid)

    def __setattr__(self, grid):
        return setattr(self.instance, grid)
