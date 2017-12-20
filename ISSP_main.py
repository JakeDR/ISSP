#ISSP main script of the simulation

#### import libraries

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import ISSP_functions as ISSP
import ISSP_classes as ISSPclasses

#### create time vector ####

# the time vector contains times (seconds) which are used tp generate a time step
# over which to simulate the model. The vector does not need to have even spacing
# of numbers, and numbers can be floating point. However, for the sake of realism,
# numbers should be in ascending order.

time = np.arange(0, 600, 1)  # create time vector starting at t=0, ending at t=599, incrementing by 1 second
n_plot = 1  # data every n_plot-th time step will be recorded for objects
time_plot = np.transpose(time[0::n_plot])  # creates subsampled time vector to plot against


#### create instance of body() class with intial conditions ####

# earth parameters
static = True
name = 'Earth'
pos = np.array([0.0, 0.0, 0.0])
v = np.array([0.0, 0.0, 0.0])
dvdt = np.array([0.0, 0.0, 0.0])
dryMass = 5.972e24  # kg
fuelMass = 0.0
engineOutput = 0.0
engineBurnRate = 0.0
engineThrottle = 0.0
thrustVector = np.array([0.0, 0.0, 0.0])
dragCoef = 0.0
A = 0.0
r = 6.371e6  # m
gravity = np.array([0.0, 0.0, 0.0])
drag = np.array([0.0, 0.0, 0.0])

earth = ISSPclasses.body(static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate, engineThrottle,
                         thrustVector, dragCoef, A, r, gravity, drag)

# spacecraft parameters
static = False
name = 'SaturnV'
pos = np.array([earth.r+10, 0.0, 0.0])
v = np.array([0.0, 0.0, 0.0])
dvdt = np.array([0.0, 0.0, 0.0])
dryMass = 2950.0e3  # kg
fuelMass = 2169.0e3  # kg
engineOutput = 50.8e6  # N (not realistic?)
engineBurnRate = 12.58e3  #kg/s source: https://history.nasa.gov/SP-4029/Apollo_18-23b_Launch_Vehicle_Propellant_Use.htm
engineThrottle = 1.0
thrustVector = np.array([1.0, 0.0, 0.0])
dragCoef = 0.515  # guesstimate
A = 78.54  # m^2
r = 0.0
gravity = np.array([0.0, 0.0, 0.0])
drag = np.array([0.0, 0.0, 0.0])

spacecraft = ISSPclasses.body(static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate,
                              engineThrottle, thrustVector, dragCoef, A, r, gravity, drag)

spacecraftData = ISSPclasses.bodyData(spacecraft.pos,
									  spacecraft.v,
									  spacecraft.dvdt,
									  [spacecraft.dryMass],
									  [spacecraft.fuelMass],
									  [spacecraft.totalMass],
									  [spacecraft.engineThrottle],
									  [spacecraft.speed],
									  [spacecraft.g],
									  [ISSP.altitude(spacecraft.pos, earth.pos, earth.r)]
									  )


#### put bodies in objectList ####

objectList = [earth, spacecraft]  # for some reason this seems to be converted to a numpy array later on...?

#### iterate through time vector, generating time interval ####

for i in range(1, len(time)):
	dt = time[i] - time[i-1]  # calculate time step, dt

	objectList = ISSP.netGravity(objectList)  # calculate net gravity on each body at current positions
	objectList = ISSP.updateBodyList(dt, objectList)  # this will calculate the position of bodies at the end of the tstep
	objectList = ISSP.burnFuelList(dt, objectList)  # updates fuel masses for objects in objectList
	objectList = ISSP.dragList(objectList, earth)   # calculated drag force on each body in body list, due to atmosphere of earth

	#spacecraft.thrustVector = ISSP.thrustVector1(spacecraft.v, 'fwd')   # specify what the thrust vector should be for spacecraft
	spacecraft.thrustVector = ISSP.thrustVector2(spacecraft.pos, earth.pos, 'awy')
	spacecraftData = ISSP.recordData(spacecraft, spacecraftData, earth, n_plot, i)

	if ISSP.altitude(spacecraft.pos, earth.pos, earth.r) < 0:
		end_tpoint = i
		break

#### plot some results ####

time_final = time[0:end_tpoint+1]  # crop down time vector to only include up to last simulated timestep
time_plot = np.transpose(time_final[0::n_plot])  # creates subsampled time vector to plot against

plt.plot(time_plot, spacecraftData.earthAlt)
plt.show()


