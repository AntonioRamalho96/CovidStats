
from Fetch import Fetch
import numpy as np
import matplotlib.pyplot as plt #pylint: disable=import-error
from copy import copy

#Fetch.updateData()


#Country in early stages of epidemic
pt=Fetch.confirmed("Portugal")

#List of countries in further stages of epidemic, to compare
nameList=["Germany", "Italy", "Spain", "France"]#, "South_Korea"] #list of names
population=[83.0,60.0,47.0, 67.0]
colorsInGraphic=["y--", "g--", "r--", "b--"]#, "ys"] #List of styles in graphic
# ATENTION: len(nameList) should be equal to len(colorsInGraphic)
countryList=[Fetch.confirmed(countryName) for countryName in nameList]



#defining useful methods
def box_cox(value, lambda1=0.15, lambda2=50):
    if(lambda1==0):
        return np.log(value+lambda2)
    else:
        return ((value+lambda2)**lambda1-1)/lambda1
#error measure
def errorMetric(value1, value2):
    #return np.square(np.log(value1+100)-np.log(value2+100))
    #return np.square(box_cox(value1)-box_cox(value2))
    return np.square(value1-value2)

def compareError(list1, list2):
    #average of (log(list1[i]+1)-log(list2[i]+1))^2
    # can be seen as average quadratic error of logariths
    return sum([errorMetric(list1[i], list2[i]) for i in range(len(list1))])/float(len(list1))

def dayForBestFit(list1, list2):
    #Finds a positive i such that
    #list1[i:] and list2[:len(list1)-i] are the best match possible
    iMax=35
    listCompareErrors=[compareError(list1[i:], list2[:len(pt)-i]) for i in range(iMax)]
    return listCompareErrors.index(min(listCompareErrors))

def increaseRate(studied, meanFilter=True):
    #return the growth rate for every element in a list
    increase=[0]*(len(studied)-1)
    for i in range(1,len(studied)):
        if(studied[i-1]==0):
            increase[i-1]=0
        else:
            increase[i-1]=studied[i]/float(studied[i-1])-1.0
    n=5
    if meanFilter:
        return np.convolve(increase, np.ones((n,))/n, mode='valid')
    return increase

#Study increase rates instead fo cases
ptCases=copy(pt)
pt=increaseRate(pt)
countryListCases=copy(countryList)
countryList=[increaseRate(cases) for cases in countryList]


#PLOT
case=[]
d0=[]
style=[]
name=[]

#Data for plotting country in early stage
case.append([case/11.0 for case in ptCases])
d0.append(0)
style.append("gs")
name.append("Portugal")

#Data for plotting other countries
for i in range(len(countryList)):
    d=dayForBestFit(pt, countryList[i] )
    case.append([case/population[i] for case in countryListCases[i]])
    d0.append(d)
    style.append(colorsInGraphic[i])
    name.append(nameList[i])
    print("Country: "+ nameList[i] + ", averageError: " + repr(compareError(pt[d:], (countryList[i])[:len(pt)-d])))


#Plot everything
handles=[]
for i in range(len(case)):
    handle, = plt.plot([x+d0[i] for x in range(len(case[i]))], case[i], style[i], label=name[i]  )
    handles.append(handle)
plt.legend(handles=handles)
plt.ylabel("Cases per Million")
plt.xlabel("Days")
plt.show()

