from schnorr_signature import *

if __name__ == "__main__":
    '''Main guard required due to multithreading work for prime finding.'''
    print("Example Schnorr's Signature Scheme")
    prime = pow(2, 1279) - 1
    print(f"Prime Length: {prime.bit_length()} bits - Prime Test: {utilities.test_prime(prime)}\n")
    
    print("Initialising Signature Parameters...\n")
    schnorr_ss = schnorr_signature_scheme(prime)
    
    print("Choosing a private key:")
    schnorr_ss.gen_private_key()
    print(f"{schnorr_ss.s}\n")
    
    m = "this is a digitally signed message"
    print(f"Signing message: {m}")
    signed_message = schnorr_ss.sign(m)
    print(f"Digital Signature Pair Value (e, y):\ne: {signed_message.signature.e}\ny: {signed_message.signature.y}\n")
    
    print(f"Verify Procedure: {signed_message.signature.verify(m)}")