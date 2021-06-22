import csv
from Solution_class import Solution
from Lab_work_class import Lab_work

def main(T, N, n, p):
    Solution.labs = []
    for i in range(T):
        Solution.labs.append(Lab_work(p[i], n[i]))
    L = calculate_probability_by_attempt(Solution.labs)
    A = {}
    record = Solution(T)
    for el in L.copy():
        if(el[1]>N):
            del L[el]
    solution, record = branches_method(A, L, Solution(T), record, N)
    Solution.labs.clear()
    return record

def branches_method(taken_list, not_taken_list, current_solution, record, possible_attempts):
    if current_solution.z < record.z:
        return record, record
    if len(not_taken_list) == 0 or possible_attempts == 0:
        return current_solution, current_solution

    b = not_taken_list.popitem()
    taken_list_l = taken_list.copy()
    not_taken_list_l = not_taken_list.copy()
    taken_list_l[b[0]] = b[1]
    for i in range(1, b[0][1]):
        del not_taken_list_l[(b[0][0], i)]
    
    solution_l = Solution(len(Solution.labs))
    solution_l.z = sum(taken_list_l.values())
    for el in taken_list_l:
        solution_l.x[el[0]] = el[1]
    possible_attempts_l = possible_attempts - b[0][1]

    for el in not_taken_list_l.copy():
        if el[1] > possible_attempts_l:
            del not_taken_list_l[el]
        else:
            solution_l.z += not_taken_list_l[el]
    solution_l, record = branches_method(taken_list_l,
    not_taken_list_l, solution_l, record, possible_attempts_l)


    taken_list_r = taken_list.copy()
    not_taken_list_r = not_taken_list.copy()
    solution_r = Solution(len(Solution.labs))
    solution_r.z += sum(taken_list_r.values())
    solution_r.z += sum(not_taken_list_r.values())
    possible_attempts_r = possible_attempts
    
    solution_r, record = branches_method(taken_list_r, not_taken_list_r,
    solution_r, record, possible_attempts_r)

    if solution_l.z > solution_r.z:
        return solution_l, record
    else:
        return solution_r, record

def calculate_probability_by_attempt(labs):
    L = {}
    for i in range(len(labs)):
        for j in range(1, labs[i].n+1):
            L[(i, j)] = sum(labs[i].P[:j+1])
    L_sorted = sorted(L.items(), key = lambda x: x[1])
    L.clear()
    for el in L_sorted:
        L[el[0]] = el[1]
    return L

if __name__ == "__main__":
    n = []
    p = []
    T = 0 
    N = 0
    with open("src/problems.csv", 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if T == 0:
                T = int(row[0])
                N = int(row[1])
            else:
                n.append(int(row[0]))
                p.append(float(row[1]))
    print(main(T, N, n, p))