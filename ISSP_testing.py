##ISSP script f0r testing things

import numpy as np
import matplotlib.pyplot as plt
import ISSP_functions as ISSP


pos1 = np.array([0,0,0])
pos2 = np.array([100,0,0])
mass1 = 100
mass2 = 50972e25

F = ISSP.gravity(pos1, pos2, mass1, mass2)
print(F)
