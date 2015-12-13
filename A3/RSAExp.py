__author__ = 'Rakatak'
# given values

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

p = 41
q = 17
e = 39
m = 9

n = p * q
print("n = " + str(n))
phiN = (p - 1) * (q - 1)
print("phiN = " + str(phiN))
d = modinv(e, phiN)
print("Inverse to phiN and e is " + str(d))
print("d = " + str(d))
valueOne = (d*e) % phiN
print("valueOne = " + str(valueOne))
print("Public key is (e, n) => (3, " + str(n) + ")")
print("Private key is (d, n) => (27, " + str(n) + ")")
c = m**e % n
print("Encrypted Message of 9 is " + str(c))
dM = c**d % n
print("Decrypted Message of " + str(c) + " is " + str(dM))
