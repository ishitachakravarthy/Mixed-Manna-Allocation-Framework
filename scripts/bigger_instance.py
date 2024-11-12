from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *
from chore_allocation import *
from agent_chore import *
import time 

items = []

for i in range(500):
    items.append(str(i))

agents=[]

for i in range(50):
    agents.append(Agent(id=str(i), cap=100, desired_items=items))


X_c_matr = initialize_allocation_matrix(items, agents)
X_0_matr = initialize_allocation_matrix(items, agents)
X__1_matr = initialize_allocation_matrix(items, agents)

start_time=time.time()
X_c_matr, X_0_matr = yankee_swap_c(
    agents=agents,
    items=items,
    X_c_matr=X_c_matr,
    X_0_matr=X_0_matr,
    plot_exchange_graph=False,
)
endtime=time.time()
print(endtime-start_time)

np.savetxt("tests/x_c.txt", X_c_matr)
np.savetxt("tests/x_0.txt", X_0_matr)
