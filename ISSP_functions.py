#ISSP functions

import numpy as np

# altitude()
# airDensity()
# drag()
# burnFuel()
# thrustVector1()
# thrustVector2()
# gravity()
# netGravity()

######################################

# rotates a list, l, by n elements.
# the np.roll() function has the undesirable side-effect of converting
# a list to an np.array.
# Use this if you want to preserve the list type


def rotateList(l, n):
    return l[n:] + l[:n]

######################################

# returns distance of point at [x, y, z] from planet at [x, y, z] with radius r


def altitude(point, planet, r):
	distance = ((point[0] - planet[0])**2 + (point[1] - planet[1])**2 + (point[2] - planet[2])**2)**0.5
	altitude = distance - r
	return altitude

######################################

# returns density of air (kg/m^3) at given altitude above earth
def airDensity(alt):

	p0 = 101.325  # sea level standard atmospheric pressure, kPa
	T0 = 288.15  # sea level standard temperature, K
	g = 9.80665  # earth surface gravitation acceleration, m/s^2
	L = 0.0065  # temperature lapse rate, K/m
	R = 8.31447  # ideal gas constant, J/(mol*K)
	M = 0.0289644  # molar mass of dry air, kg/mol


	if alt >= 42000:  # if alt is greater than 42,000m, assume out of atmosphere
		density = 0
		return density
	else:
		T = T0 - (L*alt)  # temperature at altitude, alt
		p = p0*(1 - (L*alt)/T0) **((g*M)/(R*L))  # pressure at altitute, alt
		density = (p*M)/(R*T)
		return density

# use below if wanting to visualise relationship
#alt = np.arange(0,45000, 10)
#density = np.zeros(len(alt))

#for i in range(0,len(density)):
	#density[i] = ISSP.airDensity(alt[i])
	#print("alt="+str(alt[i])+"  density="+str(density[i]))

#plt.plot(alt, density)
#plt.axis([0, 45000, 0, 0.0015])
#plt.xlabel('Altitude (m)')
#plt.ylabel('Air density (kg/m^3)')
#plt.title('Relationship between air density and alitude')
#plt.show()

######################################

# returns component drag in [x, y, z].

# point = position of body experience drag
# planet = position of planet with atmosphere
# r = radius of planet with atmosphere

# A = cross-sectional area of body (m^2)
# v = component velocity in [x,y,x] (m/s)
# C = drag coefficient


def drag(point, planet, r, A, C, v):
	alt = altitude(point, planet, r)
	density = airDensity(alt)
	speed = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
	F = - 0.5*density*C*A*v*speed
	return F  # component drag in [x, y, z]

######################################

# returns component drag in [x, y, z] for each body in objectList,
# as long as not earth

# 'planet' is the planet whose atmosphere is causing drag

def dragList(objectList, planet):
	for body in objectList:
		if body != planet:
			body.drag = drag(body.pos, planet.pos, planet.r, body.A, body.dragCoef, body.v)
	return objectList

######################################

# return new fuel mass after engine burn over time step
# dt = time step (seconds)
# burnRate = engine's burn rate of fuel, kg/s
# throttle = throttle status (between 0 and 1)
# fuelMass = mass of fuel at at start of time step (kg)


def burnFuel(dt, burnRate, throttle, fuelMass):

	if fuelMass > 0:  # only burn fuel if there is some in the tank
		fuelMass = fuelMass - (dt*burnRate*throttle)
	else:
		fuelMass = 0  # compensates for when fuelMass goes below zero after a burn
	return fuelMass

######################################

# iterates over objectList containing bodies in simulation and
# computes updates the fuelMass using burnFuel()


def burnFuelList(dt, objectList):

	for body in objectList:
		body.fuelMass = burnFuel(dt, body.engineBurnRate, body.engineThrottle, body.fuelMass)
	return objectList

######################################

# function to generate a thrust vector to specifiy in which direction the engines will
# produce force. The thrust vector is 3-component vector, where sqrt(x^2 + y^2 + z^2) = 1.
# Therefore simply multiplying the engine's total force by this vector gives the force
# in [x, y, z].
# This simple version allows absolute thrust vector to be given as either in the spacecraft's
# direction of travel, or against it.


def thrustVector1(v, direction):

	if direction == 'fwd':  # thrust to be in spacecraft direction of travel
		thrustVector = v / ((v[0]**2 + v[1]**2 + v[2]**2)**0.5)
		return thrustVector

	if direction == 'rev':  # thrust to be against spacecraft direction of travel
		thrustVector = -v / ((v[0]**2 + v[1]**2 + v[2]**2)**0.5)
		return thrustVector

######################################

# generates thrust vector either towards or away from a reference position, e.g. a planet


def thrustVector2(spacecraft_pos, reference_pos, direction):

	diff = (spacecraft_pos - reference_pos)
	d = (diff[0]**2 + diff[1]**2 + diff[2]**2)**0.5

	if direction == 'awy':  # thrust to be towards reference
		thrustVector = (spacecraft_pos - reference_pos)/d

	if direction == 'twd':  # thrust to be away from reference
		thrustVector =(reference_pos - spacecraft_pos)/d
	return thrustVector

######################################

# function to generate a thrust vector to specify in which direction the engines will
# produce force. This more complex function uses the spacecrafts current velocity as one
# axis, and the line from the spacecraft to some other point as the other axis. The third
# axis is then orthogonal to these two axes.
# angle1 is the angle


def thrustVector3(v, pos, reference_pos, yaw, elevation):
	# okay, got a bit stuck on this one! JR
	return

######################################

# Calculate component force [Fx, Fy, Fz] felt by body at pos1, with mass1, due to
# gravitational attraction with body at pos2 with mass2
# pos1 = position of body1 [x, y, z] (m)
# pos2 = position of body2 [x, y, z] (m)
# mass1 = mass of body1 (kg)
# mass2 = mass of body2 (kg)


def gravity(pos1, pos2, mass1, mass2):
	G = 6.674e-11  # gravitational constant (m^3*kg^-1*s^-2)
	d = ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)**0.5
	F = ((G*mass1*mass2)/d**3)*(pos2 - pos1)
	return F  # component force felt by mass at pos1

######################################

# given a list containing all bodies in the simulation, calculate the net force due
# to gravity for each body, due to gravity between all other bodies.


def netGravity(bodyList):

	for i in range(0, len(bodyList)):  # for as many times as there are bodies

		bodyList[0].gravity = np.array([0, 0, 0])  # clear previous net gravity of the first body

		for k in range(1, len(bodyList)):  # for each body in list except the first one

			# calculate net gravity between first body in list, and all others
			bodyList[0].gravity = bodyList[0].gravity + gravity(bodyList[0].pos, bodyList[k].pos, bodyList[0].totalMass, bodyList[k].totalMass)

		bodyList = rotateList(bodyList, 1)  # rotate bodyList by 1 to present new body at bodyList[0]

	return bodyList

######################################

# updates the dvdt, v, and pos for each body (in a list) over a timestep,
# based on attributes at the start of the timestep


def updateBodyList(dt, objectList):

	for body in objectList:
		if body.static != True:  # if body is not set to be static
			body.dvdt = body.force / body.totalMass  #f rom F=ma
			body.v = body.v + (body.dvdt * dt)  # calculate new v using v = u + at
			body.pos = body.pos + (body.v * dt) # calculate new position
		else:
			body.pos = body.pos  # not really needed, but explicitly says that static bodies don;t change position
	return objectList

######################################

# generates arrays containing data for a given body, every n timepoints,
# where timepoint is the current timepoint

# body = body object, e.g. spacecraft
# bodyData = bodyData object, initialised with initial conditions for t=0
# n = int. Data will be recorded every first and nth timepoint
# timepoint = timepoint number.

# Because bodyData is created from body loaded with initial conditions (bodyData = body), t=0 data is already present
# in bodyData

# NOTE: scalar body attributes, e.g. body.g,  must first be converted to lists, e.g. [body.g], to for the np
# concatenation to work


def recordData(body, bodyData, earth, n, timepoint):

	if (timepoint/n).is_integer():  # if nth timepoint.

		bodyData.pos = np.row_stack((bodyData.pos, body.pos))
		bodyData.v = np.row_stack((bodyData.v, body.v))
		bodyData.dvdt = np.row_stack((bodyData.dvdt, body.dvdt))
		bodyData.dryMass = np.concatenate((bodyData.dryMass, [body.dryMass]), axis=0)
		bodyData.fuelMass = np.concatenate((bodyData.fuelMass, [body.fuelMass]), axis=0)
		bodyData.totalMass = np.concatenate((bodyData.totalMass, [body.totalMass]), axis=0)
		bodyData.engineThrottle = np.concatenate((bodyData.engineThrottle, [body.engineThrottle]), axis=0)
		bodyData.speed = np.concatenate((bodyData.speed, [body.speed]), axis=0)
		bodyData.mod_dvdt = np.concatenate((bodyData.mod_dvdt, [body.mod_dvdt]), axis=0)
		bodyData.earthAlt = np.concatenate((bodyData.earthAlt, [altitude(body.pos, earth.pos, earth.r)]), axis=0)
		bodyData.g_load = np.concatenate((bodyData.g_load, [body.g_load]), axis=0)
		bodyData.drag = np.row_stack((bodyData.drag, body.drag))
		bodyData.force = np.row_stack((bodyData.force, body.force))
		bodyData.thrust = np.row_stack((bodyData.thrust, body.thrust))

	return bodyData


######################################


# adds a new entry to the events log
# log = event log array to be appended
# t = time of event
# string = string to label event

def logEvent(log, string, t):
	new_entry = [t, string]
	log = np.row_stack((log, new_entry))
	return log
