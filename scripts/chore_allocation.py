from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from allocation import *

from agent_chore import  *

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
        print(f"x_c \n {X_c_matr}")
        print(f"x_0 \n {X_0_matr}")

        count += 1
        agent_picked = np.argmin(utility_vector)
        G = add_agent_to_exchange_graph(X_c_matr, G, agents, items, agent_picked)
        if plot_exchange_graph:
            pos = nx.spring_layout(G, seed=7)
            nx.draw(G,pos, with_labels=True)
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels)
            plt.show()

        path = find_shortest_path(G, "s", "t")
        G.remove_node("s")
        if path == False:
            players.remove(agent_picked)
            utility_vector[agent_picked] = float("inf")
        else:
            X_c_matr, X_0_matr, agents_involved = update_allocation_chore(
                X_c_matr, X_0_matr, agents, items, path, agent_picked
            )
            G = update_exchange_graph_weighted(
                X_c_matr, X_0_matr, G, agents, items, path, agents_involved
            )
            utility_vector[agent_picked] += 1
            if plot_exchange_graph:
                pos = nx.spring_layout(G, seed=7)
                nx.draw(G,pos, with_labels=True)
                edge_labels = nx.get_edge_attributes(G, "weight")
                nx.draw_networkx_edge_labels(G, pos, edge_labels)
                plt.show()
    return X_c_matr, X_0_matr


items = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9"]

agent1 = Agent(id="0", cap=8, desired_items=["o2", "o9"])
agent2 = Agent(id="1", cap=8, desired_items=["o1", "o3"])
agent3 = Agent(id="2", cap=8, desired_items=["o2"])

agents = [agent1, agent2, agent3]

X_c_matr = initialize_allocation_matrix(items, agents)
X_0_matr = initialize_allocation_matrix(items, agents)
X__1_matr = initialize_allocation_matrix(items, agents)

# Set example allocation for testing
X_0_matr[:, 0] = [1, 1, 0, 0, 0, 0, 0, 0, 1]
X_0_matr[:, 1] = [0, 0, 1, 1, 0, 0, 0, 0, 0]
X_0_matr[:, 2] = [0, 0, 0, 0, 1, 1, 1, 1, 0]
X_0_matr[:, 3] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

X = yankee_swap_c(
    agents=agents, items=items, X_c_matr=X_c_matr, X_0_matr=X_0_matr,plot_exchange_graph=True
)
