from __future__ import annotations
from decimal import Decimal
from preset_primes import first_10k
import math
import os
import hashlib

class utilities:
    @classmethod
    def hash_message(cls, s: str) -> int:
        '''Double hash input string and return integer review.'''
        return int(hashlib.sha256( hashlib.sha256(s.encode("utf-8")).digest()).hexdigest(),16)
    @classmethod
    def lcm(cls, a, b):
        return a * b // cls.gcd(a,b)
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
    def crt(cls, a, m):
        '''Chinese remainder theorem returns a solution given a set of congruences from integers 'a' and moduli 'm'.'''
        M = 1
        for mi in m:
            M *= mi
            
        sum = 0
        for ai, mi in zip(a, m):
            Mi = M // mi
            sum = (sum + ai * Mi % M * pow(Mi, -1, mi)) % M
        return sum
    @classmethod
    def test_prime(cls, candidate: int, tests = 8) -> bool:
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
            a = cls.secure_next_int(2, n - 2)
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
    def mod_square_root(cls, n, p):
        '''Tonelli-Shanks Algorithm to find the square root of n mod p.'''
        #https://en.wikipedia.org/wiki/Tonelli–Shanks_algorithm
        if(pow(n, (p-1)//2, p) != 1):
            return None
        if p % 4 == 3:
            return pow(n, (p + 1) // 4, p)
        elif p % 8 == 5:
            v = pow(n << 1, (p - 5) // 8, p)
            i = pow((n * v * v << 1) % p, (p - 1) // 4, p)
            return (n * v * ((i - 1) >> 1)) % p
        s = 0
        q = p -1
        while(q % 2 == 0):
            q //= 2
            s += 1
        z = 2
        while True:
            if (pow(z, (p -1)//2, p) == p - 1):
                break
            z += 1
        m = s
        c = pow(z,q, p)
        t = pow(n,q, p)
        r = pow(n, (q+1)//2, p)
        while t != 1:
            i = 0
            temp = t
            while temp != 1:
                temp = (temp * temp) % p
                i += 1
            b = pow(c, pow(2, m - i - 1), p)
            c = (b * b) % p
            t = (t * c) % p
            r = (r * b) % p
            m = i
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
class point:
    def __init__(self, x : int, y: int, curve: elliptic_curve) -> None:
        '''Defines a point (x, y) with respect to a given curve.'''
        self.x = x
        self.y = y
        self.curve = curve
        if(x is None and y is None):
            return
        y2 = y**2 % self.curve.p
        f_x = (x**3 + curve.a * x + curve.b) % curve.p
        if (y2 != f_x):
            raise Exception(f"Co-ordinates ({x},{y}) in F_{curve.p} are not on the curve.")
    def __eq__(self, __value: point) -> bool:
        '''Compares point x,y and curve parameters.'''
        return (self.x == __value.x) and (self.y == __value.y) and (self.curve == __value.curve)
    def __neg__(self) -> point:
        '''Returns the equivalent to the negative of the current point.'''
        return point(self.x, -self.y % self.curve.p, self.curve)
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) F_{self.curve.p}"
    def __add__(self, __value: point) -> point:
        '''Add self to other point.'''
        return self.curve.add(self, __value)
    def __rmul__(self, __value: int) -> point:
        '''Multiplies the current point by a scalar value.'''
        return self.curve.scalar_mult(__value, self)
    def __truediv__(self, __value: int) -> point:
        '''Divides the current point by a scalar value.'''
        coef = pow(__value,-1, self.curve.n)
        return self.__rmul__(coef)
class elliptic_curve:
    def __init__(self, a, b, p, n=None) -> None:
        '''Curve defining parameters.'''
        self.a = a
        self.b = b
        self.p = p
        self.n = n
    def __repr__(self) -> str:
        ret_str = f"Prime: (Valid - {utilities.test_prime(self.p)})\n{self.p}\n\nOrder (Number of Points):\n{self.n}\n\nCurve: y^2 = x^3 + ax + b\na: {self.a}\nb: {self.b}"
        if( self.G is not None):
            ret_str += f"\n\nBase Point G:\nx: {self.G.x}\ny: {self.G.y}"
        return ret_str
    def __eq__(self, __value: object) -> bool:
        '''Compares self with other curve containing the same parameters.'''
        return (self.a == __value.a) and (self.b == __value.b) and (self.p == __value.p) and (self.n == __value.n)
    def setBasePoint(self, x, y) -> None:
        '''Sets a base point part of an elliptic curve scheme.'''
        self.G = point(x, y, self)
    def find_random_point(self):
        '''Finds and returns a random valid point in curve.'''
        x = None
        y = None
        while y == None:
            x = utilities.secure_next_int(1,self.p - 1)
            f_x = x**3 + self.a * x + self.b % self.p 
            y = utilities.mod_square_root(f_x, self.p)
        return point(x, y, self)
    def find_commutative_point(self):
        candidate = self.find_random_point()
        n = utilities.secure_next_int(2,self.p -1) | 1
        while True:
            res = n * candidate
            if res.x == None:
                if(utilities.test_prime(n)):
                    return candidate
                break
            n += 2
        return None
    def add(self, P, Q):
        '''Adds two points together in the same curve and returns the result.'''
        if(P.x is None):
            return Q
        if(Q.x is None):
            return P
        if(P.x == Q.x and P.y != Q.y):
            return point(None, None, self)
        if(P != Q):
            lam = (Q.y - P.y % self.p) * pow(Q.x - P.x, -1, self.p) % self.p
            r_x = (lam**2 - P.x - Q.x) % self.p
            r_y = (lam * (P.x - r_x) - P.y) % self.p
            return point(r_x, r_y, self)
        if(P == Q and P.y == 0 * P.x):
            return point(None, None, self)
        if (P == Q):
            lam = (3 * (P.x**2) + self.a) * pow(2 * P.y, -1, self.p) % self.p                        
            r_x = (lam**2 - P.x - Q.x) % self.p
            r_y = (lam * (P.x - r_x) - P.y) % self.p
            return point(r_x, r_y, self)
    def scalar_mult(self, n, P):
        '''Efficient point multiplication given a scalar value.'''
        result = point(None, None, self)
        current = P
        while n:
            if n & 1:
                result = result + current
            current = current + current
            n >>= 1
        return result

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




    
