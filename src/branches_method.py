import csv
from Solution_class import Solution
from Lab_work_class import Lab_work


def solution_matrixes(T, n, p):
    for i in range(T):
        Solution.labs.append(Lab_work(p[i], n[i]))
    solution = Solution(T)
    return solution


# матриця імовірностей здачі i-тої ЛР з j-ї спроби
def prob_matrix(T, n, p):
    pr = []
    for i in range(T):
        pr.append([])
        for j in range(max(n)):
            if j + 1 <= n[i]:
                pr[i].append(1 - (1 - p[i]) ** (j + 1))
            else:
                pr[i].append(0)
    return pr


# розрахувати сумарні ймовірності здачі від спроби
def sumprob_list(T, n, pr):
    sumpr = []
    sum = 0
    for i in range(T):
        for j in range(n[i]):
            sum += pr[i][j]
            sumpr.append({"lab": i + 1, "attempt": j + 1, "probability": sum})
        sum = 0

    sumpr.sort(key=lambda x: x['probability'], reverse=True)

    return sumpr


def get_sum_of_maximums(prob_list, quantity):
    sum = 0

    for i in range(quantity):
        curr_lab = list(filter(lambda x: x['lab'] == i + 1, prob_list))
        if len(curr_lab) != 0:
            max_prob = max(curr_lab, key=lambda x: x['probability'])
            sum += max_prob["probability"]
    return sum


def get_sum_of_probs(prob_list):
    sum = 0
    for i in range(len(prob_list)):
        sum += prob_list[i]["probability"]
    return sum


def branches_method(sum_prob_list, attempt_quantity, labs_quantity, included_probs_list=[], record=0, side='center',
                    step=1):
    print('-----------------------------------------------------------------------------------------------------------')
    print('side:', side, '| step:', step)
    print('A: ', included_probs_list)
    print('B: ', sum_prob_list)
    print('U:', attempt_quantity)

    if attempt_quantity == 0 or len(sum_prob_list) == 0:
        print('--returning😎', get_sum_of_probs(included_probs_list))

        return get_sum_of_probs(included_probs_list)

    else:

        max_prob = sum_prob_list.pop(0)

        # left_side
        left_attempt_quantity = attempt_quantity - max_prob['attempt']
        left_sum_prob_list = list(
            filter(lambda prob: prob['lab'] != max_prob['lab'] and prob['attempt'] <= left_attempt_quantity,
                   sum_prob_list))
        left_included_probs_list = [*included_probs_list, max_prob]

        left_result = get_sum_of_probs(left_included_probs_list) + get_sum_of_maximums(left_sum_prob_list,
                                                                                       labs_quantity - 1)

        print('left: ', left_result)

        # right side
        right_attempt_quantity = attempt_quantity
        right_sum_prob_list = [*sum_prob_list]
        right_included_probs_list = [*included_probs_list]
        right_result = get_sum_of_probs(right_included_probs_list) + get_sum_of_maximums(right_sum_prob_list,
                                                                                         labs_quantity)
        print('right: ', right_result)

        if right_result < record:
            return branches_method(left_sum_prob_list, left_attempt_quantity, labs_quantity - 1,
                                   left_included_probs_list, left_result, 'left', step + 1)
        else:
            left = branches_method(left_sum_prob_list, left_attempt_quantity, labs_quantity - 1,
                                   left_included_probs_list, left_result, 'left', step + 1)
            right = branches_method(right_sum_prob_list, right_attempt_quantity, labs_quantity,
                                    right_included_probs_list, right_result, 'right', step + 1)

            if left > right:
                return left
            else:
                return right


if __name__ == "__main__":
    T = 0
    N = 0
    n = []
    p = []
    with open("problems.csv", 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if T == 0:
                T = int(row[0])
                N = int(row[1])
            else:
                n.append(int(row[0]))
                p.append(float(row[1]))

    all_prob_matrix = prob_matrix(T, n, p)
    sum_prob_list = sumprob_list(T, n, all_prob_matrix)
    result = branches_method(sum_prob_list, N, T)
    print(result)
