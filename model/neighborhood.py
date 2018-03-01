import random

from core.configuration import Configuration
from model.person import State


class Neighborhood:

    # Constructor
    def __init__(self, neighborhood):
        self.people = neighborhood

    # Chequea si todas las células de la vecindad son susceptibles
    def isSusceptible(self):
        if list(filter(lambda p: p.getState() == State.SUSCEPTIBLE, self.people)).__len__() == list(
                self.people).__len__():
            return True
        return False

    def getCountForState(self, state):
        choices = {
            State.SUSCEPTIBLE: (list(filter(lambda p: p.getState() == State.SUSCEPTIBLE, self.people))).__len__(),
            State.EXPUESTO: (list(filter(lambda p: p.getState() == State.EXPUESTO, self.people))).__len__(),
            State.INFECTADO: (list(filter(lambda p: p.getState() == State.INFECTADO, self.people))).__len__(),
            State.RECUPERADO: (list(filter(lambda p: p.getState() == State.RECUPERADO, self.people))).__len__(),
        }
        return choices.get(state, 0)

    def getBoolProbability(self, state):
        choices = {
            State.SUSCEPTIBLE: self.probability(1),
            # probabilidad de ser expuesto al virus
            State.EXPUESTO: self.probability(
                self.getCountForState(State.INFECTADO) * Configuration().getTransmissibilityDisease()),
            State.INFECTADO: self.probability(1),
            State.RECUPERADO: self.probability(1),
        }
        return choices.get(state, False)

    def probability(self, probability):
        return random.random() <= probability
