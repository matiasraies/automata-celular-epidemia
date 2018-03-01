"""
    Automata celular para simular la distribucion de una epidemia
    Python/Pygame Programs

    Autor Matias Marcelo Raies
"""

import sys

# Importamos la biblioteca Pygame
import pygame

from core.configuration import Configuration
from core.simulator import Simulator
from model.person import State


class Application:
    def __init__(self):
        self.simulator = Simulator()
        self.configuration = Configuration()
        pass

    def stageOne(self):
        while True:
            try:
                incubation_perdiod = int(input("Cual es el periodo de incubacion? Dias... "))
                infection_perdiod = int(input("Cual es el periodo de infeccion? Dias... "))
                immunity_perdiod = int(input("Cual es el periodo de inmunidad? Dias... "))
                transmissibility_disease = float(input("Cual es la probabilidad de contagio? 0..1 (Ejemplo: 0.3) "))
                print(f'\n[IMPORTANTE] Has click sobre el mapa para generar infectados\n'
                      f'[IMPORTANTE] Debe hacer click y arrastrar el mouse para que tome el punto inicial exacto\n')

                self.quit = False
                self.kquit = ''
                while self.kquit != 's' and self.kquit != 'n':
                    self.kquit = input("Comenzar simulacion? s/n ")

                break
            except:
                pass

        # salgo si la eleccion es n
        if (self.kquit == 'n'):
            self.quit = True
            sys.exit()

        # Configuracion de la simulacion
        Configuration().setIncubationPerdiod(incubation_perdiod)
        Configuration().setInfectionPerdiod(infection_perdiod)
        Configuration().setImmunityPerdiod(immunity_perdiod)
        Configuration().setTransmissibilityDisease(transmissibility_disease)

        # Comienzo de hilo de simulacion
        simulator = Simulator()
        simulator.setUp(500, 285)
        simulator.start()

    def stageTwo(self):
        pygame.init()

        # Establecemos la altura y largo de la pantalla
        dimensions = [self.simulator.getGrid().getRows(), self.simulator.getGrid().getColumns()]
        self.screen = pygame.display.set_mode(dimensions, 0)

        # Titulo de la ventana
        pygame.display.set_caption("Simulacion Epidemia")

        self.imagen = pygame.image.load('images/fondo_chubut.png').convert()

        self.surface = pygame.Surface(dimensions)
        self.surface.set_alpha(75)

    def stageThree(self):

        # ----------------------- BUCLE PRINCIPAL-------------------------------------------------#

        while not self.quit:
            self.screen.blit(self.imagen, (0, 0))
            self.screen.blit(self.surface, (0, 0))
            self.surface.fill((0, 0, 0));

            # El usuario hizo algo
            for event in pygame.event.get():
                # Si el usuario hace click sobre cerrar
                # Marcar que quiero salir, forma que abandona el bucle
                # Iteramos hasta que el usuario haga click sobre el boton de cerrar
                if event.type == pygame.QUIT:
                    self.quit = True
                    pygame.quit()
                    sys.exit()

                # Si algun boton del mouse es presionado
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Genero infeccion
                    x, y = event.pos
                    self.simulator.generateInfection(x, y)
                    print(f'\n[INFO] Se genero infección en posicion ({x}, {y})')

            # --- Dibujamos
            for x in range(self.simulator.getGrid().getRows() - 1):
                for y in range(self.simulator.getGrid().getColumns() - 1):
                    person = self.simulator.getGrid().getPersonByRowColumn(x, y)
                    if person.getState() == State.SUSCEPTIBLE:
                        pass
                    elif person.getState() == State.EXPUESTO:
                        pygame.draw.circle(self.surface, person.determineStateColor(), (x, y), 1)
                    elif person.getState() == State.INFECTADO:
                        pygame.draw.circle(self.surface, person.determineStateColor(), (x, y), 1)
                    elif person.getState() == State.RECUPERADO:
                        pygame.draw.circle(self.surface, person.determineStateColor(), (x, y), 1)

            # Avancemos y actualicemos la pantalla con lo que hemos dibujado.
            pygame.display.flip()
            pygame.display.update()


if __name__ == '__main__':
    application = Application()
    # Etapa de configuracion
    application.stageOne()
    # Etapa de disenio de interfaz
    application.stageTwo()
    # Etapa bucle principal
    application.stageThree()
