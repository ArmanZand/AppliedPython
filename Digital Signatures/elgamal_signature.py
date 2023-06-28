import hashlib
import math
import os
class utilities:
    @classmethod
    def testPrime(self, candidate: int, tests: int = 10) -> bool:
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
    def gcd(cls, a: int, b: int) -> int:
            '''Finds and returns the Greatest Common Divisor (GCD) of integers 'a' and b' using the Euclidean Algorithm.'''
            if a > b:
                    a, b = b,a
            r = a % b
            while r > 0:
                    a, b = b, r
                    r = a % b
            return b
    @classmethod
    def hash_message(cls, s: str) -> int:
        '''Double hash input string and return integer review.'''
        return int(hashlib.sha256( hashlib.sha256(s.encode("utf-8")).digest()).hexdigest(),16)
    @classmethod
    def random_relatively_prime(cls, n: int) -> int:
        '''Find and return a random value 'r' such that 'r' and 'n' are relatively prime.'''
        while True:
            r = cls.secure_next_int(n>>1, n-1)
            if (cls.gcd(r, n) == 1):
                return r
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

class message:
    def __init__(self, message, publicKey, signature):
        self.message = message
        self.publicKey = publicKey
        self.signature = signature
    def __repr__(self):
        return """Message      | {}
Public Key   | {}
Verifiable   | {}""".format(self.message, self.publicKey, self.signature.verify(self.message, self.publicKey))

class elgamal_signature_scheme:
    def __init__(self, privateKeyX: int, p: int = pow(2,607) - 1) -> None:
        '''Prepares parameters for digitally signing a message. An example prime 'p' is pre-set.'''
        self.primeP = p
        self.generator = 5
        self.x = privateKeyX
        self.y = pow(self.generator, privateKeyX, self.primeP)
        self.k = utilities.random_relatively_prime(self.primeP - 1)
    def sign(self, messageM: str) -> message:
        '''Digitally sign the given message 'str' and return an object containing the tools and values to verify the message.'''
        m = utilities.hash_message(messageM)
        if(m < 0 and m > (self.primeP - 1)):
            raise ValueError("Invalid signing, prime smaller than message.")
        s1 = pow(self.generator, self.k, self.primeP)
        kr = pow(self.k, -1, self.primeP - 1)
        s2 = kr * (m - self.x*s1) % (self.primeP - 1)
        return message(messageM, self.y, signature(self.generator, self.primeP, s1, s2))
class signature:
    def __init__(self, generator, primeP, S1, S2):
        '''Checks and stores parameters which are used in the signature verification procedure.'''
        errors = ""
        if(not utilities.testPrime(primeP)):
            errors += "\nPrime P is not a prime number."
        if(generator < 1 or generator > primeP - 1):
            errors += "\nGenerator cannot be less than 1 or greater than Prime P - 1"
        if(errors != ""):
            raise ValueError(errors)
        self.generator = generator
        self.primeP = primeP
        self.s1 = S1
        self.s2 = S2
    def __repr__(self):
        return """S1           | {}
S2           | {}""".format(self.s1, self.s2)
    def verify(self, messageM, publicKeyY):
        '''Checks the correctness of the message and signature values given the public parameters.'''
        m = utilities.hash_message(messageM) 
        v1 = pow(self.generator, m, self.primeP)
        v2 = (pow(publicKeyY, self.s1, self.primeP) * pow(self.s1, self.s2, self.primeP)) % self.primeP
        return v1 == v2
