#python3.8.8 64-bit
from matrix_secretsharing import * 
print("Choose a prime integer")
p = 97
print(p)
print()

print("Construct a vector or a matrix")
print("Univariate Coefficient vector:")
a = matrix([[5,10,15]], p)
print(a)
print("Bivariate Coefficient Matrix:")
A = matrix([[5,25,50],[25,7,30],[50,30,49]],p)
print(A)
print()

print("Generate an indeterminate Vandermonde vector by index and length")
v1 = matrix_utils.v(1,3,p).T()
print(v1)
print()

print("Generate a Vandermonde matrix to produce shares")
V1 = matrix_utils.V([1,2,3],p)
print("Vandermonde Matrix:")
print(V1)
shares = a * V1
print("Produced Shares:")
print(shares)
inv_V1 = matrix_utils.V([1,2,3],p).inv()
print("Combined Shares:")
print(shares * inv_V1)
print()

print("Perform Bivariate Secret Sharing")
biv = A * V1
print("Coefficient matrix multiplied by Vandermonde matrix:")
print(biv)
print("Coefficient recovery by matrix inverse of Vandermonde:")
print(biv * V1.inv())
#print(matrix_utils.V([0,1,2],p).inv() * matrix_utils.V([0,1,2],p))

print()

print("Symmetric Bivariate Pre-defined Secret Sharing")
x_vander = matrix_utils.V([1,2,3],p)
y_vander = matrix_utils.V([2,3,5],p)
print("X Vandermonde:")
print(x_vander)
print("Y Vandermonde:")
print(y_vander)
print("A Matrix:")
print(A)
print("B Matrix (B=X*A*Y):")
B = x_vander * A * y_vander
print(B)

print("Recover A:")
rec_A = x_vander.inv() * B * y_vander.inv()
print(rec_A)
print()