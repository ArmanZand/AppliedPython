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
    def test_prime_alt(self, candidate: int, tests = 8) -> bool:
        '''Miller-Rabin test for larger integers'''
        n = candidate
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
    @classmethod
    def get_random_prime(cls, bit_length: int, threads: int = multiprocessing.cpu_count()) -> int:
        '''Finds and returns a probable prime with a given bit length, thread number can be set to adjust rate of prime testing.'''
        #Approximate number of tries (Divided by 2 because only odd integers are in the work space):
        #For bit length N : (N * ln(2)) / 2
        #For integer x : ln(x) / 2
        if (threads < 1):
            raise Exception("Must have at least one thread to perform this task.")
        candidate = utilities.secure_bits(bit_length) | 1
        with multiprocessing.Pool(processes=threads) as pool:
            while True:
                results = pool.map(cls.test_prime_alt, [(candidate + (2 * i )) for i in range(threads)])
                if any(results):
                    return candidate
                candidate += 2 * threads

class schnorr_signature_scheme:
    def __init__(self, p: int) -> None:
        '''Initialise suitable parameters for the signing message.'''
        self.p = p
        q_size = int(p.bit_length() // math.log(p.bit_length(), 3))
        self.q = utilities.get_random_prime(q_size)
        self.g = utilities.secure_next_int(2 , p - 1)
        self.a = pow(self.g, (p-1)//self.q, p)
    def set_private_key(self, s: int) -> None:
        '''Manually set private key.'''
        if(0 < s < self.q):
            self.s = s
            self.v = pow(self.a, -self.s, self.p)
        else:
            raise Exception(f"Private key must be between 0 and {self.q}.")
    def gen_private_key(self) -> None:
        '''Generates and sets a suitable private key.'''
        self.s = utilities.secure_next_int(0, self.q  - 1)
        self.v = pow(self.a, -self.s, self.p)
    def sign(self, messageM: str):
        '''Sign a given message and return a verifiable message.'''
        r = utilities.secure_next_int(0, self.q - 1)
        x = pow(self.a, r, self.p)
        e = utilities.hash_message(f"{messageM}{x}")
        y = (r + self.s * e) % self.q
        return message(messageM, schnorr_signature(self.v, e, y, self.a, self.p))

class schnorr_signature:
    '''Object which holds the necessary public parameters and values to verify a given message.'''
    def __init__(self, v: int, e: int, y: int, a: int, p: int) -> None:
        self.v = v
        self.e = e
        self.y = y
        self.a = a
        self.p = p
    def verify(self, message: str) -> bool:
        '''Returns the verification of the message by computing a challenge that checks the correctness of the digital signature.'''
        x_prime = (pow(self.a, self.y, self.p) * pow(self.v, self.e, self.p)) % self.p
        challenge = utilities.hash_message(f"{message}{x_prime}")
        return self.e == challenge
        
class message:
    '''Object which holds the string message and signature values that would be communicated to a public key holder.'''
    def __init__(self, message: str, signature: schnorr_signature) -> None:
        self.message = message
        self.signature = signature
