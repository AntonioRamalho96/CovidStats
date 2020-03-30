
from Fetch import Fetch
import numpy as np
import matplotlib.pyplot as plt #pylint: disable=import-error



#Country in early stages of epidemic
pt=Fetch.confirmed("Portugal")

#List of countries in further stages of epidemic, to compare
nameList=["Germany", "Italy", "France", "Spain", "South_Korea"] #list of names
colorsInGraphic=["y--", "g--", "b--", "r--", "bs"]
countryList=[Fetch.confirmed(countryName) for countryName in nameList]


#defining useful methods
def compareError(list1, list2):
    #average of (log(list1[i]+1)-log(list2[i]+1))^2
    # can be seen as average quadratic error of logariths
    return sum([np.square(np.log(list1[i]+100)-np.log(list2[i]+100)) for i in range(len(list1))])/float(len(list1))

def dayForBestFit(list1, list2):
    #Finds a positive i such that
    #list1[i:] and list2[:len(list1)-i] are the best match possible
    iMax=30
    listCompareErrors=[compareError(list1[i:], list2[:len(pt)-i]) for i in range(iMax)]
    return listCompareErrors.index(min(listCompareErrors))



#PLOT
case=[]
d0=[]
style=[]
name=[]

#Data for plotting country in early stage
case.append(pt)
d0.append(0)
style.append("gs")
name.append("Portugal")

#Data for plotting other countries
for i in range(len(countryList)):
    case.append(countryList[i])
    d0.append(dayForBestFit(pt, countryList[i]))
    style.append(colorsInGraphic[i])
    name.append(nameList[i])

#Plot everything
handles=[]
for i in range(len(case)):
    handle, = plt.plot([x+d0[i] for x in range(len(case[i]))], case[i], style[i], label=name[i]  )
    handles.append(handle)
plt.legend(handles=handles)
plt.ylabel("Number infected")
plt.xlabel("Days")
plt.show()

