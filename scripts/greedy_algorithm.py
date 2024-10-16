items = ['o1','o2','o3','o4','o5','o6','o7','o8','o9']
agents = [1,2,3]
c=2

X_c={
    0:set(['o1', 'o2',  'o7', 'o8', 'o9']),
    1:set(['o3', 'o4', 'o6']),
    2:set(['o5']),
    3:set()
}
X_0={
    0:set(['o3','o4' 'o5', 'o6', 'o7', 'o8', 'o9']),
    1:set(['o1', 'o2']),
    2:set(),
    3:set([])
}
X__1={
    0:set(['o7', 'o8', 'o9']),
    1:set(),
    2:set(),
    3:set()
}

# Print utilities of agents after before allocation is done
for agent in agents:
        value= 0*len(X_0[agent])+(c*len(X_c[agent]) )-len(X__1[agent])
        print(f"Agent {agent}: {value}")

def allocate_remaining_items(X_c, X_0, X__1):
    # While there is an element in the set intersection
    while set(X_c[0]) & set(X_0[0]) & set(X__1[0]) :

        # Find the agent with maximum utility with maximum index
        max_agent = None
        max_value = -float('inf')
        for agent in agents:
            value= 0*len(X_0[agent])+(c*len(X_c[agent]) )-len(X__1[agent])
            if value >= max_value:
                max_value = value
                max_agent = agent

        # Pick an arbitrary item from the set intersection
        unallocated_items= set(X_c[0]) & set(X_0[0]) & set(X__1[0])
        item = unallocated_items.pop()

        # Assign an arbitrary unallocated item to the max utility agent
        X__1[max_agent].add(item)

        # Remove assigned item from set of unallocated items
        X__1[0].remove(item)
    return X_c, X_0, X__1



X_c, X_0, X__1= allocate_remaining_items(X_c, X_0, X__1)

print(f"Xc: {X_c}")
print(f"X0: {X_0}")
print(f"X__1: {X__1}")

# Print utilities of agents after all allocation is done
for agent in range(1, len(agents)+1):
        value= 0*len(X_0[agent])+(c*len(X_c[agent]) )-len(X__1[agent])
        print(f"Agent {agent}: {value}")


