from copy import copy
import matplotlib.pyplot as plt #pylint: disable=import-error

#Static classes
class PopulationParameters:
    def __init__(self, total, contact):
        #Static parameters
        self.__totalPopulation=total    #total population
        self.__contact=contact          #number of people critically contacted by infected per day

    def getTotalPopulation(self):
        return self.__totalPopulation

    def getContact(self):
        return self.__contact

class Desease:
    def __init__(self, time, immuneRate, deathRate):
        #Static parameters
        self.__deseaseTime=time        #number of days a person caries the infection
        self.__immuneRate=immuneRate   #Probability of getting immune after getting the desease
        self.__deathRate=deathRate     #Probability of dying with the desease

    def getDeseaseTime(self):
        return self.__deseaseTime

    def getImmuneRate(self):
        return self.__immuneRate

    def getDeathRate(self):
        return self.__deathRate



#Structure 
class PopulationStatus:
    def __init__(self, totalCases, totalImmune, newlyInfected, totalDead):
        self.totalCases=totalCases
        self.totalImmune=totalImmune
        self.newlyInfected=newlyInfected
        self.totalDead=totalDead



class History:
    def __init__(self, beforeTime, simTime):
        self.__beforeTime=beforeTime  #first day
        self.__simTime=simTime        #simulation time after first day

        #Store over time
        self.__cases=[0]*(beforeTime+simTime)
        self.__immune=[0]*len(self.__cases)
        self.__newCases=[0]*len(self.__cases)
        self.__dead=[0]*len(self.__cases)

    def store(self, population, day):
        #update history
        self.__cases[day] = population.totalCases
        self.__immune[day] = population.totalImmune
        self.__newCases[day]= population.newlyInfected
        self.__dead[day]= population.totalDead

    def  getNewCases(self, day):
        return self.__newCases[day]

    def plot(self):
        plt.plot(list(range(-self.__beforeTime, self.__simTime)), self.__cases , 'r--')
        #plt.plot(list(range(-self.__beforeTime, self.__simTime)), self.__immune, 'g--')
        #plt.plot(list(range(-self.__beforeTime, self.__simTime)), self.__dead  , 'b--')



class Simulation:
    def __init__(self, population, desease):
        #take population parameters
        self.__totalPopulation=population.getTotalPopulation()
        self.__contact=population.getContact()
        #take desease parameters
        self.__infectionTime=desease.getDeseaseTime()
        self.__immuneRate=desease.getImmuneRate()
        self.__deathRate=desease.getDeathRate()

    def simulate(self, cases0, simTime):
        #Initialize history
        Day0=self.__infectionTime+3
        self.__history=History(Day0 , simTime)
        #first infected
        population0=PopulationStatus(cases0, 0, cases0, 0)
        self.__history.store(population0, Day0)

        currentPopulation=population0

        for day in range(Day0, Day0+simTime):
            #Compute new population
            newPopulation=self.__computeUpdate(currentPopulation, day)
            
            #Store new population
            self.__history.store(newPopulation, day)

            #update population
            currentPopulation=newPopulation

        self.__history.plot()
    

    def __computeUpdate(self, currentPopulation, day):
        totalPopulation = self.__totalPopulation           #number of total people (including dead)
        cases           = currentPopulation.totalCases     #current number of infected people
        immune          = currentPopulation.totalImmune    #current number of immune people
        dead            = currentPopulation.totalDead      #current number of dead people
        alive           = totalPopulation-dead             #current number of living people

        deathRate       = self.__deathRate                 #portion of people that die
        surviveRate     = 1 - deathRate                    #portion of people that survive


        #Portion of the living population that can be infected
        healthyVulnerablePortion=(alive-cases-immune)/alive 

        #Portion of the population that is infected
        newlyInfected= min(cases*self.__contact, totalPopulation)*healthyVulnerablePortion

        #number of people that recover from illness
        recovered=self.__history.getNewCases(day-self.__infectionTime)*surviveRate

        #number of people that die from illness
        newlyDead=self.__history.getNewCases(day-self.__infectionTime)*deathRate

        #Total people that are immune (some of the recovered get immune)
        totalImmune = immune + recovered*self.__immuneRate   

        #Total people that are dead
        totalDead = dead + newlyDead

        #Update of number of cases from day d-1 to day d
        totalCases = cases + newlyInfected-recovered-newlyDead

        #return updated population
        return PopulationStatus(totalCases, totalImmune, newlyInfected, totalDead)


def showPlot():
    plt.ylabel("Number infected")
    plt.xlabel("Days")
    plt.show()


Pt = [2, 4, 6, 9, 13, 21 , 30, 39, 41, 59, 78, 112, 169, 245, 331, 448, 641]
plt.plot(list(range(len(Pt))), Pt , 'gs')


s=Simulation(PopulationParameters(10000000, 0.4), Desease(17, 1, 0.03))
s.simulate(3, 200)

#s=Simulation(PopulationParameters(100000000, 0.13), Desease(17, 1, 0.03))
#s.simulate(3, 600)


showPlot()
