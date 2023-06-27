from __future__ import annotations
from typing import Tuple, List, Any
import time
import math, os

def secure_next_int(min: int, max: int) -> int:
    '''Find a random integer between the given range with cryptographically secure RNG.'''
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

def function_execution_time(func):
    def wrap_exectionTime(*args, **kwargs) -> Any:
        '''Decorator that prints the time in milliseconds for how long a function has been running.'''
        t0 = time.perf_counter_ns()
        result = func(*args, **kwargs)
        t1 = time.perf_counter_ns()
        print(f"Time taken to execute function: {func.__name__!r} - {((t1-t0) / 1000000)} ms")
        return result
    return wrap_exectionTime

class share:
    '''Distinct class for univariate points.'''
    def __init__(self, x: int, y:int) -> None:
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
        
class scalar:
    '''Distinc class for bivariate points.'''
    def __init__(self, x:int, y:int, z:int) -> None:
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self) -> str:
        return f"({self.x}|{self.z}, {self.y})"


class univariate_polynomial:
    '''Object that holds univariate coefficients which can be used to produce shares and can be obtained by interpolation.'''
    def __init__(self, coeffs: List[int], p: int) -> None:
        self.coeffs = coeffs
        self.p = p
    @function_execution_time
    def evaluate(self, x: int, set_x: int = None) -> share:
        '''Evaluate the polynomial with current coefficents at 'x', set_x to change x value of returned share (Useful for bivariate operations).'''
        sum = 0
        for i in range(len(self.coeffs)):
            sum += self.coeffs[i] * pow(x, i, self.p) 
        if(set_x != None):
            return share(set_x, sum % self.p)
        return share(x, sum % self.p) 
    def eval_range(self, x_range: List[int]) -> List[share]: 
        '''Evaluate the polynomial for a range of specific 'x' values.'''
        points = []
        for x in x_range:
            points.append(self.evaluate(x))
        return points
    def __repr__(self) -> str:
        return "".join([f"{self.coeffs[i]}x^{i} + " for i in range(len(self.coeffs))])[:-3]

class bivariate_polynomial:
    '''Object that holds bivariate coefficients which can be used to produce scalars and can be obtained by bivariate interpolation.'''
    def __init__(self, p: int, coeffs: List[int][int] = None) -> None:
        self.p = p
        self.coeffs = coeffs
    @function_execution_time
    def univariate_evaluate(self, x: int) -> univariate_polynomial:
        '''Evaluate the current coefficients to produce a univariate polynomial with respect to 'x'.'''
        if self.coeffs == None: raise Exception("No coefficients have been initialised.")
        uni_coeffs = []
        d = len(self.coeffs[0])
        for i in range(d):
            uni_coeffs.append(0)
            for j in range(d):

                uni_coeffs[i] += self.coeffs[j][i] * pow(x,i, self.p) % self.p
            uni_coeffs[i] %= self.p
        return univariate_polynomial(uni_coeffs, self.p) 
    @function_execution_time
    def univariate_evaluate_cross(self, y: int) -> univariate_polynomial:
        '''Evaluate the current coefficients with swapped indexes to produce a univariate polynomial with respect to 'x'.'''
        if self.coeffs == None: raise Exception("No coefficients have been initialised.")
        uni_coeffs = []
        d = len(self.coeffs[0])
        for i in range(d):
            uni_coeffs.append(0)
            for j in range(d):
                uni_coeffs[i] += self.coeffs[i][j] * pow(y,j, self.p) % self.p
            uni_coeffs[i] %= self.p
        return univariate_polynomial(uni_coeffs, self.p) 
    def evaluate(self, x: int, z: int) -> scalar:
        '''Evaluate the current coefficients to produce a scalar given 'x' and 'z'.'''
        if self.coeffs == None: raise Exception("No coefficients have been initialised.")
        return self.bivariate_evaluate(x, z)
    @function_execution_time
    def bivariate_evaluate(self, x: int, z: int):
        sum = 0
        d = len(self.coeffs[0])
        for i in range(d):
            for j in range(d):
                sum += self.coeffs[i][j] * pow(x,i, self.p) * pow(z,j, self.p)
        sum %= self.p
        return scalar(x, sum, z)
    def construct(self, primary_poly: univariate_polynomial):
        '''Given a secret by the input univariate polynomial, this function populates the bivariate coefficient with random integers symmetrically.'''
        d = len(primary_poly.coeffs)
        self.coeffs = [[0 for i in range(d)] for j in range(d)]
        for i in range(d):
            for j in range(d):
                if i == 0:
                    self.coeffs[i][j] = primary_poly.coeffs[j]
                    self.coeffs[j][i] = primary_poly.coeffs[j]
                elif j > 0:
                    u_random = secure_next_int(0, self.p-1)
                    self.coeffs[i][j] = u_random
                    self.coeffs[j][i] = u_random

class member:
    def __init__(self, value: int, deg: int) -> None:
        '''Member class that tracks a symbol's coefficient and exponent.'''
        self.value = value
        self.deg = deg

class bracket:
    def __init__(self, members: List[member]) -> None:
        '''Bracket object which contains a list of members.'''
        self.members = members
    def multiply_with(self, otherBracket: bracket) -> bracket:
        '''Expand current bracket by multiplying with another bracket.'''
        result = []
        for i in range(len(self.members)):
            for j in range(len(otherBracket.members)):
                result.append(member(self.members[i].value * otherBracket.members[j].value, self.members[i].deg + otherBracket.members[j].deg))
        for i in range(len(result) -1, -1,-1):
            for j in range(len(result)-1,-1,-1):
                if(i != j):
                    if(result[i].deg == result[j].deg):
                        result[i].value += result[j].value
                        result.remove(result[j])
        return bracket(result)

class lagrange_polynomial:
    def __init__(self, p: int) -> None:
        '''Initialise the Lagrange Basis Polynomial class with some prime 'p'.'''
        self.p = p
    def create_fractions(self, points: List[share]) -> Tuple[List[int], List[int]]:
        '''Given a series of points, the 'x' values are used to create a list of numberators and denominators according to the Lagrange basis.'''
        numerators = []
        denominators = []
        for j in range(self.k):
            numerators.append([])
            denominators.append(1)
            for m in range(self.k):
                if(m != j):
                    numerators[j].append(-points[m].x)
                    denominators[j] *= (points[j].x - points[m].x)
        return numerators, denominators
    def expand_brackets(self, numerators: List[int]) -> List[bracket]:
        '''The numerators are organised into brackets and are expanded.'''
        expanded_brackets = []
        for i in range(len(numerators)):
            expanded_brackets.append(bracket([member(1,1), member(numerators[i][0],0)]))
            for j in range(len(numerators[i])-1):
                b = bracket([member(1,1), member(numerators[i][j+1],0)])
                expanded_brackets[i] = expanded_brackets[i].multiply_with(b)
        return expanded_brackets
    @function_execution_time
    def interpolate(self, points: List[share]) -> univariate_polynomial:
        '''Find the Lagrange Basis Polynomial with a list of points.'''
        self.k = len(points)
        numerators, divisors = self.create_fractions(points)
        expanded_brackets = self.expand_brackets(numerators)
        fB = [0 for i in range(len(expanded_brackets))]
        for i in range(len(expanded_brackets)):
            for j in range(len(expanded_brackets[i].members)):
                expanded_brackets[i].members[j].value = expanded_brackets[i].members[j].value * (points[i].y)
                fB[len(expanded_brackets[i].members) - j - 1] += (expanded_brackets[i].members[j].value * pow(divisors[i], -1, self.p)) % self.p
                fB[len(expanded_brackets[i].members) - j - 1] %= self.p  
        return univariate_polynomial(fB, self.p)
    @function_execution_time
    def interpolate_secret(self, points: List[share], set_x: int = None) -> share:
        '''Finds the secret with the given set of shares without having to compute the remaining coefficients. Use set_x to change x value of returned share useful for bivariate operations.'''
        k = len(points)
        sum = 0
        for j in range(k):
            pi = 1
            for m in range(k):
                if(j != m):
                    pi *= points[m].x * pow(points[m].x - points[j].x, -1, self.p) % self.p
            sum = (sum + (points[j].y * pi)) % self.p
        if(set_x != None):
            return share(set_x, sum)
        return share(0, sum)
    @function_execution_time
    def bivariate_interpolate(self, point_vectors: List[int, List[scalar]]) -> None:
        '''Given a square matrix of scalars, the points can be interpolated to obtain the coefficient of a bivariate polynomial.'''
        d = len(point_vectors[0])
        new_point_vectors = [[0 for i in range(d)] for j in range(d)]
        for i in range(d):
            if(len(point_vectors[i]) != d): raise Exception("Inconsistent size of points vector.")
            z = point_vectors[i][0].z
            if(z == -1): raise Exception("Point z value is not set.")
            lbp = lagrange_polynomial(self.p)
            lagrange_poly = lbp.interpolate(point_vectors[i])
            for j in range(d):
                new_point_vectors[j][i] = share(z, lagrange_poly.coeffs[j])
        coeffs = [[0 for i in range(d)] for j in range(d)]
        for i in range(d):
            lbp = lagrange_polynomial(self.p)
            recover_poly = lbp.interpolate(new_point_vectors[i])
            for j in range(d):
                coeffs[i][j] = recover_poly.coeffs[j]
        return bivariate_polynomial(self.p, coeffs)

