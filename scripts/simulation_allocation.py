import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from agent import Agent
from allocation import yankee_swap

items = ["o1", "o2", "o3", "o4", "o5", "o6"]

agent1 = Agent(id="0", cap=8, desired_items=items)
agent2 = Agent(id="1", cap=8, desired_items=["o2", "o3"])
agent3 = Agent(id="2", cap=8, desired_items=["o2"])

agents = [agent1, agent2, agent3]


X = yankee_swap(agents=agents, items=items)
print(X)
