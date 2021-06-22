from genetic_algorithm import genetic_algorithm
from branches_method import main as branches_method
from greedy_algorithm import greedy_algorithm
import experiments
import csv
import random
def user_input():
    print("Input T:")
    T = int(input())
    print("Input N:")
    N = int(input())
    p = []
    n = []
    for i in range(T):
        print("input nubmer of attempts for lab {}".format(i+1))
        n.append(int(input()))
        print("input probability for lab {}".format(i+1))
        p.append(float(input()))
    return T, N, n, p

def read_from_file(filename):
    n = []
    p = []
    T = 0
    N = 0
    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if T == 0:
                T = int(row[0])
                N = int(row[1])
            else:
                n.append(int(row[0]))
                p.append(float(row[1]))
    return T, N, n, p

def generate_data(T_lower_bound, T_upper_bound, N_lower_bound, N_upper_bound, 
n_lower_bound, n_upper_bound, p_lower_bound, p_upper_bound):
    T = random.randint(T_lower_bound, T_upper_bound)
    N = random.randint(N_lower_bound, N_upper_bound)
    while N <= T:
        N = random.randint(N_lower_bound, N_upper_bound)
    n = []
    p = []
    for i in range(T):
        n.append(random.randint(n_lower_bound, n_upper_bound))
        p.append(p_lower_bound+random.random()*(p_upper_bound-p_lower_bound))
    while sum(n) <= N:
        n.clear()
        for i in range(T):
            n.append(random.randint(n_lower_bound, n_upper_bound))
    return T, N, n, p

def run_experiments():
    print("""Choose experiment:
        1) Population size (genetic algorithm)
        2) Iterations amount (genetic algrithm)
        3) Algorithms comparison
        4) Run all""")
    menu = int(input())
    if menu == 1:
        experiments.population_size()
    elif menu == 2:
        experiments.iterations()
    elif menu == 3:
        experiments.compare_algorithms()
    elif menu == 4:
        experiments.population_size()
        experiments.iterations()
        experiments.compare_algorithms()
    else:
        print("Try again")

def input_problem():
    T = 0
    N = 0
    p = []
    n = []
    print("""MENU:
        1) input data
        2) generate data
        3) read data from file""")
    menu = int(input())
    if menu == 1:
        print("Be ware that it is not recommended to input N >= 19")
        T, N, n, p = user_input()
    elif menu == 2:
        print("Be ware that it is not recommended to input N >= 19")
        print("Input lower bound for T")
        T_lower = int(input())
        print("Input upper bound for T")
        T_upper = int(input())
        print("Input lower bound for N")
        N_lower = int(input())
        print("Input upper bound for N")
        N_upper = int(input())
        print("Input lower bound for n")
        n_lower = int(input())
        print("Input upper bound for n")
        n_upper = int(input())
        print("Input lower bound for p")
        p_lower = float(input())
        print("Input upper bound for p")
        p_upper = float(input())
        T, N, n, p = generate_data(T_lower, T_upper, N_lower,
        N_upper, n_lower, n_upper, p_lower, p_upper)
    elif menu == 3:
        print("Input filename:")
        filename = input()
        T, N, n, p = read_from_file(filename)
    print("T =", T, "\nN =", N, "\nn =", n, "\np =", p)
    res = genetic_algorithm(T, N, n, p, N/2, 20)  # TODO: Change parameters
    print("Greedy algorithm: ", greedy_algorithm(T, N, n, p))
    print("Genetic algorithm: ", res[len(res)-1])
    print("Branches method: ", branches_method(T, N, n, p))

if __name__ == "__main__":
    while True:
        print("""MENU:
        1) Run experiments
        2) Input problem
        3) Exit""")
        menu = int(input())
        if menu == 1:
            run_experiments()
        elif menu == 2:
            input_problem()
        elif menu == 3:
            break
        else:
            print("Try again")
