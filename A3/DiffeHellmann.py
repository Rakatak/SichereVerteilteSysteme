__author__ = 'Rakatak'

p = 467
g = 2
a = 228
b = 57

A = ((g**a) % p)
print("A = " + str(A))
B = ((g**b) % p)
print("B = " + str(B))
sA = ((A**b) % p)
print("sA = " + str(sA))
sB = ((B**a) % p)
print("sB = " + str(sB))

if sA == sB:
    print("Lol, alright")