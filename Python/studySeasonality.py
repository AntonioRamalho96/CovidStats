
from Fetch import Fetch
import numpy as np
import matplotlib.pyplot as plt #pylint: disable=import-error
from copy import copy

#Fetch.updateData()
D=35 #days for making model

#Country in early stages of epidemic
pt=Fetch.confirmed("Portugal")

#List of countries in further stages of epidemic, to compare
nameList=["Germany", "Italy", "Spain", "France"]#, "South_Korea"] #list of names
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
            if(studied[i]==studied[i-1]):
                increase[i-1]=increase[i-2]
    n=5
    if meanFilter:
        return np.convolve(increase, np.ones((n,))/n, mode='valid')
    return increase

#Study increase rates instead fo cases
ptCases=copy(pt)
ptFiltered=increaseRate(pt, meanFilter=True)
pt=increaseRate(pt, meanFilter=False)
countryListCases=copy(countryList)
countryList=[increaseRate(cases) for cases in countryList]

print(len(ptFiltered))
print(len(countryList[0]))


#Predict growth
def predictGrowth(n0, degree):
    #Poly fit for extrapolating the portuguese growth rate
    #using the past n0 days. Extrapolates for next D days
    D=15
    if degree==2:
        a,b,c=np.polyfit(range(len(pt)-n0, len(pt)), pt[len(pt)-n0:], 2)
        return [a*day*day  + b*day + c for day in range(len(pt), len(pt)+D)]
    else:
        a,b=np.polyfit(range(len(pt)-n0, len(pt)), pt[len(pt)-n0:], 1)
        return [a*day +b for day in range(len(pt), len(pt)+D)]

#Match parabola
def regression(pt, D, Dd):
    #Poly fit for accessing tendency
    a,b,c=np.polyfit(range(len(ptFiltered)-D, len(ptFiltered)), ptFiltered[len(ptFiltered)-D:], 2)
    return [a*day*day  + b*day + c for day in range(len(pt)-D, len(pt)+Dd)]

#Compute error for each day of the weak
def weeklyErrorVEctor(predict, vector, D):
    errorVector=[[] for i in range(7)]
    for i in range(D):
        err=(vector[len(vector)-D+i]-predict[i])/float(predict[i]+0.1)
        #print(err)
        errorVector[i%7].append(err)
    return [np.mean(weekDay) for weekDay in errorVector]

#Compute correcting indexes
growth=regression(pt, D, 10)
weekCorrection=weeklyErrorVEctor(growth, pt, D)

#print([pt[len(pt)-D+i]-growth[i] for i in range(D)])
growthCorr=[(growth[i]+0.1)*(weekCorrection[i%7])+growth[i] for i in range(len(growth))]

#PLOT-----------------------------------------------
case=[]
d0=[]
style=[]
name=[]

#Data for plotting country in early stage
case.append(pt)
d0.append(0)
style.append("g--")
name.append("Portugal")

#Data for plotting predicted growth
case.append(growth)
d0.append(len(pt)-D)
style.append('y--')
name.append("Predict (not seasonal)")

#Predicted growth corrected
case.append(growthCorr)
d0.append(len(pt)-D)
style.append('r--')
name.append("Predict (seasonal)")

#case.append([growth[i]-pt[i+len(pt)-D] for i in range(D)])
#d0.append(len(pt)-D)
#style.append('rs')
#name.append("Err")



#Plot everything
handles=[]
for i in range(len(case)):
    handle, = plt.plot([x+d0[i] for x in range(len(case[i]))], case[i], style[i], label=name[i]  )
    handles.append(handle)

#Plot mondays and fridays
monday=(D)%7
friday=(D-3)%7
#Plot mondays
x=[7*i+monday for i in range(D//7)]
y=[growthCorr[j] for j in x]
handle,=plt.plot([j+len(pt)-D for j in x], y, 'rs', label="monday"  )
handles.append(handle)
#fridays
x=[7*i+friday for i in range(D//7+1)]
y=[growthCorr[j] for j in x]
handle,=plt.plot([j+len(pt)-D for j in x], y, 'gs', label="friday"  )
handles.append(handle)

plt.legend()#handles=handles)
plt.ylabel("Growth rate")
plt.xlabel("Days")
plt.show()

#Estimate number of cases for future days
today=ptCases[len(ptCases)-1]
print()
print("Cases:")
print("Today="+repr(today))
i=0
for g in growthCorr:
    today=today*(1+g)
    i=i+1
    print("Today+"+repr(i)+ "=" + repr(today))

