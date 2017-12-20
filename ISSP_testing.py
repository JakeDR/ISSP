##ISSP script for testing things

import numpy as np
import matplotlib.pyplot as plt
import ISSP_functions as ISSP

list1 = np.array([1,2,3])
list2 = list1
list3 = np.row_stack((list1,list2))
list4 = np.row_stack((list3,list1))
print(list3)
print(list4)






