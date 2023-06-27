from elgamal_signature import *

#prime integer
p = pow(2,607) - 1
#private key
prv_key = 5999998
eg = elgamal_signature(prv_key, p)

print(f"Private Key: {eg.x}\nPublic Key: {eg.y}")

test_message = "hello"

print(f"Message: {test_message}")
signed_message = eg.sign(test_message)

print(f"Verified Message: {signed_message.signature.verify(test_message, signed_message.publicKey)}")