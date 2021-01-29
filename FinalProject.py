# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:10:02 2020

@author: sauls
"""


import numpy as np
import matplotlib.pyplot as plt


###############################################################################
####################### FUNCTIONS #############################################

####################### 1 ####################################################

def create_lists(x):
    
    infile = open(x, 'r')
    
    driver1 = 'Helio Castroneves'
    driver2 = 'Juan Pablo Montoya'
    
    #list 1 header
    header = [infile.readline().split(',')]
    
    #rest of the data
    data = infile.readlines()
    dataList = []
    for i in range(len(data)):
        dataList += [data[i].split(',')]
        
            
    #list 2 time and distance for driver 1
    driver1_td = []
    for i in range(len(dataList)):
        if dataList[i][0] == driver1:
            driver1_td += [[float(dataList[i][2]),float(dataList[i][3])]]
    
    #list 3 time and distance for driver 2
    driver2_td = []
    for i in range(len(dataList)):
        if dataList[i][0] == driver2:
            driver2_td += [[float(dataList[i][2]),float(dataList[i][3])]]
    
    #list 4 race sectors
    r_sect = []
    for i in range(len(dataList)):
        r_sect.append(dataList[i][1])
        
    #list 5 x and y locations
    xy_loc = []
    for i in range(len(dataList)):
        xy_loc += [[float(dataList[i][4]), float(dataList[i][5])]]
    
        

    
    return header, driver1_td, driver2_td, r_sect, xy_loc, dataList

####################### 2 ####################################################

def vel(t,x):
  
    vI = []
    for i in range(len(x)):
        deltaX = x[i]-x[i-1]
        deltaT = t[i]-t[i-1]
        vI.append(deltaX/deltaT)
    return vI
        

def compute_speed(t, x):
    
    vI = vel(t,x)
  
    return vI

####################### 3 & 4 #################################################

def solve_mb(intervalV, intervalD, dist):
    #Getting m and v values using linalg
    m = []
    b = []
    for i in range(len(intervalD)):
        A = np.array([[intervalD[i][0], 1], [intervalD[i][1],1]])
        c = np.array([intervalV[i][0], intervalV[i][1]])
        
        z = np.linalg.solve(A,c)
        
        m.append(z[0])
        b.append(z[1])
    #Finally calculating the velocity 
    v = []
    for i in range(len(intervalV)):
        v.append((m[i] * float(dist[i])) + b[i])
    
    
    return v

def vel_in_dis(dist, driverDV):
    intervalD = [] #intervals for position
    for i in range(len(dist)):
        for j in range(len(driverDV)):
            if driverDV[j-1][0] < float(dist[i]) <= driverDV[j][0]:
                intervalD += [[driverDV[j-1][0], driverDV[j][0]]]
    intervalV = []
    for i in range(len(dist)):
        for j in range(len(driverDV)):
            if driverDV[j-1][0] < float(dist[i]) <= driverDV[j][0]:
                intervalV += [[driverDV[j-1][1], driverDV[j][1]]]   
    
    v = solve_mb(intervalV, intervalD, dist)
    return v

####################### 5 #################################################


def negative_local_min(y):
        
    negative_localminY = []
    negative_localminX = []
    
    global x
    
    for i in range(len(y)):
        if (y[i] < y[i-1]) and (y[i] < y[i+1]):
            if y[i] < 0:
                negative_localminY.append(y[i])
                negative_localminX.append(x[i])
    
    
    return negative_localminX, negative_localminY
                
def positive_local_max(y):
        
    positive_localmaxY = []
    positive_localmaxX = []
    
    global x
    
    
    for i in range(len(y)):
        if (y[i] < y[i-1] or y[i] == y[i-1]) and ((y[i-1] > y[i-2])):
            if y[i-1] > 0:
                positive_localmaxY.append(y[i-1])
                positive_localmaxX.append(x[i-1]) 
                
               
    return positive_localmaxX, positive_localmaxY

############################  6c ##############################################
def local_min(y):
        
    localminY = []
    localminX = []
    
    global xy_loc
    
    for i in range(len(y)):
        if (y[i] < y[i-1]) and (y[i] < y[i+1]):
            if y[i] < 0:
              localminY.append(xy_loc[i][1])
              localminX.append(xy_loc[i][0])
              
    
    
    return localminX, localminY

def local_max(y):
        
    localmaxY = []
    localmaxX = []
    
    global xy_loc
    
    for i in range(len(y)-1):
        if (y[i] < y[i-1] or y[i] == y[i-1]) and ((y[i-1] > y[i-2])):
            if y[i-1] > 0:
              localmaxY.append(xy_loc[i-1][1])
              localmaxX.append(xy_loc[i-1][0])
              
    
    
    return localmaxX, localmaxY


############################### 7 #############################################
    
def makeCSV(header, r_sect, driver_td1, driver_td2, velD1, local_minmum):
    outfile = open('SaulParra.csv','w')
    outfile.write('Race_Sector , Time [m:s] , Time_Split [s], Time Castroneves - Time Motoya , Velocity Cast. [mph] , Observations\n')
    
    #list for time coloum
    timeC = []
    timeformat = []
    
    for i in range(len(driver1_td)):
        timeC.append(driver1_td[i][0])
    
    for i in range(len(timeC)):
        timeformat += [('%2.f:%2.f' % (timeC[i]/60 , timeC[i]%60))]
        
    #list for timesplits   
    timeSplit = []
    for i in range(len(timeC)):
        timeSplit.append(timeC[i]-timeC[i-1])
    timeSplit[0] = timeSplit[-1]
    
    #list for  time cas - time mon
    timeM = []
    for i in range(len(driver2_td)):
        timeM.append(driver2_td[i][0])
        
    timeDiff = []
    for i in range(len(timeM)):
        timeDiff.append(timeC[i] - timeM[i])
        
    #velocity for Ca using velD1
    velocityC = []
    for i in range(len(velD1)):
        velocityC.append(velD1[i]*3600)
    
    #list for slower sector 
    slowerSect = []
    
    for i in range(68):
        sectionChosen =1
        for j in range(len(local_minimum)):
            if dataList[i][1] == local_minimum[j]:
                slowerSect += ['slower section']
                sectionChosen = 0
        if sectionChosen == 1:
            slowerSect+= [' ']
    
        
    for i in range(68):
        outfile.write('%s, %s, %.2f, %.3f, %d, %s\n' % (r_sect[i], timeformat[i], timeSplit[i], timeDiff[i], velocityC[i], slowerSect[i]))
        
    outfile.close()


###############################################################################
############################ MAIN #############################################
    
############################## 1 ##############################################
while True:
    try:
        #change to input statement after done
        file_name = input('Please enter the file name along with the file type (i.e. file_name.file_type): ')
        header, driver1_td, driver2_td, r_sect, xy_loc, dataList = create_lists(file_name)

        break
    except:
        print('\nSorry something is wrong with that file name, please try again',)

############################## 2 ##############################################

#Time and distance list for driver 1
timeD1 = [] 
distD1 = []

#Time and distance lists for driver 2
timeD2 = []
distD2 = []

for i in range(len(driver1_td)):
    timeD1.append(driver1_td[i][0])
    distD1.append(driver1_td[i][1])

for i in range(len(driver2_td)):
    timeD2.append(driver2_td[i][0])
    distD2.append(driver2_td[i][1])
    
velD1 = compute_speed(timeD1, distD1)
velD2 = compute_speed(timeD2, distD2)

############################## 3 & 4 ##########################################

#list of distance and velocity
dist_vel_D1 = []
for i in range(len((distD1))):
    dist_vel_D1 += [[distD1[i], velD1[i]]]
    
dist_vel_D2 = []
for i in range(len((distD2))):
    dist_vel_D2 += [[distD2[i], velD2[i]]]

#Makes sure the distace given is within the parameters 
while True:
    try:
        distances= input('Please enter a list of distances for which you want to know the velocity, seperate using commas:  ').split(',')
        u = 1
        for i in range(len(distances)):
            if float(distances[i]) > 2.229:
                u = 0
        U = 1/u
        v1 = vel_in_dis(distances, dist_vel_D1)
        v2 = vel_in_dis(distances, dist_vel_D2)
        break
    except ZeroDivisionError:
        print('\n Sorry one of the values was bigger than the max distance, try again: ')
    except:
        print('\n Sorry one of the values was bigger than the max distance, try again: ')

        

print('\n****************************************************************')
for i in range(len(v1)):
    print('\nThe velocity at distance %.2f mi. for Helio Castroneves is: %.2f mi./h ' % (float(distances[i]), v1[i]*3600) )

print('\n----------------------------------------------------------------')
for i in range(len(v2)):
    print('\nThe velocity at distance %.2f mi. for Juan Pablo Montoya is: %.2f mi./h' % (float(distances[i]), v2[i]*3600) )
    
############################## 6 ##############################################

# first graph #
d = []
for i in range(len(driver1_td)):
    d.append(driver1_td[i][1])
    
speed1 = []
for i in range(len(dist_vel_D1)):
    speed1.append(dist_vel_D1[i][1]*3600)
speed1[0] = speed1[-1]
d = []
for i in range(len(driver2_td)):
    d.append(driver2_td[i][1])
    
speed2 = []
for i in range(len(dist_vel_D2)):
    speed2.append(dist_vel_D2[i][1]*3600)   
speed2[0] = speed2[-1]

plt.plot(d,speed1, 'b')      
plt.plot(d,speed2, 'r')
plt.ylabel('Speed [miles/hour]')
plt.xlabel('Distance [miles]')
plt.legend(['Castroneves','Motoya'])

# second graph #

x = np.linspace(0,2.228,69)
yInd = []
for i in range(len(speed1)):
    yInd.append(speed1[i] - speed2[i])
    
nmx, nmy = negative_local_min(yInd)   
pmx, pmy = positive_local_max(yInd)

plt.figure(2)
plt.plot(x, yInd, 'b')
plt.plot(nmx, nmy, 'r*')
plt.plot(pmx, pmy, 'g*')
plt.legend(['Speed difference', 'local_min', 'local_max'])
plt.ylabel('speed [miles/h]')
plt.xlabel('Distance [miles]')
   
# thrid graph #

xPos = []
yPos = []

driverDiff = yInd    #speed1 - speed2  

xSlow, ySlow = local_min(driverDiff)

xFast, yFast = local_max(driverDiff)

for i in range(int(len(xy_loc))):
     xPos += [float(xy_loc[i-1][0])]
     yPos += [float(xy_loc[i-1][1])]

xPosI = xPos[0]
yPosI = yPos[0]

plt.figure(3)
plt.plot(xPos,yPos,'b')
plt.plot(xPosI,yPosI, 'k*', markersize = 15)
plt.plot(xFast, yFast, 'go') 
plt.plot(xSlow, ySlow, 'ro')
plt.xlabel('Distance east [feet]')
plt.ylabel('Distance north [feet]')
plt.legend(['Laguna seca', 'Start', 'Faster locations', 'Slower locations'])
plt.show()

#################################  7  #########################################



local_minimum = []
for i in range(len(xSlow)):
    section = 1
    for j in range(68):
        if xSlow[i] == (float(dataList[j][4])) and section != 0:
            local_minimum += [dataList[j][1]]
            section = 0


makeCSV(header, r_sect, driver1_td, driver2_td, velD1, local_minimum)

################################ 8 ############################################

print("\nFrom looking at the data I belive the driver is slower in: ")
print('Sect 7')
print('Sect 12')
print('Sect 20')
print('Sect 31')
print('Sect 42')
print('Sect 48')
print('Sect 53')
print('Sect 56')
print('Sect 62')

