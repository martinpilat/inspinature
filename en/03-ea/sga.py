from os import wait
import random
import copy

DIM = 25
POP_SIZE = 50
MAX_GEN = 500
CROSS_P = 0.8
MUT_P = 0.2
FLIP_P = 1/DIM

PATTERN = [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1]

def random_individual(dim):
    return [random.randint(0,1) for _ in range(dim)]

def random_population(pop_size, dim):
    return [random_individual(dim) for _ in range(pop_size)]

def one_max_fitness(ind):
    # return sum(1 if i == p else 0 for (i, p) in zip(ind, PATTERN))
    return sum(ind)

def select(pop, how_many, fits):
    sel = random.choices(pop, weights=fits, k=how_many)
    return copy.deepcopy(sel)

def crossover(pool, cross_p):
    dim = len(pool[0])
    off = []
    for p1, p2 in zip(pool[::2], pool[1::2]):
        if random.random() < cross_p:
            point = random.randrange(0, dim)
            o1 = p1[:point] + p2[point:]
            o2 = p2[:point] + p1[point:]
        else:
            o1, o2 = p1, p2
        off += [o1, o2]
    return off

def mutation(pool, mut_p, flip_p):
    off = []
    for p in pool:
        if random.random() < mut_p:
            o = []
            for v in p:
                if random.random() < flip_p:
                    o.append(1-v)
                else:
                    o.append(v)
            off.append(o)
        else:
            off.append(p)
    return off

def evolution(pop, dim, fitness, 
              max_gen, cross_p, mut_p, flip_p):
    pop_size = len(pop)
    log = []
    for g in range(max_gen):
        # logging
        fits = [fitness(ind) for ind in pop]
        log.append(1/max(fits))
        
        # elitism
        best = max(pop, key=fitness)
        
        mating_pool = select(pop, pop_size, fits)
        pre_off = crossover(mating_pool, cross_p)
        off = mutation(pre_off, mut_p, flip_p)
        
        off[0] = copy.deepcopy(best) # elitism
        pop = off
    return pop, log

from pprint import pprint

SET = [random.randint(0, 500) for _ in range(100)]
DIM = len(SET)
print(sum(SET))
K = sum(SET)//3

def subset_fitness(ind):
    s = sum(i*s for (i, s) in zip(ind, SET))
    if K == s:
        return 2
    diff = 1/abs(K-s)
    return diff

pop = random_population(POP_SIZE, DIM)
print('After init')
pprint(pop)
res, log = evolution(pop, DIM, subset_fitness, MAX_GEN, CROSS_P, MUT_P, FLIP_P)
print('After evolution')
pprint(res)
print(log)

import matplotlib.pyplot as plt 

logs = []
for _ in range(10):
    pop = random_population(POP_SIZE, DIM)
    res, log = evolution(pop, DIM, subset_fitness, MAX_GEN, CROSS_P, MUT_P, FLIP_P)
    logs.append(log)

import numpy as np

logs = np.array(logs)

plt.plot(logs.mean(axis=0))
plt.fill_between(list(range(len(logs[0]))), np.percentile(logs, axis=0, q=25), np.percentile(logs, axis=0, q=75), alpha=0.5)
plt.yscale('log')
plt.show()

# print('Before crossover')
# pprint(pop)
# print('After crossover')
# cross = crossover(pop, 1.0)
# pprint(cross)
# print('After mutation')
# mut = mutation(cross, 1.0, 0.5)
# pprint(mut)

