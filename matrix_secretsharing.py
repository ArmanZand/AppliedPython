#python3.8.8 64-bit
#function annotations
from __future__ import annotations
from typing import Tuple, List, Any
import time
import copy

def function_execution_time(func):
    def wrap_exectionTime(*args, **kwargs) -> Any:
        '''Decorator that prints the time in milliseconds for how long a function has been running.'''
        t0 = time.perf_counter_ns()
        result = func(*args, **kwargs)
        t1 = time.perf_counter_ns()
        print(f"Time taken to execute function: {func.__name__!r} - {((t1-t0) / 1000000)} ms")
        return result
    return wrap_exectionTime

class matrix:
    '''Class to contain matrix elements compatible with arithmetic and manipulation within the same field.'''
    def __init__(self, elements: List[int][int], prime: int) -> None:
        self.height = len(elements)
        self.width = len(elements[0])
        self.p = prime
        for i in range(self.height):
            if len(elements[i]) != self.width:
                raise Exception("Matrix dimension is not consistent.")
        self.is_square = (self.height == self.width)
        self.elements = elements
    def __repr__(self) -> str:
        '''Returns a very basic string builder to represent matrix elements.'''
        if(self.height == 1): return f"[{str(self.elements[0])}]"
        rep_str = f"[{str(self.elements[0])}\n"
        for row in self.elements[1:]:
            rep_str += f" {str(row)},\n"
        rep_str = rep_str[:-2]
        rep_str += "]"
        return rep_str
    def T(self):
        return matrix_utils.transpose(self)
    @function_execution_time
    def inv(self):
        '''Inverts self matrix using determinant and adjugate finding algorithm in mod p and returns a resulting matrix.'''
        return  pow(matrix_utils.det(self), -1, self.p) * matrix_utils.adjugate(self)
    def __rmul__(self, other: matrix) -> matrix:
        '''Performs multiplication with self and other which could be an integer and returns a resulting matrix.'''
        if(isinstance(other, int)):
            return matrix_utils.scalar_multiply(other, self)
        if(isinstance(other, matrix)):
            return matrix_utils.matrix_product(self, other)
    @function_execution_time
    def __mul__(self, other: matrix) -> matrix:
        '''Performs matrix multiplication with self and another matrix and returns a resulting matrix.'''
        if(isinstance(other, matrix)):
            return matrix_utils.matrix_product(self, other)
        
class matrix_utils:
    '''Class providing static methods to generate, manipulate and perform operations on matrices.'''
    @classmethod
    def v(cls, index, size, prime) -> List[int]:
        '''Constructs and returns an indeterminate Vandermonde vector with a given index and size in mod p.'''
        new_list = []
        for i in range(size):
            new_list.append(pow(index, i, prime))
        return matrix([new_list], prime)
    @classmethod
    def V(cls, indexes: List[int], prime: int) -> matrix:
        '''Constructs a Vandermonde matrix given a list of indexes which returns a square matrix in mod p.'''
        d = len(indexes)
        new_matrix = []
        for i in range(d):
            new_matrix.append(cls.v(indexes[i], d, prime).elements[0])
        return matrix(new_matrix, prime)
    @classmethod
    def remove_row_column(cls, _matrix: matrix, row_index: int, column_index: int) -> matrix:
        '''Deletes a row and column of a matrix by its index and returns a new reduced matrix.'''
        result_matrix = copy.deepcopy(_matrix.elements)
        del result_matrix[row_index]
        for i in range(len(result_matrix)):
            del result_matrix[i][column_index]
        return matrix(result_matrix, _matrix.p)
    @classmethod
    def transpose(cls, _matrix: matrix) -> matrix:
        '''Simple transpose operation for a given matrix which returns the transposed matrix.'''
        result_matrix =  [[0] * _matrix.height for _ in range(_matrix.width)]
        for i in range(_matrix.width):
            for j in range(_matrix.height):
                
                result_matrix[i][j] = _matrix.elements[j][i]
                #result_matrix[j][i] = _matrix.elements[i][j]
        return matrix(result_matrix, _matrix.p)
    @classmethod
    def det2x2(cls, _matrix: matrix) -> int:
        '''Returns the determinant of a 2x2 matrix.'''
        m = _matrix.elements
        return (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % _matrix.p
    @classmethod
    def det(cls, _matrix: matrix) -> int:
        '''A recursive function to calculate the determinant of a given matrix of any size.'''
        if (_matrix.height == 2 and _matrix.is_square): 
            return cls.det2x2(_matrix)
        sum = 0
        for i in range(_matrix.height):
            determinant = cls.det(cls.remove_row_column(_matrix, 0, i))
            if i%2 == 0:
                sum += _matrix.elements[0][i] * determinant
            else:
                sum -= _matrix.elements[0][i] * determinant
            sum %= _matrix.p
        return sum 
    @classmethod
    def adjugate(cls, _matrix: matrix) -> matrix:
        '''An algorithm to find the adjugate of a given square matrix and returns the adjugate matrix.'''
        dimension = _matrix.height
        if (not _matrix.is_square): raise Exception("Matrix must be square.")
        p = _matrix.p
        if(_matrix.width == 2 and _matrix.height == 2):
            new_matrix = [[_matrix.elements[1][1] % p, -_matrix.elements[0][1] % p],
                          [-_matrix.elements[1][0] % p, _matrix.elements[0][0] % p]]
            return matrix(new_matrix, _matrix.p)
        new_matrix = []
        for i in range(dimension):
            new_matrix.append([])
            for j in range(dimension):
                determinant = cls.det(cls.remove_row_column(_matrix, j, i))
                if pow(-1, i +j % 2) == 1:
                    new_matrix[i].append(determinant)
                else:
                    new_matrix[i].append(-determinant) 
        return matrix(new_matrix, _matrix.p)
    @classmethod
    def scalar_multiply(cls, left_scalar: int, right_matrix: matrix) -> matrix:
        '''Returns a new matrix where each element of a given matrix is multiplied by a scalar value in mod p.'''
        d = right_matrix.height
        new_matrix = copy.deepcopy(right_matrix.elements)
        for i in range(d):
            for j in range(d):
                new_matrix[i][j] = (left_scalar * new_matrix[i][j]) % right_matrix.p
        return matrix(new_matrix, right_matrix.p)
    @classmethod
    def matrix_product(cls, left_matrix: matrix, right_matrix: matrix) -> matrix:
        '''Returns the matrix product of two given matrices as a new matrix.'''
        if (left_matrix.p != right_matrix.p): raise Exception("Matrix dot product cannot be performed on matrices in different fields.")
        result = [[0] * right_matrix.width for _ in range(left_matrix.height)]
        for i in range(left_matrix.height):
            for j in range(right_matrix.width):
                for l in range(left_matrix.width):
                    result[i][j] += left_matrix.elements[i][l] * right_matrix.elements[l][j]
                result[i][j] %= left_matrix.p
        return matrix(result, left_matrix.p)

