
from Fetch import Fetch
import numpy as np
import matplotlib.pyplot as plt #pylint: disable=import-error
from copy import copy

#Fetch.updateData()
D=39 #days for making model

#Country in early stages of epidemic
pt=Fetch.confirmed("Portugal")
weekDay=[i%7 for i in range(len(pt)+30)]

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
            if(studied[i-1]==studied[i-2]):
                increase[i-1]=increase[i-2]
    n=5
    if meanFilter:
        return np.convolve(increase, np.ones((n,))/n, mode='valid')
    return increase

#Study increase rates instead fo cases
ptCases=copy(pt)
ptFiltered=increaseRate(pt, meanFilter=True)
pt=increaseRate(pt, meanFilter=False)



#Predict growth
def predictGrowth(D, Dd, degree):
    #Poly fit for extrapolating the portuguese growth rate
    #using the past D days. Extrapolates for next D days
    if degree==2:
        a,b,c=np.polyfit(range(len(pt)-D, len(pt)), pt[len(pt)-D:], 2)
        return [a*day*day  + b*day + c for day in range(len(pt), len(pt)+Dd)]
    else:
        a,b=np.polyfit(range(len(pt)-D, len(pt)), pt[len(pt)-D:], 1)
        return [a*day +b for day in range(len(pt), len(pt)+D)]

#Match parabola
def regression(pt, D, Dd, degree=2):
    #Poly fit for accessing tendency
    if(degree==2):
        a,b,c=np.polyfit(range(len(pt)-D, len(pt)), pt[len(pt)-D:], 2)
        return [a*day*day  + b*day + c for day in range(len(pt)-D, len(pt)+Dd)]
    else:
        a,b=np.polyfit(range(len(pt)-D, len(pt)), pt[len(pt)-D:], 1)
        return [a*day +b for day in range(len(pt)-D, len(pt)+Dd)]

#Compute error for each day of the weak
def weeklyErrorVEctor(predict, vector, D):
    errorVector=[[] for i in range(7)]
    for day in range(len(vector)-D, len(vector)):
        err=(vector[day]-predict[day-len(vector)+D])/float(predict[day-len(vector)+D]+0.1)
        #print(err)
        errorVector[weekDay[day]].append(err)
    return [np.mean(weekDay) for weekDay in errorVector]

#Compute correcting indexes
growth=regression(pt, D, 10)
weekCorrection=weeklyErrorVEctor(growth, pt, D)

#print([pt[len(pt)-D+i]-growth[i] for i in range(D)])
D=10
growth=regression(pt, D, 10, degree=1)
growthCorr=[(growth[day+D-len(pt)]+0.1)*(weekCorrection[weekDay[day]])+growth[day+D-len(pt)] for day in range(len(pt)-D, len(pt)+10)]

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

#Plot everything
handles=[]
for i in range(len(case)):
    handle, = plt.plot([x+d0[i] for x in range(len(case[i]))], case[i], style[i], label=name[i]  )
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
for g in growthCorr[D:]:
    today=today*(1+g)
    i=i+1
    print("Today+"+repr(i)+ "=" + repr(today))

