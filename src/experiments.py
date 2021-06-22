from genetic_algorithm import genetic_algorithm
from branches_method import main as branches_method
from greedy_algorithm import greedy_algorithm
import random
import math
import matplotlib.pyplot as plt
import datetime
import csv
import os
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
    return n, p

def iterations():
    print("Iterations experiment started...")
    try:
        os.mkdir("experiments/")
    except:
        pass
    try:
        os.makedirs("experiments/figures/iterations")
    except:
        pass
    with open("experiments/iterations.csv", 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(("T", "N", "C", "Time (ms)", "Z"))
    for T in range(10, 41, 5):
        for N in [round(1.5*T), round(3*T), round(5*T)]:
            n, p = init_p_n(T, N)
            C_time = []
            C_solution = []
            for C in [20, 50, 100, 1000]:
                start_time = datetime.datetime.now()
                solution = genetic_algorithm(T, N, n, p, N/2, C)
                end_time = datetime.datetime.now()
                time_diff = end_time - start_time
                working_time = time_diff.total_seconds() * 1000
                C_time.append(working_time)
                C_solution.append(solution[len(solution)-1].z)
                iteratio = []
                z = []
                for i in range(len(solution)):
                    iteratio.append(i)
                    z.append(solution[i].z)
                plt.plot(iteratio, z, label="C = {}".format(C))
            plt.ylabel("Objective function")
            plt.xlabel("Iteration")
            plt.legend()
            plt.savefig("experiments/figures/iterations/Labs{}_Attempts{}_Iterations{}.png".format(T, N, C), format="png")
            plt.clf()
            with open("experiments/iterations.csv", 'a', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([T, N])
                writer.writerow(("", "", 20, C_time[0], C_solution[0]))
                writer.writerow(("", "", 50, C_time[1], C_solution[1]))
                writer.writerow(("", "", 100, C_time[2], C_solution[2]))
                writer.writerow(("", "", 1000, C_time[3], C_solution[3]))
                C_solution.clear()
                C_time.clear()
    print("Iterations experiment finished.")

def population_size():
    print("Population size experiment started...")
    try:
        os.mkdir("experiments/")
    except:
        pass
    with open("experiments/population_size.csv", 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(("T", "N", "C"))
    for T in range(10, 41, 5):
        for N in [round(1.5*T), round(3*T), round(5*T)]:
            n, p = init_p_n(T, N)
            res = genetic_algorithm(T, N, n, p, 100, 1000)
            optimum = res[len(res)-1].z
            C_opt = 0
            time_opt = 999999
            for C in range(5, 105, 5):
                start_time = datetime.datetime.now()
                solution = genetic_algorithm(T, N, n, p, C, 20)
                end_time = datetime.datetime.now()
                time_diff = end_time - start_time
                working_time = time_diff.total_seconds() * 1000
                if time_opt > working_time and optimum <= solution[len(solution)-1].z:
                    C_opt = C
                    time_opt = working_time
            with open("experiments/population_size.csv", 'a', encoding='utf-8-sig') as f:
                if (C_opt != 0):
                    writer = csv.writer(f)
                    writer.writerow((T, N, C_opt))
    print("Iterations experiment finished.")

def compare_algorithms():
    print("Compare algorithms experiment started...")
    try:
        os.mkdir("experiments/")
    except:
        pass
    try:
        os.makedirs("experiments/figures/algorithms_comparison")
    except:
        pass
    with open("experiments/algorithms_comparison.csv", 'w', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(("T", "N", "greedy_time (ms)", "greedy_result",
                    "genetic_time (ms)", "genetic_result", "branches_time (ms)", "branches_result"))

    N_arr = []
    grwt = []
    gewt = []
    brwt = []
    for T in range(5, 15, 1):
        for N in [round(1.1*T), round(1.2*T), round(1.3*T)]:
            N_arr.append(N)
            n, p = init_p_n(T, N)
            with open("experiments/algorithms_comparison.csv", 'a', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                start_time_greedy = datetime.datetime.now()
                res_greedy = greedy_algorithm(T, N, n, p)
                end_time_greedy = datetime.datetime.now()
                time_diff_greedy = end_time_greedy - start_time_greedy
                working_time_greedy = time_diff_greedy.total_seconds() * 1000
                grwt.append(working_time_greedy)
                
                start_time_genetic = datetime.datetime.now()
                res_genetic_list = genetic_algorithm(T, N, n, p, N/2, 20)
                res_genetic = res_genetic_list[len(res_genetic_list)-1]
                end_time_genetic = datetime.datetime.now()
                time_diff_genetic = end_time_genetic - start_time_genetic
                working_time_genetic = time_diff_genetic.total_seconds() * 1000
                gewt.append(working_time_genetic)

                start_time_branches = datetime.datetime.now()
                res_branches = branches_method(T, N, n, p)
                end_time_branches = datetime.datetime.now()
                time_diff_branches = end_time_branches - start_time_branches
                working_time_branches = time_diff_branches.total_seconds() * 1000
                brwt.append(working_time_branches)

                writer.writerow((T, N, working_time_greedy, res_greedy.z, 
                working_time_genetic, res_genetic.z, 
                working_time_branches, res_branches.z))
    for i in range(len(N_arr)):
        grwt[i] = math.log(grwt[i])
        gewt[i] = math.log(gewt[i])
        brwt[i] = math.log(brwt[i])
    plt.plot(N_arr, grwt, 'r-', label="greedy algorithm")
    plt.plot(N_arr, gewt, 'b-',label="genetic algorithm")
    plt.plot(N_arr, brwt,  'g-',label="branches method")
    plt.legend()
    plt.ylabel("ln(working time)")
    plt.xlabel("N")
    plt.savefig("experiments/figures/algorithms_comparison/plot.png", format="png")
    print("Compare algorithms experiment finished.")