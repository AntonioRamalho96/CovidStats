#SIR model:
#Susceptible
#Infected
#Recovered

import matplotlib.pyplot as plt #pylint: disable=import-error

#Class definition (don't need to look)
class History:
    def __init__(self):
        #100 days prior to the infection era
        self.newI=[0]*100 #newly infected for each day
        self.newR=[0]*100 #newly recovered for each day

        self.totI=[0]*100 #total infected for each day
        self.totR=[0]*100 # total recovered for each day

    def updateHistory(self, newlyInfected=0, newlyRecovered=0):
            #History of newly infected
            self.newI=self.newI+[newlyInfected] #I0 of newly infected
            self.newR=self.newR+[newlyRecovered]  #no news recovers

            #Update totals (for plotting only)
            lastTotI=self.totI[len(self.totI)-1] #last values
            lastTotR=self.totR[len(self.totR)-1]
            self.totI=self.totI+[lastTotI+newlyInfected-newlyRecovered] #update
            self.totR=self.totR+[lastTotR+newlyRecovered] 

class Population:
    def __init__(self):
        self.S=1.0  #Susceptible
        self.I=0.0  #Infected
        self.R=0.0  #Recovered

    def updatePopulation(self, newlyInfected=0, newlyRecovered=0):
        self.S=self.S-newlyInfected
        self.I=self.I+newlyInfected-newlyRecovered
        self.R=self.R+newlyRecovered


#PARAMETERS
contactRatePerDay=0.2   #Number of people that are contacted
                        # in an infectious way by the infected,
                        # for each day

daysUntilRecovered=int(14) #Days from being infected to being recovered


#Very importante, look carefully
def computeNewlyInfected(Pop, His):
    #Do stuff here
    infectable=Pop.S/float(Pop.S+Pop.I+Pop.R) #Portion of infectable population
    #Traditional way of computing newly infected
    newlyInfected=Pop.I*contactRatePerDay*infectable

    return newlyInfected

#Very important, look carefully
def computeNewlyRecovered(Pop, His):
    #compute who was infected x days ago
    today=len(His.newI)-1
    newlyRecovered=His.newI[today-daysUntilRecovered]

    return newlyRecovered

#Determine portion of infected people introduced in society
I0=0.0000001

#Create population and history classes
Pop=Population()
His=History()

#infect population
Pop.updatePopulation(newlyInfected=I0)
#update history
His.updateHistory(I0, 0)


#Now the simulation!
simulationDays=600
for i in range(simulationDays):
    #Compute updates
    newlyInfected=computeNewlyInfected(Pop, His)
    newlyRecovered=computeNewlyRecovered(Pop, His)
    #Update variables
    Pop.updatePopulation(newlyInfected=newlyInfected, newlyRecovered=newlyRecovered)
    His.updateHistory(newlyInfected=newlyInfected, newlyRecovered=newlyRecovered)



plt.plot([i for i in range(len(His.totI))], His.totI, "r--")
plt.ylabel("Infected")
plt.xlabel("Days")
plt.show()