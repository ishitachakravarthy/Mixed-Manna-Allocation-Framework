from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *
from chore_allocation import *
from agent_chore import *
import time
from greedy_algorithm import *

items = []
desired_items_2 = []
desired_items_4 = []
c=2
for i in range(10):
    items.append(str(i))
    if i%2==0:
        desired_items_2.append(str(i))
    if i%4==0:
        desired_items_4.append(str(i))

agents = []
desired_items_0 = [desired_items_2, desired_items_2]
desired_items_c = [[], desired_items_4]

agents.append(Agent(id=str(0), cap=100, desired_items=desired_items_0[0]))
agents.append(Agent(id=str(1), cap=100, desired_items=desired_items_0[1]))


X_0_matr = yankee_swap(agents=agents, items=items)


X_c_matr = initialize_allocation_matrix(items, agents)
X__1_matr = initialize_allocation_matrix(items, agents)


print(f"Xc: {X_c_matr}")
print(f"X0: {X_0_matr}")
print(f"X__1: {X__1_matr}")

agents[0] = Agent(id=str(0), cap=100, desired_items=desired_items_c[0])
agents[1] = Agent(id=str(1), cap=100, desired_items=desired_items_c[1])

X_c_matr, X_0_matr = yankee_swap_c(
    agents=agents,
    items=items,
    X_c_matr=X_c_matr,
    X_0_matr=X_0_matr,
    plot_exchange_graph=False,
)
print(f"Xc: {X_c_matr}")
print(f"X0: {X_0_matr}")
print(f"X__1: {X__1_matr}")

X_c_matr, X_0_matr, X__1_matr = allocate_remaining_items_matr(agents, c,
    X_c_matr, X_0_matr, X__1_matr
)
print(f"Xc: {X_c_matr}")
print(f"X0: {X_0_matr}")
print(f"X__1: {X__1_matr}")
print(desired_items_2)
print(desired_items_4)
