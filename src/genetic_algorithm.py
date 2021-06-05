import random
import csv
from Solution_class import Solution
from Lab_work_class import Lab_work

T = 0
N = 0
def generate_population(U=4):
    population = []
    while len(population) < U:
        generated_labs = []
        solution = Solution(T)
        for j in range(T-1):
            r = -1
            while r in generated_labs or r == -1:
                r = random.randint(0, T-1)
            generated_labs.append(r)
            sum_attempts = sum(solution.x)
            solution.x[r] = random.randint(0, min(N-sum_attempts, Solution.labs[r].n))

        sum_attempts = sum(solution.x)
        for j in range(T):
            if j not in generated_labs:
                solution.x[j] = min(N-sum_attempts, Solution.labs[j].n)
        child_is_exists = False
        for child in population:
            if (child == solution):
                child_is_exists = True
                break
        if not child_is_exists:
            population.append(solution)
    for entity in population:
        entity.calculate_z()
    return population


def choose_parents(population, k):
    I = 5  # количество итераций, за которые не изменилась ЦФ и нужно провести аутбридинг
    if k < I:
        g = 0
        for entity in population:
            g += entity.z/len(population)
        A = []
        for i in range(len(population)):
            if population[i].z >= g:
                A.append(population[i])
        x1 = max(A)
        A.remove(x1)
        try:
            x2 = A[random.randint(0, len(A)-1)]
        except:
            x2 = x1
        return (x1, x2)
    else:
        D = []
        i_max = -1
        j_max = -1
        max_d = -1
        for i in range(len(population)-1):
            d = []
            for j in range(i+1, len(population)):
                distance = 0
                for t in range(T):
                    distance += abs(population[i].x[t] - population[j].x[t])
                d.append(distance)
                if distance > max_d:
                    i_max = i
                    j_max = j
                    max_d = distance
            D.append(d)
        return (population[i_max], population[j_max])


def create_children(x1, x2):
    i_temp = random.randint(0, T)
    j_temp = random.randint(0, T)
    while j_temp == i_temp:
        j_temp = random.randint(0, T)
    i = min(i_temp, j_temp)
    j = max(i_temp, j_temp)
    sol1 = Solution(T)
    sol2 = Solution(T)
    for t in range(T):
        if t <= i or t > j:
            sol1.x[t] = x1.x[t]
            sol2.x[t] = x2.x[t]
        else:
            sol1.x[t] = x2.x[t]
            sol2.x[t] = x1.x[t]
    if not is_feasible(sol1):
        sol1 = reanimation(sol1)
    if not is_feasible(sol2):
        sol2 = reanimation(sol2)
    sol1.calculate_z()
    sol2.calculate_z()
    return sol1, sol2


def reanimation(solution):
    while not is_feasible(solution):
        A = []
        for i in range(T):
            if solution.x[i] > Solution.labs[i].n and solution.x[i]>0:
                A.append(i)
        sum_attempts = sum(solution.x)

        if sum_attempts > N and not len(A)==0:
            t = -1
            min_p = 99999
            for a in A:
                if min_p > Solution.labs[a].P[1]:
                    min_p = Solution.labs[a].P[1]
                    t = a
            solution.x[t] -= 1
        elif sum_attempts > N:
            t = -1
            min_p = 99999
            for i in range(T):
                if Solution.labs[i].P[solution.x[i]] < min_p and solution.x[i]>0:
                    t = i
                    min_p = Solution.labs[i].P[solution.x[i]]
            solution.x[t] -= 1
        else:
            t = A[random.randint(0, len(A)-1)]
            h = random.randint(0, T-1)
            while h in A or solution.x[h] >= Solution.labs[h].n - 1:
                h = random.randint(0, T-1)
            solution.x[t] -= 1
            solution.x[h] += 1
    solution.calculate_z()
    return solution


def is_feasible(solution):
    if sum(solution.x) > N:
        return False
    for i in range(len(Solution.labs)):
        if solution.x[i] > Solution.labs[i].n:
            return False
    return True



def mutate_children(x1, x2):
    for x in (x1, x2):
        if random.random() <= 0.3:
            if T == 2:
                x.x[0], x.x[1] = x.x[1], x.x[0]
            else:
                s = random.randint(1, T-2)
                x.x[s-1], x.x[s+1] = x.x[s+1], x.x[s-1]
            if not is_feasible(x):
                x = reanimation(x)
            x.calculate_z()
    return x1, x2




def local_impovement(x1, x2):
    for x in (x1, x2):
        x_temp = Solution(T)
        x_temp.z = x.z
        for i in range(T):
            x_temp.x[i] = x.x[i]
        if random.random() <= 0.5:
            i = random.randint(0, T-1)
            j = random.randint(0, T-1)
            while j == i:
                j = random.randint(0, T-1)
            x.x[i], x.x[j] = x.x[j], x.x[i]
            if not is_feasible(x):
                x = reanimation(x)
            
        while sum(x.x) < N:
            A = []
            for i in range(T):
                if x.x[i] < Solution.labs[i].n:
                    A.append(i)
            t = A[random.randint(0, len(A)-1)]
            x.x[t] += 1
        x.calculate_z()
        if x < x_temp:
                x = x_temp
    return x1, x2


def renew_population(population, x1, x2):
    for x in (x1, x2):
        worst = min(population)
        if x > worst and x not in population:
            population.remove(worst)
            population.append(x)
    return population


def genetic_algorithm(T_, N_, n, p, U, k):
    global T 
    global N
   
    T = T_
    N = N_
    for i in range(T):
        Solution.labs.append(Lab_work(p[i], n[i]))
    
    population = generate_population(U)
    count = 0
    best = max(population)
    solutions = [best]
    i = 0
    while count <= k:
        p1, p2 = choose_parents(population, count)
        c1, c2 = create_children(p1, p2)
        c1, c2 = mutate_children(c1, c2)
        c1, c2 = local_impovement(c1, c2)
        population = renew_population(population, c1, c2)
        new_best = max(population)
        if new_best > best:
            best = new_best
            count = 0
        else:
            count += 1
        i += 1
        solutions.append(best)
    Solution.labs.clear()
    return solutions


if __name__ == "__main__":
    n = []
    p = []
    T_ = 0 
    N_ = 0
    with open("src/problems.csv", 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if T_ == 0:
                T_ = int(row[0])
                N_ = int(row[1])
            else:
                n.append(int(row[0]))
                p.append(float(row[1]))
    genetic_algorithm(T_, N_, n, p, 10, 1000)
