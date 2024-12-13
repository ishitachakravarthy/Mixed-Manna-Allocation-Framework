from agent import Agent

from allocation import *
from yankee_swap import *
from pareto_paths import *
from greedy_algorithm import *

def mixed_manna(agents, items,c_value):
    X_0_matr = yankee_swap(agents=agents, items=items)
    X_c_matr = initialize_allocation_matrix(items, agents)
    X__1_matr = initialize_allocation_matrix(items, agents)

    # print(f"Xc: {X_c_matr}")
    # print(f"X0: {X_0_matr}")
    # print(f"X__1: {X__1_matr}")
    path_updated=True
    G = initialize_exchange_graph(items)
    while path_updated:

        X_c_matr, X_0_matr, G, pareto_path = yankee_swap_c(
            agents=agents,
            items=items,
            G=G,
            X_c_matr=X_c_matr,
            X_0_matr=X_0_matr,
            c_value=c_value,
            plot_exchange_graph=False,
        )
        X_c_matr, X_0_matr, G , path_augment= path_augmentation(
        agents, items, X_c_matr, X_0_matr, G, c_value)
        print(pareto_path, path_augment)
        path_updated = pareto_path or path_augment
        print("One run done")
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
    return X_c_matr, X_0_matr, X__1_matr
