import math
import os
import hashlib
import multiprocessing

class utilities:
    @classmethod
    def test_prime(self, candidate: int, tests = 8) -> bool:
        '''Miller-Rabin test to determine likelyhood of given integer being prime.'''
        n = candidate
        if n == 1:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        for _ in range(tests):
            a = self.secure_next_int(2, n - 2)
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    @classmethod
    def hash_message(cls, s: str) -> int:
        '''Double hash input string and return integer review.'''
        return int(hashlib.sha256( hashlib.sha256(s.encode("utf-8")).digest()).hexdigest(),16)
    @classmethod
    def secure_bits(cls, bit_length: int) -> int:
        '''Generate and return a random integer of a set bit length.'''
        return int.from_bytes(os.urandom(bit_length), byteorder="little")
    @classmethod
    def secure_next_int(cls, min: int, max: int) -> int:
        '''Find and returns a random integer between the given range with cryptographically secure RNG.'''
        if min == max: return min
        if min > max: raise Exception("Random number range max cannot be less than min.")
        i_range = max - min
        if i_range == 0: return min
        mask = i_range
        numSize = (i_range.bit_length() +7) // 8
        iter = int(math.log(numSize*8, 2))
        for i in range(iter):
            mask |= mask >> pow(2, i)
        result = 0
        while True:
            result = int.from_bytes(os.urandom(numSize), byteorder="little") & mask
            if (result <= i_range): break
        result += min
        return result

class fiat_shamir_proof:
    def __init__(self, g, t, r, p) -> None:
        self.g = g
        self.t = t
        self.r = r 
        self.p = p
    def verify(self, challenge_input: str) -> bool:
        challenge_value = utilities.hash_message(challenge_input)
        y_hat = pow(self.g, challenge_value, self.p)
        c_hat = utilities.hash_message(f"{self.g}{y_hat}{self.t}")
        t_hat = (pow(self.g, self.r, self.p) * pow(y_hat, c_hat, self.p)) % self.p
        return t_hat == self.t
class fiat_shamir_identity:
    def __init__(self, p: int) -> None:
        self.p = p
        self.g = utilities.secure_next_int(2, p - 1)
    def createProof(self, proof_input: str) -> fiat_shamir_proof:
        secret = utilities.hash_message(proof_input)
        v = utilities.secure_next_int(0, self.p - 1)
        t = pow(self.g, v, self.p)
        y = pow(self.g, secret, self.p)
        c = utilities.hash_message(f"{self.g}{y}{t}")
        r = (v - c * secret) % self.p
        return fiat_shamir_proof(self.g, t, r, self.p)
    
