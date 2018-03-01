from enum import Enum

from core.configuration import Configuration


# Estados permitidos para las personas
class State(Enum):
    SUSCEPTIBLE = 1
    INFECTADO = 2
    EXPUESTO = 3
    RECUPERADO = 4


class Person:

    # Constructor
    def __init__(self, State):
        self.state = State
        self.incubation_period = 0
        self.infection_period = 0
        self.immunity_period = 0

    # Obtiene el estado de la persona
    def getState(self):
        return self.state

    # Setea el estado de la persona
    def setState(self, state):
        self.state = state

    # Verifica el estado de la persona en base a las condiciones de su vecindario
    # actualiza el estado de la persona en caso de ser necesario, en base a las condiciones del AC
    def verifyState(self, neighborhood):
        if self.isStateSusceptible(neighborhood):
            self.setStateSusceptible()
        elif self.isStateExposure(neighborhood):
            self.setStateExposure()
        elif self.isStateInfection(neighborhood):
            self.setStateInfection()
        elif self.isStateResistance(neighborhood):
            self.setStateResistance()

    def isStateSusceptible(self, neighborhood):
        condition_one = self.state == State.SUSCEPTIBLE and neighborhood.isSusceptible()
        condition_two = self.state == State.RECUPERADO and self.immunity_period >= Configuration().getImmunityPerdiod()

        if condition_one or condition_two:
            return neighborhood.getBoolProbability(State.SUSCEPTIBLE)
        else:
            return condition_one or condition_two

    def isStateExposure(self, neighborhood):
        probExposure = neighborhood.getBoolProbability(State.EXPUESTO)
        condition_one = self.state == State.SUSCEPTIBLE and probExposure
        condition_two = self.state == State.EXPUESTO and self.incubation_period < Configuration().getIncubationPerdiod()

        if condition_one or condition_two:
            return probExposure
        else:
            return condition_one or condition_two

    def isStateInfection(self, neighborhood):
        condition_one = self.state == State.EXPUESTO and self.incubation_period >= Configuration().getIncubationPerdiod()
        condition_two = self.state == State.INFECTADO and self.infection_period < Configuration().getInfectionPerdiod()

        if condition_one or condition_two:
            return neighborhood.getBoolProbability(State.INFECTADO)
        else:
            return condition_one or condition_two

    def isStateResistance(self, neighborhood):
        condition_one = self.state == State.INFECTADO and self.infection_period >= Configuration().getInfectionPerdiod()
        condition_two = self.state == State.RECUPERADO and self.immunity_period < Configuration().getImmunityPerdiod()

        if condition_one or condition_two:
            return neighborhood.getBoolProbability(State.RECUPERADO)
        else:
            return condition_one or condition_two

    # Actualiza el estado completo de la persona a SUSCEPTIBLE
    def setStateSusceptible(self):
        self.state = State.SUSCEPTIBLE
        self.setPeriods(0, 0, 0)

    # Actualiza el estado completo de la persona a EXPUESTO
    def setStateExposure(self):
        self.state = State.EXPUESTO
        self.setPeriods(self.incubation_period + 1, 0, 0)

    # Actualiza el estado completo de la persona a INFECTADO
    def setStateInfection(self):
        self.state = State.INFECTADO
        self.setPeriods(0, self.infection_period + 1, 0)

    # Actualiza el estado completo de la persona a RECUPERADO
    def setStateResistance(self):
        self.state = State.RECUPERADO
        self.setPeriods(0, 0, self.immunity_period + 1)

    def setPeriods(self, incubation_period, infection_period, immunity_period):
        self.incubation_period = incubation_period
        self.infection_period = infection_period
        self.immunity_period = immunity_period

    # Determina los colores de los estados
    def determineStateColor(self):
        choices = {
            State.SUSCEPTIBLE: (255, 255, 255),
            State.EXPUESTO: (255, 150, 0),
            State.INFECTADO: (255, 0, 0),
            State.RECUPERADO: (0, 255, 0),
        }
        return choices.get(self.state, (255, 255, 255))

    # Representación del objeto
    def __str__(self):
        return f'{str(self.state.name)}'
