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
dryMass = 5.972e24  # kg
fuelMass = 0
engineOutput = 0
engineBurnRate = 0
engineThrottle = 0
thrustVector = np.array([0, 0, 0])
dragCoef = 0
A = 0
r = 6.371e6  # m
gravity = np.array([0, 0, 0])

earth = ISSPclasses.body(static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate, engineThrottle,
                         thrustVector, dragCoef, A, r, gravity)

# spacecraft parameters
static = False
name = 'SaturnV complete stack'
pos = np.array([earth.r, 0, 0])
v = np.array([0, 0, 0])
dvdt = np.array([0, 0, 0])
dryMass = 2950e3  # kg
fuelMass = 2169e3  # kg
engineOutput = 33.4e6  # N
engineBurnRate = 12.58e3  #kg/s source: https://history.nasa.gov/SP-4029/Apollo_18-23b_Launch_Vehicle_Propellant_Use.htm
engineThrottle = 1
thrustVector = np.array([1, 0, 0])
dragCoef = 0.515  # guesstimate
A = 78.54  # m^2
r = 0
gravity = np.array([0, 0, 0])

spacecraft = ISSPclasses.body(static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate,
                              engineThrottle, thrustVector, dragCoef, A, r, gravity)

#### put bodies in objectList ####

objectList = [earth, spacecraft]

#### iterate through time vector, generating time interval ####

for i in range(1, len(time)):
    dt = time[i] - time[i-1]  # calculate time step, dt

    objectList = ISSP.netGravity(objectList)  # calculate net gravity on each body at current positions
    # objectList = ISSP.update(objectList)  # this will calculate the position of bodies at the end of the tstep
    objectList = ISSP.burnFuelList(dt, objectList)  # updates fuel masses for objects in objectList

    spacecraft.thrustVector = ISSP.thrustVector1(spacecraft.v, 'fwd')   # specify what the thrust vector should be for
                                                                        # spacecraft

	


