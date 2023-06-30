from ecc import *

class ecdsa:
    def __init__(self, curve, private_key) -> None:
        if (1 > private_key > curve.n - 1):
            raise Exception(f"Private key must be between 1 and {curve.n - 1}")
        self.curve = curve
        self.d = private_key
        self.Q = self.d * self.curve.G
    def sign(self, messageM: str):
        '''ECDSA digital signining algorithm of a message which returns signature pairs (r, s).'''
        r = 0
        while r == 0:
            k = utilities.secure_next_int(1, self.curve.n - 1)
            P = k * self.curve.G
            r = P.x % self.curve.n
        t = pow(k, -1, self.curve.n)
        e = utilities.hash_message(messageM)
        s = (t * (e + (self.d * r))) % self.curve.n
        return message(messageM, ecdsa_signature(r, s, self.Q, self.curve))

class ecdsa_signature:
    def __init__(self, r, s, Q, curve) -> None:
        self.r = r
        self.s = s
        self.Q = Q
        self.curve = curve
    def verify(self, messageM: str) -> bool:
        '''ECDSA signature verification algorithm of a message using pair values "r", "s" and public information.'''
        e = utilities.hash_message(messageM)
        w = pow(self.s, -1, self.curve.n)
        u_1 = e * w
        u_2 = self.r * w
        X = (u_1 * self.curve.G) + (u_2 * self.Q)
        if(X == point(None, None, self)):
            return False
        v = X.x % self.curve.n
        return v == self.r
class message:
    '''Object which holds the string message and signature values that would be communicated to a public key holder.'''
    def __init__(self, message: str, signature: ecdsa_signature) -> None:
        self.message = message
        self.signature = signature


