from cvxopt import matrix, solvers
import numpy as np


A = np.zeros((5,4))
A[:3, 0] = 1.0
A[3, 1:] = 1.0
A[4, 1:] = -1.0


a = [[0.0, 1.0, -1.0], [-1.0, 0.0, 4.47], [1.0, -4.47, 0.0]]




for posr, row in enumerate(a):
    for posc, col in enumerate(row):

        A[posr, posc+1] = col


A = matrix(A)



b = matrix([0.0,0.0,0.0,1.0,-1.0])

c = matrix([-1.0,0.0,0.0,0.0])




test_sol = solvers.lp(c,A,b)

print(test_sol)

print(test_sol['x'])