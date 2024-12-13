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
    c_value: int,
):
    """Add picked agent to the exchange graph.

    Create node representing the agent currently playing, add edges from the node to items that would increase their utility

    Args:
        X (type[np.ndarray]): allocation matrix
        G (type[nx.Graph]): exchange graph
        agents (list[Agent]): List of agents from class Agent
        items (list[str]): List of items
        agent_picked (int): index of the agent currently playing
        c_value (int): Value of c for goods

    Returns:
        G (type[nx.Graph]): Updated exchange graph
    """
    G.add_node("s")
    bundle = [items[index] for index, i in enumerate(X[:, agent_picked]) if i != 0]
    agent = agents[agent_picked]
    for g in items:
        if (
            g not in bundle
            and agents[agent_picked].marginal_contribution(bundle, g) == c_value
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
    agents: list[Agent],
    items: list[str],
    path_og: list[int],
    agent_picked: int,
    c_flag: int,
):
    """Update allocation matrix.

    Execute the transfer path found, updating the allocation of items accordingly

    Args:
        X (type[np.ndarray]): allocation matrix
        agents (list[Agent]): List of agents from class Agent
        items (list[str]): List of items
        path_og (list[str]): shortest path, list of items
        agent_picked (int): index of the agent currently playing
        c_value (int): Value of c for goods

    Returns:
        X (type[np.ndarray]): updated allocation matrix
        X_0_matr (type[np.ndarray]): updated allocation matrix of 0 valued items
        agents_involved (list[int]): indices of the agents involved in the transfer path
    """
    path = path_og.copy()
    path = path[1:-1]
    last_item = items.index(path[-1])
    agents_involved = [agent_picked]
    X[last_item, len(agents)] -= 1

    if c_flag == 1:
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
    G: type[nx.Graph],
    agents: list[Agent],
    items: list[str],
    path_og: list[int],
    agents_involved: list[int],
    c_flag: int,
):
    """Update the exchange graph after the transfers made.

    Given the updated allocation, path found and list of involved agents in the transfer path, update the exchange graph

    Args:
        X (type[np.ndarray]): allocation matrix
        X_0_matr (type[np.ndarray]): allocation matrix of 0 valued items
        G (type[nx.Graph]): exchange graph
        agents (list[BaseAgent]): List of agents from class BaseAgent
        items (list[ScheduleItem]): List of items from class BaseItem
        path_og (list[int]): shortest path, list of items indices
        agents_involved (list[int]): list of the indices of the agents invovled in the transfer path
        c_value (int): Value of c for goods

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
            for item_2 in items:
                exchangeable = agent.exchange_contribution(bundle, item_1, item_2)
                if exchangeable:
                    if not G.has_edge(item_1, item_2):
                        weight = 1
                        if c_flag == 1:
                            if X_0_matr[items.index(item_2), agent_index] == 1:
                                weight = 0.5
                        G.add_edge(item_1, item_2, weight=weight)
                else:
                    if G.has_edge(item_1, item_2):
                        G.remove_edge(item_1, item_2)
    return G


def update_path(agents, items, items_wanted, X_c_matr, X_0_matr, G, i,agent_idx):
    # Add new sync node
    X_c_col = X_c_matr[:,agent_idx]
    X_c_col_flat = X_c_col.flatten()
    items_pos = np.where(X_c_col_flat == 1)[0]

    G.add_node("x")
    for item in items_pos:
        G.add_edge(items[item], "x")

    G.add_node("a")
    for item in items_wanted:
        G.add_edge("a", item)

    path = find_shortest_path(G, "a", "x")

    if True:
        pos = nx.spring_layout(G, seed=7)
        nx.draw(G, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.show()
    # Update exchange graph
    if path == False:
        G.remove_node("a")
        G.remove_node("x")
        return X_c_matr, X_0_matr, G,False
    else:
        print(X_c_matr,X_0_matr)
        X_c_matr, X_0_matr, agents_involved = update_allocation_swap(
            X_c_matr,
            X_0_matr,
            agents,
            items,
            path,
            i,
            agent_idx
        )
        print(X_c_matr, X_0_matr, agents_involved)
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
        G.remove_node("a")
        G.remove_node("x")
        return X_c_matr, X_0_matr, G,True

    return X_c_matr, X_0_matr, G


def path_augmentation(agents, items, X_c_matr, X_0_matr, G,c_value):
    if True:
        pos = nx.spring_layout(G, seed=7)
        nx.draw(G, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.show()
    valuations_c = 2 * np.sum(X_c_matr, axis=0)[:-1]
    update=False
    for i in range(len(agents)):
        # find bundle of items wanted
        items_wanted = set()
        agent = agents[i]
        bundle = [items[index] for index, i in enumerate(X_c_matr[:, i]) if i != 0]
        for g in items:
            if (
                g not in bundle
                and agents[i].marginal_contribution(bundle, g) == c_value
            ):
                items_wanted.add(g)
        # print(i, X_c_matr, items_wanted)
        # print(valuations_c)
        for item in items_wanted:
            item_idx = items.index(item)
            agent_with_item_arr = X_c_matr[item_idx][:-1]
            agent_idx = np.where(agent_with_item_arr == 1)[0][0]
            # print(i, agent_idx)
            if (
                valuations_c[agent_idx] > valuations_c[i]+1
                or (valuations_c[agent_idx] + 1 == valuations_c[i] and i<agent_idx) 
            ):
                # Run exchange path
                print("path update")
                X_c_matr, X_0_matr, G,flag = update_path(
                     agents, items, items_wanted, X_c_matr, X_0_matr, G, i, agent_idx
                )
                update=True
                if flag==True:
                    return X_c_matr, X_0_matr, G, update

    return X_c_matr, X_0_matr, G, update


def update_allocation_swap(
    X: type[np.ndarray],
    X_0_matr: type[np.ndarray],
    agents: list[Agent],
    items: list[str],
    path_og: list[int],
    agent_picked: int,
    agent_idx
):
    """Update allocation matrix.

    Execute the transfer path found, updating the allocation of items accordingly

    Args:
        X (type[np.ndarray]): allocation matrix
        agents (list[Agent]): List of agents from class Agent
        items (list[str]): List of items
        path_og (list[str]): shortest path, list of items
        agent_picked (int): index of the agent currently playing
        c_value (int): Value of c for goods

    Returns:
        X (type[np.ndarray]): updated allocation matrix
        X_0_matr (type[np.ndarray]): updated allocation matrix of 0 valued items
        agents_involved (list[int]): indices of the agents involved in the transfer path
    """
    path = path_og.copy()
    path = path[1:-1]
    last_item = items.index(path[-1])
    agents_involved = [agent_picked]
    X[last_item, agent_idx] -= 1

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
