from agent import Agent

from allocation import *
from yankee_swap import *
from pareto_paths import *
from greedy_algorithm import *

items = []
desired_items_2 = []
desired_items_4 = []
c_value = 2
for i in range(6):
    items.append(str(i))
    if i % 4 == 0:
        desired_items_4.append(str(i))
    if i % 2 == 0:
        desired_items_2.append(str(i))
# desired_items_0 = [desired_items_2, desired_items_2]
# desired_items_c = [desired_items_4, []]
agents = []
desired_items_0 = [[
    "0",
    "2",
    "3",
    "4",
    "5",
], [
    "0",
    "3",
    "4",
]]
desired_items_c = [
    desired_items_4,["0","4"]
]
agents.append(
    Agent(
        id=str(0),
        cap=100,
        desired_items=desired_items_0[0],
        desired_items_c=desired_items_c[0],
        c_value=c_value,
    )
)
agents.append(
    Agent(
        id=str(1),
        cap=100,
        desired_items=desired_items_0[1],
        desired_items_c=desired_items_c[1],
        c_value=c_value,
    )
)

print(f"Agent 1: ")
print(f"desired_items_0:{desired_items_0[0]} ")
print(f"desired_items_c:{desired_items_c[0]} ")
print(f"Agent 2: ")
print(f"desired_items_0:{desired_items_0[1]} ")
print(f"desired_items_c:{desired_items_c[1]} ")

X_0_matr = yankee_swap(agents=agents, items=items)


X_c_matr = initialize_allocation_matrix(items, agents)
X__1_matr = initialize_allocation_matrix(items, agents)


# print(f"Xc: {X_c_matr}")
# print(f"X0: {X_0_matr}")
# print(f"X__1: {X__1_matr}")

# agents[0] = Agent(id=str(0), cap=100, desired_items=desired_items_c[0])
# agents[1] = Agent(id=str(1), cap=100, desired_items=desired_items_c[1])

X_c_matr, X_0_matr = yankee_swap_c(
    agents=agents,
    items=items,
    X_c_matr=X_c_matr,
    X_0_matr=X_0_matr,
    c_value=c_value,
    plot_exchange_graph=False,
)
# print(f"Xc: {X_c_matr}")
# print(f"X0: {X_0_matr}")
# print(f"X__1: {X__1_matr}")

X_c_matr, X_0_matr, X__1_matr = allocate_remaining_items_matr(
    agents, c_value, X_c_matr, X_0_matr, X__1_matr
)
print("Final allocation:")
print(f"Xc:\n {X_c_matr}")
print(f"X0:\n {X_0_matr}")
print(f"X__1:\n {X__1_matr}")
