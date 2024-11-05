import numpy as np
from allocation import * 
items = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9"]
agents = [1, 2, 3]
c = 3

X_c_matr = initialize_allocation_matrix(items, agents)
X_0_matr = initialize_allocation_matrix(items, agents)
X__1_matr = initialize_allocation_matrix(items, agents)

# Set example allocation for testing
X_c_matr[:, 0] = [0, 0, 1, 1, 0, 1, 0, 0, 0]
X_c_matr[:, 1] = [0, 0, 0, 0, 1, 0, 0, 0, 0]
X_c_matr[:, 3] = [1, 1, 0, 0, 0, 0, 1, 1, 1]

X_0_matr[:, 0] = [1, 1, 0, 0, 0, 0, 0, 0, 0]
X_0_matr[:, 3] = [0, 0, 1, 1, 1, 1, 1, 1, 1]


def find_current_utilities(agent, X_c_matr, X_0_matr, X__1_matr):
    #  Given an agent find the utility of the agent
    value = (
        np.sum(X_c_matr[:, agent]) * c
        + np.sum(X_0_matr[:, agent]) * 0
        - np.sum(X__1_matr[:, agent])
    )
    return value


def find_max_utility_agent(agents, X_c_matr, X_0_matr, X__1_matr):
    max_agent = None
    max_value = -float("inf")
    for agent in range(len(agents)):
        value = find_current_utilities(agent, X_c_matr, X_0_matr, X__1_matr)
        if value >= max_value:
            max_value = value
            max_agent = agent
    return max_agent, max_value

def allocate_remaining_items_matr(X_c_matr, X_0_matr, X__1_matr):

    # Create a list of unallocated items
    unallocated_items_arr = X_c_matr[:, -1] & X_0_matr[:, -1] & X__1_matr[:, -1]
    unallocated_items = list((unallocated_items_arr > 0).nonzero()[0])

    # While there are unallocated items
    while unallocated_items:
        # Find the agent with maximum utility with maximum index
        max_agent, max_value = find_max_utility_agent(
            agents, X_c_matr, X_0_matr, X__1_matr
        )

        # Pick and remove an arbitrary item from the unallocated items
        item = unallocated_items.pop()

        # Assign an arbitrary unallocated item to the max utility agent
        X__1_matr[item, max_agent] = 1

        # Remove assigned item from set of unallocated items
        X__1_matr[item, -1] = 0
    return X_c_matr, X_0_matr, X__1_matr


# Print utilities of agents before allocation is done
for agent in range(len(agents)):
    value = find_current_utilities(agent, X_c_matr, X_0_matr, X__1_matr)
    print(f"Value of agent id {agent}: {value}")

X_c_matr, X_0_matr, X__1_matr = allocate_remaining_items_matr(
    X_c_matr, X_0_matr, X__1_matr
)
print("New matrices after allocation: ")
print(f"Xc: {X_c_matr}")
print(f"X0: {X_0_matr}")
print(f"X__1: {X__1_matr}")
