##ISSP script fpr testing things

import numpy as np
import matplotlib.pyplot as plt
import ISSP_functions as ISSP


alt = np.arange(0,45000, 10)
density = np.zeros(len(alt))

for i in range(0,len(density)):
	density[i] = ISSP.airDensity(alt[i])
	#print("alt="+str(alt[i])+"  density="+str(density[i]))

plt.plot(alt, density)
plt.axis([0, 45000, 0, 0.0015])
plt.xlabel('Altitude (m)')
plt.ylabel('Air density (kg/m^3)')
plt.title('Relationship between air density and altitude')
plt.show()
