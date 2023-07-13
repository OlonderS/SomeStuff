import math
import openpyxl
import random

result = math.inf
order = []

def get_indexes(n_of_cities):
    idx = [x for x in range(1,n_of_cities+1)]
    random.shuffle(idx)
    return idx

def get_distances(file, idx):
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    ll = []
    for i in range(1, len(idx)):
        for j in range(i+1,len(idx)+1):
            ll.append((i, j))
    dic = {}
    for el in ll:
        dic[el] = sheet.cell(row=el[0]+1, column=el[1]+1).value
    
    return dic
    
    
def calculate_sum(idx, dic):
    sum = 0
    for i in range(1, len(idx)-1):
        if idx[i]<idx[i+1]:
            sum+=dic.get((idx[i], idx[i+1]))
        else:
            sum+=dic.get((idx[i+1], idx[i]))
    if idx[0]<idx[-1]:
        sum+=dic.get((idx[0], idx[-1]))
    else:
        sum+=dic.get((idx[-1], idx[0]))
    return sum

# def swap_random(idx):
#     l = range(1, 1+len(idx))
#     i, j = random.sample(l, 2)
#     tmp1 = idx.index(i)
#     tmp2 = idx.index(j)
#     idx[tmp1], idx[tmp2] = idx[tmp2], idx[tmp1]
#     return idx
    
# def change_index(idx):
#     l = range(len(idx))
#     i, j = random.sample(l, 2)
#     tmp = idx[i-1]
#     del idx[i-1]
#     idx.insert(j-1, tmp)
#     return idx, i, j
    
# def swap_elements(idx):
#     l = range(len(idx))
#     i, j = random.sample(l, 2)
#     tmp = idx[i:j]
#     tmp = tmp[::-1]
#     idx = idx[:i] + tmp + idx[j:]
#     return idx, i, j

def swap_random(idx, i, j):
    tmp1 = idx.index(i)
    tmp2 = idx.index(j)
    idx[tmp1], idx[tmp2] = idx[tmp2], idx[tmp1]
    return idx
    
def change_index(idx, i, j):
    tmp = idx[i-1]
    del idx[i-1]
    idx.insert(j-1, tmp)
    return idx, i, j
    
def swap_elements(idx):
    l = range(len(idx))
    i, j = random.sample(l, 2)
    tmp = idx[i:j]
    tmp = tmp[::-1]
    idx = idx[:i] + tmp + idx[j:]
    return idx, i, j
    
def best_move_swap(idx, dic, tabu_list):
    best_value = math.inf
    ll=[]
    for i in range(1, len(idx)):
        for j in range(i+1,len(idx)+1):
            ll.append((i, j))

    best_pair = ()
    for el in ll:
        if el not in tabu_list.keys():
            tmp = swap_random(idx, el[0], el[1])
            tmp_val = calculate_sum(tmp, dic)
            if tmp_val<best_value:
                best_value = tmp_val
                best_pair = (el[0], el[1])

    return best_pair, best_value
    
def tabu_move(idx, dic, length):
    global result
    global order
    tabu_moves = {}
    copy = idx[:]
    pair, value = best_move_swap(copy, dic, tabu_moves)
    copy= swap_random(copy, pair[0], pair[1])
    if value < result:
        result = value
        order = copy
    for v in tabu_moves.values():
        v-=1
    for k,v in tabu_moves.items():
        if v<=0:
            del tabu_moves[k]
    tabu_moves[(pair[0], pair[1])] = length
    
    
file = 'Dane_TSP_48.xlsx'
n = 48
indexes = get_indexes(n)
distances = get_distances(file, indexes)
min = calculate_sum(indexes, distances)
d = {}
for i in range(100000):
    indexes = get_indexes(n)
    sum = calculate_sum(indexes, distances)
    if sum<min:
        min=sum
        d[i]=min
    
    else:
        print(i)
print(d)
print(1)




def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, iters, size, n_opt=1):
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution
    while count <= iters:
        neighborhood = find_neighborhood(solution, dict_of_neighbours, n_opt=n_opt)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1
        found = False
        while found is False:
            i = 0
            first_exchange_node, second_exchange_node = [], []
            n_opt_counter = 0
            while i < len(best_solution):
                if best_solution[i] != solution[i]:
                    first_exchange_node.append(best_solution[i])
                    second_exchange_node.append(solution[i])
                    n_opt_counter += 1
                    if n_opt_counter == n_opt:
                        break
                i = i + 1

            exchange = first_exchange_node + second_exchange_node
            if first_exchange_node + second_exchange_node not in tabu_list and second_exchange_node + first_exchange_node not in tabu_list:
                tabu_list.append(exchange)
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            elif index_of_best_solution < len(neighborhood):
                best_solution = neighborhood[index_of_best_solution]
                index_of_best_solution = index_of_best_solution + 1

        while len(tabu_list) > size:
            tabu_list.pop(0)

        count = count + 1
    best_solution_ever.pop(-1)
    return best_solution_ever, best_cost


