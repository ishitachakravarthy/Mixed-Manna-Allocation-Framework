from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *

from agent_chore import *

def get_weight(X_c_matr, X_0_matr, items, item_1, item_2):

    item1_x0 = list((X_0_matr[items.index(item_1)] > 0).nonzero()[0])[0]
    item1_xc = list((X_c_matr[items.index(item_1)] > 0).nonzero()[0])[0]

    item2_x0 = list((X_0_matr[items.index(item_2)] > 0).nonzero()[0])[0]
    item2_xc = list((X_c_matr[items.index(item_2)] > 0).nonzero()[0])[0]

    f1=0
    f2=0
    if item1_x0<(len(X_0_matr[0]))-1:
        print(f"item {item_1} with agent in x0 {item1_x0}")
        i1_o=item1_x0
        i1_val='0'
        f1+=1

    if item1_xc < (len(X_0_matr[0])) - 1:
        print(f"item  {item_1}  with agent in xc {item1_xc}")
        i1_o=item1_xc
        i1_val='c'
        f1+=1

    if item2_x0 < (len(X_0_matr[0])) - 1:
        print(f"item  {item_2}  with agent in x0 {item2_x0}")
        i2_o=item2_x0
        i2_val='0'
        f2+=1

    if item2_xc < (len(X_0_matr[0])) - 1:
        print(f"item  {item_2}  with agent in xc {item2_xc}")
        i2_o=item2_xc
        i2_val='c'
        f2+=1

    # If item1 or item2 are in both x_0 and x_c bundles
    if f1>1 or f2>1:
        print("Wrong allocation")
        return 0

    # If item2 is unallocated
    if not(f2) :
        return 1

    # If owner of object 1 and 2 are the same, and object 1 has a value of c and object 2 has a value of 0
    if i1_o == i2_o and (i1_val=='c' and i2_val=='0'):
        return 0.5
    else:
        return 1


def update_allocation_chore(X_c_matr, X_0_matr, agents, items, path_og, agent_picked):
    # changes made- update X_c instead of X, and adding a change for matrix X_0
    path = path_og.copy()
    path = path[1:-1]
    last_item = items.index(path[-1])
    agents_involved = [agent_picked]
    X_c_matr[last_item, len(agents)] -= 1

    # Additionally change matrix X_0 
    agent_x0 = list((X_0_matr[last_item] > 0).nonzero()[0])[0]
    X_0_matr[last_item, agent_x0] -= 1
    X_0_matr[last_item, len(agents)] = 1

    while len(path) > 0:
        last_item = items.index(path.pop(len(path) - 1))
        if len(path) > 0:
            next_to_last_item = items.index(path[-1])
            current_agent = [
                index for index, i in enumerate(X_c_matr[next_to_last_item]) if i == 1
            ][0]
            agents_involved.append(current_agent)
            X_c_matr[last_item, current_agent] = 1
            X_c_matr[next_to_last_item, current_agent] = 0
        else:
            X_c_matr[last_item, agent_picked] = 1
    return X_c_matr, X_0_matr, agents_involved

    return


def update_exchange_graph_weighted(
    X_c_matr: type[np.ndarray],
    X_0_matr: type[np.ndarray],
    G: type[nx.Graph],
    agents: list[Agent],
    items: list[str],
    path_og: list[int],
    agents_involved: list[int],
):
    # ONLY WEIGHTS ADDED
    path = path_og.copy()
    G.remove_edges_from(
        [edge for edge in [e for e in G.edges()] if edge[0] in path[1:-1]]
    )
    for agent_index in agents_involved:
        agent = agents[agent_index]
        bundle = [
            items[index] for index, i in enumerate(X_c_matr[:, agent_index]) if i != 0
        ]
        for item_1 in bundle:
            for item_2 in agent.desired_items:
                exchangeable = agent.exchange_contribution(bundle, item_1, item_2)
                if exchangeable:
                    if not G.has_edge(item_1, item_2):
                        # ONLY CHANGE MADE
                        weight = get_weight(
                            X_c_matr, X_0_matr,items, item_1, item_2
                        )
                        G.add_edge(item_1, item_2, weight=weight)
                else:
                    if G.has_edge(item_1, item_2):
                        G.remove_edge(item_1, item_2)
    return G
