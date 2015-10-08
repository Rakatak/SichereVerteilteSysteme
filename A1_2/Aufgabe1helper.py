import math
__author__ = 'Rakatak'

bits = 128
calcPerSec = 500000000
units = 10000000
two = 2
dayInSec = 86400
half = 2
budget= 1000000000


neededUnits = pow(two, bits)/(calcPerSec * dayInSec * two)
print("\nNeeded Units to tackle " + str(bits) + "-bits in 24 hours: " + str(neededUnits) + " units \n")


yearsForNeededUnits = math.log((neededUnits/units))
print("Years to get needed units with a " + str(budget) + " Euro budget: " + str(yearsForNeededUnits) + " years")


