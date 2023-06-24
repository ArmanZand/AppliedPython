#Harn-Hsu Scheme - Bivariate Secret Sharing
#https://link.springer.com/article/10.1186/s13638-018-1086-5
#https://doi.org/10.1186/s13638-018-1086-5

from poly_secretsharing import *

#Choose a prime integer
p = 97
#Select an asymmetric matrix of coefficients where A[0][0] is the secret
A = [[5,4,3],[10,8,9],[15,12,7]]

#Put the coefficients into a bivariate polynomial object
biv_poly = bivariate_polynomial(p, A)

#Simulate the dealer producing univariate polynomials for a set of players
f_1 = biv_poly.univariate_evaluate_cross(1)
f_2 = biv_poly.univariate_evaluate_cross(2)
f_3 = biv_poly.univariate_evaluate_cross(3)

#Players use their univariate polynomial to produce and exchange shares
shares_1 = [f_1.evaluate(1,1), f_2.evaluate(1,2), f_3.evaluate(1,3)]
shares_2 = [f_1.evaluate(2,1), f_2.evaluate(2,2), f_3.evaluate(2,3)]
shares_3 = [f_1.evaluate(3,1), f_2.evaluate(3,2), f_3.evaluate(3,3)]

#Players interpolate the shares received to obtain a part of the real secret
lp = lagrange_polynomial(p)
sp1 = lp.interpolate_secret(shares_1,1)
sp2 = lp.interpolate_secret(shares_2,2)
sp3 = lp.interpolate_secret(shares_3,3)

#The parts are interpolated to recover the real secret in matrix A
secret = lp.interpolate_secret([sp1,sp2,sp3])
print(secret)



