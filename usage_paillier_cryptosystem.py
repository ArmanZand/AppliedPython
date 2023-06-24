from paillier_cryptosystem import *

#The Paillier Cryptosystem is a partial homomorphic encryption scheme.
#Multiplication and division cannot be done with two given ciphertexts.
#Instead, multiplication and division can be done with ciphertext and some scalar value.

#Parameters
p = 23 
q = 31
g = 5
ps = PaillierSystem(p, q, g)
print("Choose two values:")
p1 = 20
p2 = 4
c1 = ps.E(20)
c2 = ps.E(4)
print(f"E({p1}) = {c1}\nE({p2}) = {c2}\n")

print("Add")
c3 = ps.HAdd(c1, c2)
print(f"D({c3}) = {ps.D(c3)}")
print()

print("Sub")
c3 = ps.HSub(c1, c2)
print(f"D({c3}) = {ps.D(c3)}\n")

print("Mul")
c3 = ps.HMult(c1, p2)
print(f"D({c3}) = {ps.D(c3)}\n")

print("Div")
c3 = ps.HDiv(c1, p2)
print(f"D({c3}) = {ps.D(c3)}\n")