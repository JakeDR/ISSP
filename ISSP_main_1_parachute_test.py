#ISSP main script of the simulation

#### import libraries

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('dark_background')
import ISSP_functions as ISSP
import ISSP_classes as ISSPclasses

#### create time vector ####

# the time vector contains times (seconds) which are used tp generate a time step
# over which to simulate the model. The vector does not need to have even spacing
# of numbers, and numbers can be floating point. However, for the sake of realism,
# numbers should be in ascending order.

time = np.arange(0, 6000, 0.2)  # create time vector starting at t=0, ending at t=599, incrementing by 1 second
n_plot = 5  # data every n_plot-th time step will be recorded for objects
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
name = 'Parachutist'
pos = np.array([earth.r+50000, 0.0, 0.0])
v = np.array([0.0, 0.0, 0.0])
dvdt = np.array([0.0, 0.0, 0.0])
dryMass = 10#2950.0e3  # kg
fuelMass = 0.0#2169.0e3  # kg
engineOutput = 50.27e6  # N (not realistic?)
engineBurnRate = 12.58e3  #kg/s source: https://history.nasa.gov/SP-4029/Apollo_18-23b_Launch_Vehicle_Propellant_Use.htm
engineThrottle = 0.0
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
									  [spacecraft.mod_dvdt],
									  [ISSP.altitude(spacecraft.pos, earth.pos, earth.r)],
									  [spacecraft.g_load],
									  spacecraft.drag,
									  spacecraft.force
									  )


#### put bodies in objectList ####

objectList = [earth, spacecraft]  # for some reason this seems to be converted to a numpy array later on...?

#### iterate through time vector, generating time interval ####

for i in range(1, len(time)):

	#### the below block will be common to all simulation setups
	curr_time = time[i]
	dt = time[i] - time[i-1]  # calculate time step, dt
	objectList = ISSP.netGravity(objectList)  # calculate net gravity on each body at current positions
	objectList = ISSP.updateBodyList(dt, objectList)  # this will calculate the position of bodies at the end of the tstep
	objectList = ISSP.burnFuelList(dt, objectList)  # updates fuel masses for objects in objectList
	objectList = ISSP.dragList(objectList, earth)   # calculated drag force on each body in body list, due to atmosphere of earth
	#####

	spacecraft.thrustVector = ISSP.thrustVector1(spacecraft.v, 'fwd')   # specify what the thrust vector should be for spacecraft
	#spacecraft.thrustVector = ISSP.thrustVector2(spacecraft.pos, earth.pos, 'awy')
	spacecraftData = ISSP.recordData(spacecraft, spacecraftData, earth, n_plot, i)


	if ISSP.altitude(spacecraft.pos, earth.pos, earth.r) < 0:  #end simulation if spacecraft crashes
		end_tpoint = i  # capture last simulate timestep number
		break
	end_tpoint = i




#### plot results ####

time_final = time[0:end_tpoint+1]  # crop down time vector to only include up to last simulated timestep
time_plot = np.transpose(time_final[0::n_plot])  # creates subsampled time vector to plot against


#### 3d plot of earth and spacecraft path ####

#fig = plt.figure(figsize=plt.figaspect(1)*1)
#ax = fig.add_subplot(111, projection='3d')

# plot earth
u = np.linspace(0, 2 * np.pi, 13)
v = np.linspace(0, np.pi, 13)
x = (earth.r * np.outer(np.cos(u), np.sin(v))) + earth.pos[0]
y = (earth.r * np.outer(np.sin(u), np.sin(v))) + earth.pos[1]
z = (earth.r * np.outer(np.ones(np.size(u)), np.cos(v))) + earth.pos[2]
#ax.plot_surface(x, y, z, rstride=1, cstride=1, color='g', shade=1, edgecolor='k')


#ax.scatter3D(spacecraftData.pos[:,0], spacecraftData.pos[:,1], spacecraftData.pos[:,2], s=50, color='r')

#ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
#ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
#ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

#ax.axis('scaled')
#plt.show()

#### 2D plots of spacecraft data ####

fig = plt.figure(2)
plt.subplot(3, 2, 1)
plt.plot(time_plot, spacecraftData.earthAlt)
plt.title('Earth altitude')
plt.ylabel('Altitude (m)')
plt.xlabel('Time (s)')

plt.subplot(3, 2, 2)
plt.plot(time_plot, spacecraftData.speed)
plt.title('Speed')
plt.ylabel('absolute speed (m/s)')
plt.xlabel('Time (s)')

plt.subplot(3, 2, 3)
plt.plot(time_plot, spacecraftData.fuelMass)
plt.title('Fuel')
plt.ylabel('Fuel mass (kg)')
plt.xlabel('Time (s)')

plt.subplot(3, 2, 4)
plt.plot(time_plot, spacecraftData.mod_dvdt)
plt.title('Acceleration')
plt.ylabel('Acceleration (m/s^2)')
plt.xlabel('Time (s)')

plt.subplot(3, 2, 6)
plt.plot(time_plot, (spacecraftData.g_load/9.81))
plt.title('g load')
plt.ylabel('Acceleration (xG)')
plt.xlabel('Time (s)')

plt.subplot(3, 2, 5)
plt.plot(time_plot, ((spacecraftData.force[:,0]**2 + spacecraftData.force[:,1]**2 + spacecraftData.force[:,2]**2)**0.5) )
plt.title('force')
plt.ylabel('N')
plt.xlabel('Time (s)')

plt.tight_layout()
plt.show()


