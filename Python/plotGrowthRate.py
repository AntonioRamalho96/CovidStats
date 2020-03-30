#!/usr/bin/env python

# In this script it is ploted the growth rate of the number
#of confirmed cases over time. The time is shifted for each
# country in such a way that the growth rate curve is "at the same stage"


import numpy as np
import matplotlib.pyplot as plt #pylint: disable=import-error
from Fetch import Fetch

#update csv files
Fetch.updateData()

def increaseRate(studied, medianFilter=False):
    increase=[0]*(len(studied)-1)
    for i in range(1,len(studied)):
        if(studied[i-1]==0):
            increase[i-1]=0
        else:
            increase[i-1]=studied[i]/float(studied[i-1])-1.0

    n=5
    filtered=[0]*(len(increase)-n+1)
    if medianFilter:
        for i in range(len(filtered)):
            filtered[i]=sum(increase[i:i+n])/float(n)
    else:
        return increase

    return filtered


#PLOT
case=[]
d0=[]
style=[]
name=[]

case.append(increaseRate(Fetch.confirmed("Portugal")))
d0.append(31)
style.append("gs")
name.append("Portugal")

case.append(increaseRate(Fetch.confirmed("Italy")))
d0.append(11)
style.append("r--")
name.append("Italy")

#case.append(increaseRate(Fetch.confirmed("Germany")))
#d0.append(19)
#style.append("y--")
#name.append("Germany")

#case.append(increaseRate(Fetch.confirmed("Spain")))
#d0.append(20)
#style.append("b--")
#name.append("Spain")


case.append(increaseRate(Fetch.confirmed("France")))
d0.append(19)
style.append("b--")
name.append("France")

#case.append(increaseRate(Fetch.confirmed("China")))
#d0.append(-25)
#style.append("b--")
#name.append("China Hubei")

#case.append(increaseRate(Fetch.confirmed("South Korea")))
#d0.append(7)
#style.append("b--")
#name.append("South Korea")



handles=[]
for i in range(0,3):
    handle, = plt.plot([x-d0[i] for x in range(len(case[i]))], case[i], style[i], label=name[i]  )
    handles.append(handle)

plt.legend(handles=handles)

plt.ylabel("Number infected")
plt.xlabel("Days")
plt.show()
