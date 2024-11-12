from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *

from agent_chore import *


def yankee_swap_c(
    agents: list[Agent],
    items: list[str],
    X_c_matr,
    X_0_matr,
    plot_exchange_graph: bool = False,
):
    """General Yankee swap allocation algorithm.

    Args:
        agents (list[BaseAgent]): List of agents from class Agent
        items (list[ScheduleItem]): List of items
        plot_exchange_graph (bool, optional): Defaults to False. Change to True to display exchange graph plot after every modification to it.

    Returns:
        X (type[np.ndarray]): allocation matrix
    """
    N = len(items)
    M = len(agents)
    players = list(range(M))
    G = initialize_exchange_graph(items)
    utility_vector = np.zeros([M])
    count = 0
    while len(players) > 0:
        print("Iteration: %d" % count, end="\r")
        count += 1
        agent_picked = np.argmin(utility_vector)
        G = add_agent_to_exchange_graph(X_c_matr, 2, G, agents, items, agent_picked)
        if plot_exchange_graph:
            pos = nx.spring_layout(G, seed=7)
            nx.draw(G, pos, with_labels=True)
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels)
            plt.show()

        path = find_shortest_path(G, "s", "t")
        G.remove_node("s")
        if path == False:
            players.remove(agent_picked)
            utility_vector[agent_picked] = float("inf")
        else:
            X_c_matr, X_0_matr, agents_involved = update_allocation(
                X_c_matr, X_0_matr, 1, agents, items, path, agent_picked
            )
            G = update_exchange_graph(
                X_c_matr, X_0_matr, 1, G, agents, items, path, agents_involved
            )
            utility_vector[agent_picked] += 1
            if plot_exchange_graph:
                pos = nx.spring_layout(G, seed=7)
                nx.draw(G, pos, with_labels=True)
                edge_labels = nx.get_edge_attributes(G, "weight")
                nx.draw_networkx_edge_labels(G, pos, edge_labels)
                plt.show()
    return X_c_matr, X_0_matr
