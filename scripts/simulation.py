from agent import Agent

items=['o1', 'o2', 'o3', 'o4', 'o5', 'o6']

agent1=Agent(id='1', cap=8, desired_items=items)
agent2=Agent(id='2', cap=8, desired_items=['o2', 'o3'])
agent3=Agent(id='3', cap=8, desired_items=['o2'])

agents=[agent1, agent2, agent3]

bundle =['o1','o3', 'o4']
print(f'Agent 1 valuation of {bundle}: {agent1.valuation(bundle)}')
print(f'Agent 2 valuation of {bundle}: {agent2.valuation(bundle)}')
print(f'Agent 3 valuation of {bundle}: {agent3.valuation(bundle)}')

print(f"Agent 1 marginal contribution of o2 to {bundle}: {agent1.marginal_contribution(bundle,'o1')}")
print(f"Agent 1 marginal contribution of o2 to {bundle}: {agent1.marginal_contribution(bundle,'o2')}")
print(f"Agent 1 marginal contribution of o2 to {bundle}: {agent1.marginal_contribution(bundle,'o4')}")


print(f"Agent 1 willing to exchange o1 for o2 with bundle {bundle}: {agent1.exchange_contribution(bundle,'o1','o3')}")
print(f"Agent 2 willing to exchange o3 for o2 with bundle {bundle}: {agent2.exchange_contribution(bundle,'o3','o2')}")
print(f"Agent 2 willing to exchange o3 for o2 with bundle {bundle}: {agent3.exchange_contribution(bundle,'o3','o2')}")