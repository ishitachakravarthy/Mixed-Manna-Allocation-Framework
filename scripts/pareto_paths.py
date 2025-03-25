from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *


def yankee_swap_c(
    agents: list[Agent],
    items: list[str],
    G,
    X_c_matr: type[np.ndarray],
    X_0_matr: type[np.ndarray],
    c_value: int,
    plot_exchange_graph: bool = False,
):
    """Pareto improving paths allocation algorithm with updates to allocate c and 0 valued items

    Args:
        agents (list[BaseAgent]): List of agents from class Agent
        items (list[ScheduleItem]): List of items
        X_c_matr (type[np.ndarray]): allocation matrix of c valued items
        X_0_matr (type[np.ndarray]): allocation matrix of 0 valued items
        c_value (int): Value of c for goods
        plot_exchange_graph (bool, optional): Defaults to False. Change to True to display exchange graph plot after every modification to it.

    Returns:
        X_c_matr (type[np.ndarray]): allocation matrix of c valued items
        X_0_matr (type[np.ndarray]): allocation matrix of 0 valued items
    """
    N = len(items)
    M = len(agents)
    players = list(range(M))
    utility_vector = np.zeros([M])
    count = 0
    update=False
    while len(players) > 0:
        print("Iteration: %d" % count, end="\r")
        count += 1
        # Use players[0] for running 2B and 2C
        agent_picked = players[0]
        # agent_picked = np.argmin(utility_vector)

        G = add_agent_to_exchange_graph(
            X_c_matr,
            G,
            agents,
            items,
            agent_picked,
            c_value,
        )
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
            update=True
            X_c_matr, X_0_matr, agents_involved = update_allocation(
                X_c_matr,
                X_0_matr,
                agents,
                items,
                path,
                agent_picked,
                1,
            )
            G = update_exchange_graph(
                X_c_matr,
                X_0_matr,
                G,
                agents,
                items,
                path,
                agents_involved,
                1,
            )
            utility_vector[agent_picked] += 1
            if plot_exchange_graph:
                pos = nx.spring_layout(G, seed=7)
                nx.draw(G, pos, with_labels=True)
                edge_labels = nx.get_edge_attributes(G, "weight")
                nx.draw_networkx_edge_labels(G, pos, edge_labels)
                plt.show()
    return X_c_matr, X_0_matr, G, update
