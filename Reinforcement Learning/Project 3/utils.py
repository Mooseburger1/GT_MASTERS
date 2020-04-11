from cvxopt import matrix, solvers
from scipy.optimize import linprog
import numpy as np
from numpy import array, eye, hstack, ones, vstack, zeros




def solve_lp(q):
    
    
    c = np.zeros(5 + 1)
    c[0] = -1
    A_ub = np.ones((5, 5 + 1))
    A_ub[:, 1:] = -q.T
    b_ub = np.zeros(5)
    A_eq = np.ones((1, 5 + 1))
    A_eq[0, 0] = 0
    b_eq = [1]
    bounds = ((None, None),) + ((0, 1),) * 5

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

    
    return res.x[0] , res.x[1:]




solvers.options['show_progress'] = False


def solve_maximin(q):

    glpksolver = 'glpk'
    solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}
    solvers.options['msg_lev'] = 'GLP_MSG_OFF'
    solvers.options['LPX_K_MSGLEV'] = 0

    G = np.vstack((q.T, np.eye(5))) * -1
    
    G = np.hstack( (np.ones((10,1)) , G) )

    G[5:, 0] = 0

    G = matrix(G)
    
    A =  matrix([[0.], [1.], [1.], [1.], [1.], [1.]])
   

    h = matrix([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
    b = matrix([1.0])
    c = matrix([-1.0, 0.0, 0.0, 0.0, 0.0, 0.0])

   
    sol = solvers.lp(c,G,h,A,b, solver=glpksolver)

    
    return sol['primal objective'], sol['x']



def solve_ceq(q1, q2):

    glpksolver = 'glpk'
    solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}  # cvxopt 1.1.8
    solvers.options['msg_lev'] = 'GLP_MSG_OFF'  # cvxopt 1.1.7
    solvers.options['LPX_K_MSGLEV'] = 0  # previous versions

    M = matrix(q1).trans()
    n = M.size[1]

    A = np.zeros((2 * n * (n - 1), (n * n)))
    q1 = np.array(q1)
    q2 = np.array(q2) #TODO Possibly transpose? Code might already do this
    row = 0

    #Create system of equations for Correlated Q-Learning
    for i in range(n):
        for j in range(n):
            if i != j:
                A[row, i * n:(i + 1) * n] = q1[i] - q1[j]
                A[row + n * (n - 1), i:(n * n):n] = q2[:, i] - q2[:, j]
                row += 1

    A = matrix(A)
    # print(A.size[0])

    A = hstack((ones((A.size[0], 1)), A))
    #Constraint: All P > 0
    eye_matrix = hstack((zeros((n*n, 1)), -eye(n*n)))

    A = vstack((A, eye_matrix))
    # Constraint: Sum(P) == 1
    A = matrix(vstack((A, hstack((0,ones(n*n))), hstack((0,-ones(n*n))))))

    #Create b Matrix
    # print("A rows", A.size[0])
    # print(A)
    b = matrix(hstack((zeros(A.size[0] - 2), [1, -1])))

    # print("B", b)
    #Create C Matrix by flattening out collective sums at each a1,a2 location
    c = matrix(hstack(([-1.], -(q1+q2).flatten())))
    # print("C", c)
    sol = solvers.lp(c,A,b, solver=glpksolver)


    #Calculate Correlated Equilibrium
    if sol['x'] is None:
        return 0, 0
    dist = sol['x'][1:]
    q1_flat = q1.flatten()
    q2_flat = q2.transpose().flatten()

    #Calculated Expected return of individual players
    q1_exp_return = np.matmul(q1_flat, dist)[0]
    q2_exp_return = np.matmul(q2_flat, dist)[0]
    # print("EXPECTED GAME VALUE : {} {}".format(q1_exp_return, q2_exp_return))

    return q1_exp_return, q2_exp_return





if __name__ == '__main__':


    q = np.array([[1., 0.994, 1.59399905, 1.,1. ],
         [1., 1. , 1. , 0.994 , 1. ],
         [1. , 0.99400001 ,1. , 1. , 1. ],
         [1. , 0.99400001 ,1. , 1. , 1.  ],
         [1. , 1. , 1. , 1. , 0.98780006]])


    ans ,probs = solve_maximin(q.T * -1)

    print(ans, list(probs))