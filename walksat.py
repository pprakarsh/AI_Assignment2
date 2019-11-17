import random
import numpy as np
import matplotlib.pyplot as py
from itertools import combinations

def FindVariablesinFalseClauses(C, M):
    S = []
    count = 0
    for i in C:
        var = []
        true = 0
        for j in i:
            if((M[abs(j)-1]==0 and j < 0) or (M[abs(j)-1]==1 and j > 0)):
                var = []
                break
            else:
                if abs(j) not in S:
                    var.append(abs(j))
        S = S + var
    return S
            
def Satisfies(M, C):
    for i in C:
        true = 0
        for j in i:
            if((M[abs(j)-1]==0 and j < 0) or (M[abs(j)-1]==1 and j > 0)):
                true = 1
                break
        if true == 0:
            return False
    return True

def flipVariables(M, S, v):
    if v >= len(S):
        li = S
    else:
        li = random.sample(S, v)

    for i in li:
        M[i-1] = (M[i-1]+1)%2
    return M

def findConflicts(var, M, C):
    Mt = M[:]
    for i in var:
        Mt[i-1] = (Mt[i-1]+1)%2
        #print(f"Mt[{i-1}]: ", Mt[i-1])

    count = 0
    for i in C:
        true = 0
        for j in i:
            if((Mt[abs(j)-1]==0 and j < 0) or (Mt[abs(j)-1]==1 and j > 0)):
                true = 1
                break
        if true == 0:
            count += 1

    return count, Mt

def flipMinConflictVariables(M, C, v):
    li = []
    for i in range(len(M)):
        li.append(i+1)

    comb = combinations(li, v)
    var = []
    Mt = M[:]
    ch_M = M[:]
    min_conflicts, Mt = findConflicts([], M, C)
    for i in comb:
        conflicts, Mt = findConflicts(i, M, C)
        if conflicts < min_conflicts:
            var = i
            ch_M = Mt
            min_conflicts = conflicts

#    print("Mininum conflicts: ", min_conflicts)
#    print("ch_M: ", ch_M)
    M = ch_M
    return M

def checkSatisfiablity(n, m, C, maxit, maxv, M, p):
    if n < maxv:
        maxv = n

    v = 0
    count = 0
    while v <= maxv: 
        v = v+1
        for i in range(maxit):
            count += 1
            if Satisfies(M, C):
                return M, count 
            S = FindVariablesinFalseClauses(C, M)
            if(random.random() >= p):
                M = flipVariables(M, S, v)
            else:
                M = flipMinConflictVariables(M, C, v)
    #print(f"Iter: {type(count)}")
    return [], count

def generateRandomModel(n):
    M = []
    for i in range(n):
        M.append(random.randint(0,1))
    return M

def input_proposition(fname):
    fp = open(fname, "r")
    firstLine = fp.readline()
    nAndm_str = firstLine[6:]
    nAndm_list = nAndm_str.split()
    n = int(nAndm_list[0])
    m = int(nAndm_list[1])
    C = []
    line = fp.readline()
    while line:
        li = line.split()
        li = list(map(int, li))
        C.append(li)
        line = fp.readline()
    fp.close()

    #print("The clause is- ")
    #for i in C:
    #    print(i)

    return n, m, C



print("\n\n")
maxit = int(input("Maxiumum number of Assignments to be tried in each run                                                                         : "))
maxv = int(input("Maximum number of variables to be simultaneously split                                                                         : "))
p = float(input("Enter probability 0<= p < 1 for choosing between flipping variables randomly or flipping variables with minimum conflict (1-p) : "))

ratio = 0.1
y = []
x = []
it = []

x = np.arange(0.1, 8.1, 0.1)

while ratio <= 8:
    prob = 0
    iterations = 0
    for i in range(20):
        count = 0
        fname = "test"+"_"+str(round(ratio,1))+"_"+str(i)+".txt"
#        fname = "test_7.9_1.txt"
        print("Filename: ", fname)
        fname = "TestCases/" + fname

        n, m, C = input_proposition(fname)
        M = generateRandomModel(n)
        #n = 3
        #m = 8
        #C = [[1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3], [-1, 2, 3], [-1, 2, -3], [-1,-2,3], [-1, -2, -3]]
        #M = [0, 0, 0]

        #print("Model generated is M: ", M)

    #for i in range(100):
    #        ans = Satisfies(M, C)
    #        print(ans)
    #        if ans == False:
    #            S = FindVariablesinFalseClauses(C, M)
    #            print("Variables in False Clauses: ", S)
    #            print("Model after flipping", flipMinConflictVariables(M, C, 1))
    #        print("\n\n")

        M, count = checkSatisfiablity(n, m, C, maxit, maxv, M, p)
        iterations = iterations + count 
        if(M != []):
            prob += 0.05
            print(f"Model which satisfies the proposition statement is: {M}\n")
        else:
            print("The problem is unsatisfiable\n")

    it.append(iterations/20)
    y.append(prob)
    ratio += 0.1

py.plot(x,y)
py.xlabel("(Clauses/Symbol) ratio (m/n)")
py.ylabel("(P(satisfiable))")
py.show()

py.plot(x, it)
py.xlabel("(Clauses/Symbol) ratio (m/n)")
py.ylabel("Total iterations")
py.show()

