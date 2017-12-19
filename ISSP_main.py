#ISSP main script of the simulation

#### import libraries

import numpy as np
import matplotlib.pyplot as plt
import ISSP_functions as ISSP
import ISSP_classes as ISSPclasses

#### create time vector ####

# the time vector contains times (seconds) which are used tp generate a time step
# over which to simulate the model. The vector does not need to have even spacing
# of numbers, and numbers can be floating point. However, for the sake of realism,
# numbers should be in ascending order.

time = np.arange(0, 600, 1)  # create time vector starting at t=0, ending at t=599, incrementing by 1 second

#### create instance of body() class with intial conditions ####

# earth parameters
static = True
name = 'Earth'
pos = np.array([0, 0, 0])
v = np.array([0, 0, 0])
dvdt = np.array([0, 0, 0])
dryMass = 5.972e24
fuelMass = 0
engineOutput = 0
engineBurnRate = 0
engineThrottle = 0
thrustVector = np.array([0, 0, 0])
dragCoef = 0
A = 0
r = 6.371e6
gravity = np.array([0, 0, 0])

earth = ISSPclasses.body(static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate, engineThrottle, thrustVector, dragCoef, A, r, gravity)

# earth parameters
static = False
name = 'SaturnV'
pos = np.array([0, 0, 0])
v = np.array([0, 0, 0])
dvdt = np.array([0, 0, 0])
dryMass = 5.972e24
fuelMass = 0
engineOutput = 0
engineBurnRate = 0
engineThrottle = 0
thrustVector = np.array([0, 0, 0])
dragCoef = 0
A = 0
r = 6.371e6
gravity = np.array([0, 0, 0])

spacecraft = ISSPclasses.body(static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate, engineThrottle, thrustVector, dragCoef, A, r, gravity)

#### put bodies in objectList ####

objectList = [earth, spacecraft]

#### iterate through time vector, generating time interval ####

for i in range(1,len(time)):
    dt = time[i] - time[i-1]  # calculate timestep
    objectList = ISSP.netGravity(objectList)  # calculate net gravity on each body at current positions

	


