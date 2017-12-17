# contains class definitions for ISSP

class body(object):
	
	def __init__(self, static, pos, v, dvdt, dryMass, fuelMass, engineOutput, engineBurnRate, engineThrottle, thrustVector,
	             dragCoef, A)
		
		self.static = static  # True or False. True for bodies allowed to move, e.g. spacecraft. False for
                              # bodies that will not move (e.g. Earth)
		
		self.pos = pos  # np vector containing current postion [x, y, z], in meters
		
		self.v = v  # np vector containing current component velocity [Vx, Vy, Vz] in  (m/s)
		
		self.dvdt = dvdt  # np vector containing current component acceleration [dVdtX, dVdtY, dVdtZ] in m/s^2
		
		self.dryMass = dryMass  # mass of body minus fuel.
		
		self.fuelMass = fuelMass # mass of fuel. Initially set, but then updated based on timestep, throttle, and burnrate.
		
		self.engineOutput = engineOutput  # max output of engine (N)
		
		self.engineBurnRate = engineBurnRate  # burn rate of fuel at 100% throttle (kg/s)
		
		self.engineThrottle = engineThrottle  # current throttle of engine. Between 0 and 1.
		
		self.thrustVector = thrustVector  # direction of engine thrust, specified by np.array([x,y,z]), where components resolve to 1.
		                                  # Used to calculate engineThrust.
		                                    
		self.dragCoef = dragCoef  # current drag coefficient or body. Can be zero for planets. Might change depending on V
		                          # but will be calculated elsewhere. For now use coeff for high reynolds number.
		
		self.A = A  # cross-sectional area of body. Used to calculate drag, so can be 0 for planets.
		
	@property  # properties are read only attributes that are calculated from other attributes.
		        # i.e. things that never have to be set, but might be handy to be able to read
		
		def speed(self):  # speed in (m/s^2)
			return (v[0]**2 * v[1]**2 * v[2]**2)**0.5

		def g(self)  # combined accelation. 
			return (dvdt[0]**2 * dvdt[1]**2 * dvdt[2]**2)**0.5
			
		def totalMass(self)  # total mass of body
			return dryMass + fuelMass

		def thrust(self)  # component force due to engine thrust
			return thrustVector * engineOutput * engineThrottle
