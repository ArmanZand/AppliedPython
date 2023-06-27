#python3.8.8 64-bit
from poly_secretsharing import * 

print("Choose a prime integer")
p = 97
print(p)
print()

print("Make a univariate polynomial and produce shares:")
uni_coeffs = [5,10,37]
uni_poly = univariate_polynomial(uni_coeffs, p)
print(f"Uni Poly: {uni_poly}")
uni_share = uni_poly.evaluate(4)
print(f"Evaluation Result: {uni_share}")
print()

print("Recover share to a univariate polynomial or the secret:")
lp = lagrange_polynomial(p)
uni_shares = [share(2,76), share(3,77), share(4, 55)]
result_uni_poly = lp.interpolate(uni_shares)
print(f"Interpolation Result: {result_uni_poly}")
uni_secret = lp.interpolate_secret(uni_shares)
print(f"Secret Only Interpolation: {uni_secret}")
print()

print("Make a symmetric bivariate polynomial and produce scalars:")
biv_coeffs = [[5,25,50],[25,7,30],[50,30,49]]
biv_poly = bivariate_polynomial(p, biv_coeffs)
biv_eval_poly = biv_poly.univariate_evaluate(1)
print(f"Evaluation Result: {biv_eval_poly}")
biv_scalar = biv_poly.evaluate(1,4)
print(f"Scalar: {biv_scalar}")
print()

print("Recover share to a bivariate polynomial:")
lp = lagrange_polynomial(p)
biv_scalars =[[scalar(1,64,4), scalar(2,64,4), scalar(3,32,4)], [scalar(1,26,5), scalar(2,67,5), scalar(3, 48,5)], [scalar(1,52,6), scalar(2,3,6), scalar(3,62,6)] ]
result_biv_poly = lp.bivariate_interpolate(biv_scalars)
print(result_biv_poly.coeffs)