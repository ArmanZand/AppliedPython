from poly_secretsharing import *

print("Herzberg Proactive Secret Sharing")

p = 23
print("Choose prime p: {p}\n")

dealerSecret = 5
dealerPoly = univariate_polynomial([dealerSecret,10,15], p)
print(f"Choose the dealer's polynomial:\n{dealerPoly}\n")


originalShares = dealerPoly.eval_range([1,2,3,4,5])
print(f"The dealer sends shares to respective players:\n{originalShares}\n>Players 1, 2 and 3 wish to exclude other players from recovering the secret.\n")

player1Regen = univariate_polynomial([0,11,16],p)
player2Regen = univariate_polynomial([0,12,17],p)
player3Regen = univariate_polynomial([0,13,18],p)
print(f"Players generate random polynomials with secret = 0:\nPlayer 1: {player1Regen}\nPlayer 2: {player2Regen}\nPlayer 3: {player3Regen}\n")

print(f"Players 1,2 and 3 send shares between each other:")
player1Shares = player1Regen.eval_range([1,2,3])
print(f"Player 1 produces: {player1Shares}\n")
player2Shares = player2Regen.eval_range([1,2,3])
print(f"Player 2 produces: {player2Shares}\n")
player3Shares = player3Regen.eval_range([1,2,3])
print(f"Player 3 produces: {player3Shares}\n")



player1Share = share(1, (originalShares[0].y + player1Shares[0].y + player2Shares[0].y + player3Shares[0].y) % p)
print(f"Player 1's refreshed share: {player1Share}\n")
player2Share = share(2, (originalShares[1].y + player1Shares[1].y + player2Shares[1].y + player3Shares[1].y) % p)
print(f"Player 2's refreshed share: {player2Share}\n")
player3Share = share(3, (originalShares[2].y + player1Shares[2].y + player2Shares[2].y + player3Shares[2].y) % p)
print(f"Player 3's refreshed share: {player3Share}\n")

lp = lagrange_polynomial(p)
recoverSecret = lp.interpolate_secret([player1Share, player2Share, player3Share])
print("Combining / Interpolating the shares of player 1, 2 and 3 gives:")
print(recoverSecret.y)

