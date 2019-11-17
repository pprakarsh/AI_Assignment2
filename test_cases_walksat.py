import random

ratio = 0.1
count = 0
while(ratio <= 8):
    for i in range(20):
        fname = "test"+"_"+str(round(ratio,1))+"_"+str(i)+".txt"
        file = open(fname, "w")
        n = random.randint(1, 100)
        m = round(ratio*n)
        file.write(f"p cnf {n} {m}\n")
        for j in range(m):
            k = random.randint(1, n)
            li = random.sample(range(1,n+1), k)
            k_negs = random.randint(0,k)
#            print(f"k is {k}, k_negs is {k_negs}")
            ind_neg = random.sample(range(1,k+1), k_negs)
            for l in range(len(li)):
                if (l+1) in ind_neg:
                    file.write(str(-li[l])+" ")
                else:
                    file.write(str(li[l])+" ")
            file.write("\n")
    ratio += 0.1
    count += 1
    file.close()
