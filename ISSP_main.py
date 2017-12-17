#ISSP main script of the simulation

#### import libraries

import numpy as np
import matplotlib.pyplot as plt
import ISSP_functions as ISSP

#### create time vector ####

# the time vector contains times (seconds) which are used tp generate a time step
# over which to simulate the model. The vector does not need to have even spacing
# of numbers, and numbers can be floating point. However, for the sake of realism,
# numbers should be ascending order.

time = np.arange(0, 10, 1)  # create time vector starting at t=0, ending at t=599, incrementing by 1 second


#### iterate through time vector, generating time interval ####

for i in range(1,len(time)):
	dt = time[i] - time[i-1]  # dt will then be fed to function that updates all objects over time step
	
	# e.g. simulate(dt, objectList)
	


