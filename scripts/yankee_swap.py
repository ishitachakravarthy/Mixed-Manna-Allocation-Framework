from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *


def yankee_swap(
    agents: list[Agent],
    items: list[str],
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
    X = initialize_allocation_matrix(items, agents)
    G = initialize_exchange_graph(items)
    utility_vector = np.zeros([M])
    count = 0
    while len(players) > 0:
        print("Iteration: %d" % count, end="\r")
        count += 1
        agent_picked = np.argmin(utility_vector)
        G = add_agent_to_exchange_graph(
            X,
            G,
            agents,
            items,
            agent_picked,
            1,
        )
        if plot_exchange_graph:
            nx.draw(G, with_labels=True)
            plt.show()

        path = find_shortest_path(G, "s", "t")
        G.remove_node("s")

        if path == False:
            players.remove(agent_picked)
            utility_vector[agent_picked] = float("inf")
        else:
            X, _, agents_involved = update_allocation(
                X,
                X,
                agents,
                items,
                path,
                agent_picked,
                0,
            )
            G = update_exchange_graph(
                X,
                X,
                G,
                agents,
                items,
                path,
                agents_involved,
                0,
            )
            utility_vector[agent_picked] += 1
            if plot_exchange_graph:
                nx.draw(G, with_labels=True)
                plt.show()
    return X
