##ISSP script for testing things

import numpy as np
import matplotlib.pyplot as plt
import ISSP_functions as ISSP

class testClass:
	def __init__(self, at1, at2):
		self.at1 = at1
		self.at2 = at2

obj1 = testClass(1,2)
obj2 = testClass(4,5)

objList = [obj1, obj2]

for body in objList:
	print(body.at1)

testList = [1,2,3]
print(type(testList))
testList = [np.array([1]), 2, 3]
print(type(testList))
