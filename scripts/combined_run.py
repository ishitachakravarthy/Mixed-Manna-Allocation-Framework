from agent import Agent
from algorithm import *


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


X_c_matr, X_0_matr, X__1_matr = mixed_manna(agents, items, c_value)
print("Final allocation:")
print(f"Xc:\n {X_c_matr}")
print(f"X0:\n {X_0_matr}")
print(f"X__1:\n {X__1_matr}")
