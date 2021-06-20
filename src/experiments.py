from genetic_algorithm import genetic_algorithm
from branches_method import branches_method
import random
import math
import matplotlib.pyplot as plt
import datetime
import csv
def init_p_n(T, N):
    p = []
    n = []
    for t in range(T):
        if random.random() > 0.5:
            p.append(random.uniform(0.01, 0.99))
        else:
            p.append(random.uniform(0.3, 0.7))
        if random.random()>0.5:
            n.append(random.randint(int(math.ceil(0.2*N)), int(math.ceil(1.8*N))))
        else:
            n.append(random.randint(round(0.8*N), round(1.2*N)))
        while sum(n) <= N:
            n.clear()
            if random.random()>0.5:
                n.append(random.randint(int(math.ceil(0.2*N)), int(math.ceil(1.8*N))))
            else:
                n.append(random.randint(round(0.8*N), round(1.2*N)))
    return p, n

def iterations():
    for T in range(10, 41, 5):
        for N in [round(1.5*T), round(3*T), round(5*T)]:
            p, n = init_p_n(T, N)
            for C in [20, 50, 100]:
                
                solution = genetic_algorithm(T, N, n, p, 10, C)
                
                iteratio = []
                z = []
                for i in range(len(solution)):
                    iteratio.append(i)
                    z.append(solution[i].z)
                plt.text(len(solution)/2, (z[len(z)-1]+z[0])/2, "C = {}".format(C), fontsize=15)
                plt.plot(iteratio, z)
                plt.ylabel("Objective function")
                plt.xlabel("Iteration")
                plt.savefig("src/figures/iterations/Labs{}_Attempts{}_Iterations{}.png".format(T, N, C), format="png")

def population_size():
    with open("experiments/population_size.csv", 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(("T", "N", "C"))
    for T in range(10, 41, 5):
        for N in [round(1.5*T), round(3*T), round(5*T)]:
            p, n = init_p_n(T, N)
            res = genetic_algorithm(T, N, n, p, 10, 1000)
            optimum = res[len(res)-1].z#branches_method(T, N, n, p)
            C_opt = 0
            time_opt = 999999
            for C in range(5, 105, 5):
                start_time = datetime.datetime.now()
                solution = genetic_algorithm(T, N, n, p, C, 20)
                end_time = datetime.datetime.now()
                time_diff = end_time - start_time
                working_time = time_diff.total_seconds() * 1000
                print(working_time)
                if time_opt > working_time and optimum <= solution[len(solution)-1].z:
                    C_opt = C
                    time_opt = working_time
            with open("experiments/population_size.csv", 'a', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow((T, N, C_opt))

population_size()