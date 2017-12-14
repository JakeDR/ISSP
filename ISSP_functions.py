#ISSP functions and class definitions

# returns distance of point at [x, y, z] from planet at [x, y, z] with radius r
def altitude(point, planet, r):
	distance = ((point[0] - planet[0])**2 + (point[1] - planet[1])**2 + (point[2] - planet[2])**2)**0.5
	altitude = distance - r
	return altitude

# returns density of air (kg/m^3) at given altitude above earth
def airDensity(alt):
	
	p0 = 101.325  # sea level standard atmospheric pressure, kPa
	T0 = 288.15  # sea level standard temperature, K
	g = 9.80665  # earth surface gravitation acceleration, m/s^2
	L = 0.0065  # temerature lapse rate, K/m
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

# use below if wanting to visulise relationship
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
