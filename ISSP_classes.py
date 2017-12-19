# contains class definitions for ISSP

class body(object):
	
    def __init__(self, static, name, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate, engineThrottle,
                 thrustVector, dragCoef, A, r, gravity):

        self.thrustVector = thrustVector

        self.static = static  # True or False. True for bodies allowed to move, e.g. spacecraft. False for
                              # bodies that will not move (e.g. Earth)
                              
        self.name = name  # a string to identify the body. Can be used as labels on graphs etc
		
        self.pos = pos  # np vector containing current postion [x, y, z], in meters
		
        self.v = v  # np vector containing current component velocity [Vx, Vy, Vz] in  (m/s)
		
        self.dvdt = dvdt  # np vector containing current component acceleration [dVdtX, dVdtY, dVdtZ] in m/s^2
		
        self.dryMass = dryMass  # mass of body minus fuel.
		
        self.fuelMass = fuelMass # mass of fuel. Initially set, but then updated based on timestep, throttle, and burnrate.
		
        self.engineOutput = engineOutput  # max output of engine (N)
		
        self.engineBurnRate = engineBurnRate  # burn rate of fuel at 100% throttle (kg/s)
		
        self.engineThrottle = engineThrottle  # current throttle of engine. Between 0 and 1.
		
        self.thrustVector = thrustVector    # direction of engine thrust, specified by np.array([x,y,z]),
                                            # where sqrt(x^2+y^2+z^2) = 1.
                                            # Used to calculate engineThrust.
		                                    
        self.dragCoef = dragCoef    # current drag coefficient or body. Can be zero for planets. Might change depending on V
                                    # but will be calculated elsewhere. For now use coeff for high reynolds number.
		
        self.A = A  # cross-sectional area of body. Used to calculate drag, so can be 0 for planets.
		
        self.r = r  # Radius of body. 0 for spacecraft. For plotting and calculating altitude of spacecraft from planet
		
        self.gravity = gravity  # component force on body due to net gravitational attraction to other bodies in simulation
		
    @property
    def speed(self):  # speed in (m/s^2)
        return (self.v[0]**2 * self.v[1]**2 * self.v[2]**2)**0.5

    @property
    def g(self):  # combined accelation.
        return (self.dvdt[0]**2 * self.dvdt[1]**2 * self.dvdt[2]**2)**0.5

	@property
    def totalMass(self):  # total mass of body
        return self.dryMass + self.fuelMass

    @property
    def thrust(self):  # component force due to engine thrust
        if self.fuelMass > 0:  # if fuel still left in the tank
            return self.thrustVector * self.engineOutput * self.engineThrottle
        else:  # if no fuel left
            return np.array([0, 0, 0])  # thrust = 0

	@property
    def force(self):  # total net force acting on body
        return (self.thrust + self.gravity)
