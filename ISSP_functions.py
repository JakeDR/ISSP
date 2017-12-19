#ISSP functions

# altitude()
# airDensity()
# drag()
# burnFuel()
# thrustVector1()
# thrustVector2()
# gravity()
# netGravity()

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
# density = density of medium (kg/m^3). See density()
# A = cross-sectional area of body (m^2)
# v = component velocity in [x,y,x] (m/s)
# C = drag coefficient
def drag(density, A, C, v):
	speed = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
	F = - 0.5*density*C*A*v*speed
	return F

######################################

# return new fuel mass after engine burn over time step
# dt = time step (seconds)
# burnRate = engine's burn rate of fuel, kg/s
# throttle = throttle status (between 0 and 1)
# fuelMass = mass of fuel at at start of time step (kg)
def burnFuel(dt, burnRate, throttle, fuelMass):
	fuelMass = fuelMass - (dt*burnRate*throttle)
	return fuelMass

######################################

# function to generate a thrust vector to specifiy in which direction the engines will
# produce force. The thrust vector is 3-component vector, where sqrt(x^2 + y^2 + z^2) = 1.
# Therefore simply multiplying the engine's total force by this vector gives the force
# in [x, y, z].
# This simple version allows absolute thrust vector to be given as either in the spacecraft's
# direction of travel, or against it.
def thrustVector1(v, direction):

	if direction == 'fwd':  # thrust to be in spacecraft direction of travel
		thrustVector = v / (v[0]**2 + v[1]**2 + v[2]**2)**0.5
		return thrustVector

	if direction == 'rev':  # thrust to be against spacecraft direction of travel
		thrustVector = -v / (v[0]**2 + v[1]**2 + v[2]**2)**0.5
		return thrustVector

######################################

# function to generate a thrust vector to specify in which direction the engines will
# produce force. This more complex function uses the spacecrafts current velocity as one
# axis, and the line from the spacecraft to some other point as the other axis. The third
# axis is then orthogonal to these two axes.
# angle1 is the angle
def thrustVector2(v, pos, reference_pos, yaw, elevation):
	# okay, got a bit stuck on this one! JR
	return

######################################

# Calculate component force [Fx, Fy, Fz] felt by body at pos1, with mass1, due to
# gravitional attraction with body at pos2 with mass2
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
			bodyList[0].gravity = bodyList[0].gravity + gravity(bodyList[0].pos, bodyList[i].pos, bodyList[0].totalMass, bodyList[i].totalMass)

		bodyList = np.roll(bodyList, 1)  # rotate bodyList by 1 to present new body at bodyList[0]

######################################
