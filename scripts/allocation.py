from agent import Agent
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def initialize_allocation_matrix(items: list[str], agents: list[Agent]):
    """Initialize allocation matrix.

    Initially, no items are allocated, matrix X is all zeros, except for last column, which displays unassigned items

    Args:
        items (list[str]): List of strings representing the items
        agents (list[Agent]): List of agents from class Agent

    Returns:
        X: len(items) x (len(agents)+1) numpy array
    """
    n = len(items)
    m = len(agents) + 1
    X = np.zeros([n, m], dtype=int)
    for i in range(n):
        X[i][m - 1] = 1
    return X


def initialize_exchange_graph(items: list[str]):
    """Generate exchange graph.

    There is one node for every item and a sink node 't' representing the pile of unnasigned items.
    Initially, there are no edges between items, and an edge from every item node to node 't'.
    Args:
        N (int): number of items

    Returns:
        nx.graph: networkx graph object
    """
    exchange_graph = nx.DiGraph()
    for item in items:
        exchange_graph.add_node(item)
    exchange_graph.add_node("t")
    for item in items:
        exchange_graph.add_edge(item, "t")
    return exchange_graph


def add_agent_to_exchange_graph(
    X: type[np.ndarray],
    G: type[nx.Graph],
    agents: list[Agent],
    items: list[str],
    agent_picked: int,
):
    """Add picked agent to the exchange graph.

    Create node representing the agent currently playing, add edges from the node to items that would increase their utility

    Args:
        X (type[np.ndarray]): allocation matrix
        G (type[nx.Graph]): exchange graph
        agents (list[Agent]): List of agents from class Agent
        items (list[str]): List of items
        agent_picked (int): index of the agent currently playing

    Returns:
        G (type[nx.Graph]): Updated exchange graph
    """
    G.add_node("s")
    bundle = [items[index] for index, i in enumerate(X[:, agent_picked]) if i != 0]
    agent = agents[agent_picked]
    for g in agent.desired_items:
        if (
            g not in bundle
            and agents[agent_picked].marginal_contribution(bundle, g) == 1
        ):
            G.add_edge("s", g)
    return G


def find_shortest_path(G: type[nx.Graph], start: str, end: str):
    """Find shortest path on exchange graph.

    Find and return shortest path from start to end nodes on graph G. Return False if there is no path

    Args:
        G (type[nx.Graph]): exchange graph
        start (str): start node
        end (str): target node

    Returns:
        list[int]: list of nodes (item indices) on the shortest path
        of False: if there is no such path
    """
    try:
        p = nx.shortest_path(G, source=start, target=end)
        return p
    except:
        return False


def update_allocation(
    X: type[np.ndarray],
    X_0_matr: type[np.ndarray],
    c_flag: int,
    agents: list[Agent],
    items: list[str],
    path_og: list[int],
    agent_picked: int,
):
    """Update allocation matrix.

    Execute the transfer path found, updating the allocation of items accordingly

    Args:
        X (type[np.ndarray]): allocation matrix
        agents (list[Agent]): List of agents from class Agent
        items (list[str]): List of items
        path_og (list[str]): shortest path, list of items
        agent_picked (int): index of the agent currently playing

    Returns:
        X (type[np.ndarray]): updated allocation matrix
        agents_involved (list[int]): indices of the agents involved in the transfer path
    """
    path = path_og.copy()
    path = path[1:-1]
    last_item = items.index(path[-1])
    agents_involved = [agent_picked]
    X[last_item, len(agents)] -= 1

    if c_flag==1:
        agent_x0 = list((X_0_matr[last_item] > 0).nonzero()[0])[0]
        X_0_matr[last_item, agent_x0] -= 1
        X_0_matr[last_item, len(agents)] = 1

    while len(path) > 0:
        last_item = items.index(path.pop(len(path) - 1))
        if len(path) > 0:
            next_to_last_item = items.index(path[-1])
            current_agent = [
                index for index, i in enumerate(X[next_to_last_item]) if i == 1
            ][0]
            agents_involved.append(current_agent)
            X[last_item, current_agent] = 1
            X[next_to_last_item, current_agent] = 0
        else:
            X[last_item, agent_picked] = 1
    return X, X_0_matr, agents_involved


def update_exchange_graph(
    X: type[np.ndarray],
    X_0_matr: type[np.ndarray],
    c_flag,
    G: type[nx.Graph],
    agents: list[Agent],
    items: list[str],
    path_og: list[int],
    agents_involved: list[int],
):
    """Update the exchange graph after the transfers made.

    Given the updated allocation, path found and list of involved agents in the transfer path, update the exchange graph

    Args:
        X (type[np.ndarray]): allocation matrix
        G (type[nx.Graph]): exchange graph
        agents (list[BaseAgent]): List of agents from class BaseAgent
        items (list[ScheduleItem]): List of items from class BaseItem
        path_og (list[int]): shortest path, list of items indices
        agents_involved (list[int]): list of the indices of the agents invovled in the transfer path

    Returns:
        G (type[nx.Graph]): updated exchange graph
    """
    path = path_og.copy()
    G.remove_edges_from(
        [edge for edge in [e for e in G.edges()] if edge[0] in path[1:-1]]
    )
    for agent_index in agents_involved:
        agent = agents[agent_index]
        bundle = [items[index] for index, i in enumerate(X[:, agent_index]) if i != 0]
        for item_1 in bundle:
            for item_2 in agent.desired_items:
                exchangeable = agent.exchange_contribution(bundle, item_1, item_2)
                if exchangeable:
                    if not G.has_edge(item_1, item_2):
                        weight = 1
                        if c_flag==1:
                            if X_0_matr[items.index(item_2), agent_index] == 1:
                                weight = 0.5
                        G.add_edge(item_1, item_2, weight=weight)
                else:
                    if G.has_edge(item_1, item_2):
                        G.remove_edge(item_1, item_2)
    return G


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
        G = add_agent_to_exchange_graph(X, G, agents, items, agent_picked)
        if plot_exchange_graph:
            nx.draw(G, with_labels=True)
            plt.show()

        path = find_shortest_path(G, "s", "t")
        G.remove_node("s")

        if path == False:
            players.remove(agent_picked)
            utility_vector[agent_picked] = float("inf")
        else:
            X, _, agents_involved = update_allocation(X, X,0, agents, items, path, agent_picked)
            G = update_exchange_graph(X, X,0, G, agents, items, path, agents_involved)
            utility_vector[agent_picked] += 1
            if plot_exchange_graph:
                nx.draw(G, with_labels=True)
                plt.show()
    return X
