from fiat_shamir_identity import *

print("Example Fiat-Shamir Non-Interactive Identity Scheme")
prime = pow(2, 1279) -1
print(f"Prime Length: {prime.bit_length()} bits - Prime Test: {utilities.test_prime(prime)}\n")

print("Initialise Fiat-Shamir Identity Parameters\n")
fiat_shamir = fiat_shamir_identity(prime)

print("Mutual Information:")
mutual_info = "this is a mutual secret"
print(f"{mutual_info}\n")

print("Generating Proof:")
proof = fiat_shamir.createProof(mutual_info)
print(f"t: {proof.t}")
print(f"r: {proof.r}")
print()

print(f"Verify Procedure: {proof.verify(mutual_info)}")
    
