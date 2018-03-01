from helpers.constants import Constants


class Configuration:
    class __Configuration:
        def __init__(self):
            self.incubation_perdiod = Constants.MAX_INCUBATION_PERIOD
            self.infection_perdiod = Constants.MAX_INFECTION_PERIOD
            self.immunity_perdiod = Constants.MAX_IMMUNITY_PERIOD
            self.transmissibility_disease = Constants.TRANSMISSIBILITY_DISEASE
            self.time_day_seg = Constants.TIME_DAY_SEG

        def getIncubationPerdiod(self):
            return self.incubation_perdiod

        def getInfectionPerdiod(self):
            return self.infection_perdiod

        def getImmunityPerdiod(self):
            return self.immunity_perdiod

        def getTransmissibilityDisease(self):
            return self.transmissibility_disease

        def getTimeDaySeg(self):
            return self.time_day_seg

        def setIncubationPerdiod(self, incubation_perdiod):
            self.incubation_perdiod = incubation_perdiod

        def setInfectionPerdiod(self, infection_perdiod):
            self.infection_perdiod = infection_perdiod

        def setImmunityPerdiod(self, immunity_perdiod):
            self.immunity_perdiod = immunity_perdiod

        def setTransmissibilityDisease(self, transmissibility_disease):
            self.transmissibility_disease = transmissibility_disease

        def setTimeDaySeg(self, time_day_seg):
            self.time_day_seg = time_day_seg

    instance = None

    def __new__(cls):
        if not Configuration.instance:
            Configuration.instance = Configuration.__Configuration()
        return Configuration.instance

    def __getattr__(self):
        return getattr(self.instance)

    def __setattr__(self):
        return setattr(self.instance)
