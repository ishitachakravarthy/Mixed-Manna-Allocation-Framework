from agent import Agent

items=['o1', 'o2', 'o3', 'o4', 'o5', 'o6']

agent1=Agent(id='1', cap=8, desired_items=items)
agent2=Agent(id='2', cap=8, desired_items=['o2', 'o3'])
agent3=Agent(id='3', cap=8, desired_items=['o2'])

print(agent3.valuation(['o1','o3']))