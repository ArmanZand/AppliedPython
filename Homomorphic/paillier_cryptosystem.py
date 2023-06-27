import math, os

class utilities:
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
    def modular_inverse(cls, a: int, m: int) -> int: 
        '''Finds and returns the modular inverse of integer 'a' given integer 'm' using the Extended Euclidean Algorithm (eGCD).'''
        i = m 
        y = 0
        x = 1
        if (m == 1) : 
                return 0
        while (a > 1) : 
                q = a // m 
                t = m 
                m = a % m 
                a,t = t,y
                y = x - q * y 
                x = t 
        return x % i
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
    def lcm(cls, a: int, b: int) -> int:
        '''Finds and returns the Lowest Common Multiple (LCM) of integers 'a' and 'b'.'''
        return a * b // cls.gcd(a,b)

class paillier_system:
    def __init__(self, p: int, q: int, g: int) -> None:
        #Euler's Totient Function, checks prime integers 'p' and 'q' are relatively prime
        assert(utilities.gcd(p * q, (p-1) * (q - 1)) == 1)
        self.n = p * q
        self.n2 = self.n * self.n
        self.g = g
        self.lam = utilities.lcm(p-1,q-1)
        self._random_min = 1
        self._random_max = self.n2 - 1
        _u = self.l(pow(g, self.lam, self.n2))
        self.m_u = _u * pow(1, self.n-2, self.n)
    @property
    def random_min(self):
        return self._random_min
    @property
    def random_max(self):
        return self._random_max
    def l(self, x: int) -> int:
        '''Function that divides p * q and differentiates from modular division.'''
        return (x - 1) // self.n
    def E(self, message: int) -> int:
        '''Encrypts a message and returns a ciphertext which can be operated on.'''
        r = utilities.secure_next_int(1, self.n2 - 1)
        return pow(self.g, message, self.n2) * pow(r, self.n, self.n2) % self.n2
    def D(self, cipher: int) -> int:
        '''Decrypts the ciphertext and returns the plaintext.'''
        l_f = self.l(pow(cipher, self.lam, self.n2))
        return l_f * utilities.modular_inverse(self.m_u, self.n) % self.n
    def HAdd(self, cipher1: int, cipher2: int) -> int:
        '''Add two encrypted values together and return the encrypted result.'''
        return (cipher1 * cipher2) % self.n2
    def HSub(self, cipher1: int, cipher2: int) -> int:
        '''Subtract two encrypted values and return the encrypted result.'''
        return (cipher1 * pow(cipher2, self.n - 1, self.n2)) % self.n2
    def HMult(self, cipher1: int, coef: int) -> int:
        '''Multiply an encrypted value by a scalar and return the encrypted result.'''
        return pow(cipher1, coef, self.n2)
    def HDiv(self, cipher1: int, coef: int) -> int:
        '''Divide the encrypted value by a scalar and return the encrypted result.'''
        return self.HMult(cipher1, utilities.modular_inverse(coef, self.n2))