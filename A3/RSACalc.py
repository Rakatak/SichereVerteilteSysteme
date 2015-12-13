__author__ = 'Rakatak'
# given values
p = 5
q = 11
e = 3
m = 9

n = p * q
print("n = " + str(n))
phiN = (p - 1) * (q - 1)
print("phiN = " + str(phiN))
d = 27
print("d = " + str(d))
valueOne = (d * e) % phiN
print("valueOne = " + str(valueOne))
print("Public key is (e, n) => (3, " + str(n) + ")")
print("Private key is (d, n) => (27, " + str(n) + ")")
c = m**e % n
print("Encrypted Message of 9 is " + str(c))
dM = c**d % n
print("Decrypted Message of " + str(c) + " is " + str(dM))
