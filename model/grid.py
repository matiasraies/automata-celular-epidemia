from model.neighborhood import Neighborhood
from model.person import Person, State


class Grid:

    # Constructor
    def __init__(self):
        self.grid = []
        self.rows = 0
        self.columns = 0

    def getRows(self):
        return self.rows

    def getColumns(self):
        return self.columns

    def setRows(self, rows):
        self.rows = rows

    def setColumns(self, columns):
        self.columns = columns

    # Llenar la cuadricula con personas en un estado inicial
    def fillGridWithPerson(self, stateInit):
        for x in range(self.rows):
            self.grid.append([])
            for y in range(self.columns):
                self.grid[x].append(Person(stateInit))

    def getGridAsList(self):
        grid = []
        for x in range(self.rows):
            for y in range(self.columns):
                grid.append(self.grid[x][y])

        return grid

    # Obtener persona en una posicion por fila y columna
    def getPersonByRowColumn(self, row, column):
        try:
            return self.grid[row][column]
        except:
            return None

    # Obtengo el vecindario Von Neumann de la posición x y
    def getNeighborhoodVN(self, x, y):
        try:
            if x <= 0 or y <= 0:
                raise Exception()

            neighborhood = []
            neighborhood.append(self.grid[x][y - 1])
            neighborhood.append(self.grid[x][y + 1])
            neighborhood.append(self.grid[x - 1][y])
            neighborhood.append(self.grid[x + 1][y])

            return Neighborhood(neighborhood)

        except:
            raise Exception('Imposible obtener vecindario')

    # Obtengo el vecindario Moore de la posición x y
    def getNeighborhoodM(self, x, y):
        try:
            if x <= 0 or y <= 0:
                raise Exception()

            neighborhood = []
            neighborhood.append(self.grid[x - 1][y])
            neighborhood.append(self.grid[x + 1][y])
            neighborhood.append(self.grid[x - 1][y - 1])
            neighborhood.append(self.grid[x + 1][y - 1])
            neighborhood.append(self.grid[x - 1][y + 1])
            neighborhood.append(self.grid[x + 1][y + 1])
            neighborhood.append(self.grid[x][y - 1])
            neighborhood.append(self.grid[x][y + 1])

            return Neighborhood(neighborhood)

        except:
            raise Exception('Imposible obtener vecindario')

    # Obtengo el vecindario Moore Extendido de la posición x y
    def getNeighborhoodME(self, x, y):
        return

    def countForState(self, state):
        try:
            choices = {
                State.SUSCEPTIBLE: (list(filter(lambda p: p.getState() == State.SUSCEPTIBLE, self.getGridAsList()))).__len__(),
                State.EXPUESTO: (list(filter(lambda p: p.getState() == State.EXPUESTO, self.getGridAsList()))).__len__(),
                State.INFECTADO: (list(filter(lambda p: p.getState() == State.INFECTADO, self.getGridAsList()))).__len__(),
                State.RECUPERADO: (list(filter(lambda p: p.getState() == State.RECUPERADO, self.getGridAsList()))).__len__(),
            }
            return choices.get(state, 0)
        except:
            return 0

    # Representación del objeto
    def __str__(self):
        value = '';
        for x in range(self.rows):
            for y in range(self.columns):
                value += f'[{str(self.grid[x][y])}]'
            value += '\n'
        return value
