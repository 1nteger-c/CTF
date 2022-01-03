# Directly taken from rbtree's LLL repository
# From https://oddcoder.com/LOL-34c3/, https://hackmd.io/@hakatashi/B1OM7HFVI
from sage.modules.free_module_integer import IntegerLattice
from Crypto.Util.number import *
def Babai_CVP(mat, target):
    M = IntegerLattice(mat, lll_reduce=True).reduced_basis
    G = M.gram_schmidt()[0]
    diff = target
    for i in reversed(range(G.nrows())):
        diff -=  M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
    return target - diff
 
 
def solve(mat, lb, ub, weight = None):
    num_var  = mat.nrows()
    num_ineq = mat.ncols()
 
    max_element = 0 
    for i in range(num_var):
        for j in range(num_ineq):
            max_element = max(max_element, abs(mat[i, j]))
 
    if weight == None:
        weight = num_ineq * max_element
 
    # sanity checker
    if len(lb) != num_ineq:
        print("Fail: len(lb) != num_ineq")
        return
 
    if len(ub) != num_ineq:
        print("Fail: len(ub) != num_ineq")
        return
 
    for i in range(num_ineq):
        if lb[i] > ub[i]:
            print("Fail: lb[i] > ub[i] at index", i)
            return
 
        # heuristic for number of solutions
    DET = 0
 
    if num_var == num_ineq:
        DET = abs(mat.det())
        num_sol = 1
        for i in range(num_ineq):
            num_sol *= (ub[i] - lb[i])
        if DET == 0:
            print("Zero Determinant")
        else:
            num_sol //= DET
            # + 1 added in for the sake of not making it zero...
            print("Expected Number of Solutions : ", num_sol + 1)
 
    # scaling process begins
    max_diff = max([ub[i] - lb[i] for i in range(num_ineq)])
    applied_weights = []
 
    for i in range(num_ineq):
        ineq_weight = weight if lb[i] == ub[i] else max_diff // (ub[i] - lb[i])
        applied_weights.append(ineq_weight)
        for j in range(num_var):
            mat[j, i] *= ineq_weight
        lb[i] *= ineq_weight
        ub[i] *= ineq_weight
 
    # Solve CVP
    target = vector([(lb[i] + ub[i]) // 2 for i in range(num_ineq)])
    result = Babai_CVP(mat, target)
 
    for i in range(num_ineq):
        if (lb[i] <= result[i] <= ub[i]) == False:
            print("Fail : inequality does not hold after solving")
            break
    
        # recover x
    fin = None
 
    if DET != 0:
        mat = mat.transpose()
        fin = mat.solve_right(result)
    
    ## recover your result
    return result, applied_weights, fin


f = open("output.txt",'rb')
a = f.read().split(b'\n')
p = int(a[0])
params = eval(a[1])

M = Matrix(ZZ,6)
lb = [0] * 6
ub = [0] * 6 
for i in range(5):
    M[0,i] = (params[i][0] - params[i+1][0]) % p
    M[i+1,i] = p
    dy = (params[i][1] - params[i+1][1]) % p
    lb[i] = -1 * (2 ^ 638) - dy
    ub[i] = (2^638) - dy
M[0,5] = 1
lb[-1] = 0
ub[-1] = 2 ^ 319


result, applied_weights, fin = solve(M, lb, ub)
print(long_to_bytes(int(fin[0])))
#SECCON{9dd4e461268c8034f5c8564e155c67a6}