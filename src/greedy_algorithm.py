from Lab_work_class import Lab_work
from Solution_class import Solution
import csv
def greedy_algorithm(T, N, n, p):
    labs = []
    for i in range(T):
        labs.append(Lab_work(p[i], n[i]))
    solution = Solution(T)
    A = {}
    for i in range(N):
        for j in range(T):
            if solution.x[j] < n[j]:
                A[j] = labs[j].P[solution.x[j]+1]/(solution.x[j]+1)
        lab_num = list(A.keys())
        probabilities = list(A.values())
        a = max(probabilities)
        best = lab_num[probabilities.index(a)]
        solution.x[best] += 1
        solution.increase_z(labs[best].P[solution.x[best]])
        A.clear()
    return solution

if __name__ == "__main__":
    T = 0
    N = 0
    n = []
    p = []
    with open("src/problems.csv", 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if T == 0:
                T = int(row[0])
                N = int(row[1])
            else:
                n.append(int(row[0]))
                p.append(float(row[1]))
    
    print (greedy_algorithm(T, N, n, p))
