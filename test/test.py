if __name__ == '__main__':
    # configuro el simulador
    from core.simulator import Simulator, Type

    simulator = Simulator()
    simulator.setUp(500, 500)
    simulator.start()
    simulator.show(Type.INTERFACE)
