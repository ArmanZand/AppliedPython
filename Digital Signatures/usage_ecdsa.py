from ecdsa import *
#secp256r1 parameters
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
ecurve = elliptic_curve(a,b, p, n)
ecurve.setBasePoint(
    0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 
    0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

print("Elliptic Curve Digitial Signature Algorithm Example")

print(f"{ecurve}\n")
secret = utilities.secure_next_int(1, ecurve.n - 1)
print(f"Private Key: {secret}\n")
es = ecdsa(ecurve, secret)
m = "an elliptic curve was used to sign this message"
ds = es.sign(m)
print(f"Public Key:\nx: {es.Q.x}\ny: {es.Q.y}\n")
print(f"Digital Signature\nmessage: {m}\nr: {ds.signature.r}\ns: {ds.signature.s}")

print(f"Verifiable: {ds.signature.verify(m)}")
