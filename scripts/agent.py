class Agent:

    def __init__(self, id, desired_items, desired_items_c, cap, c_value):
        """
        Object Agent has three parameters:
        - id: Agent id (not really necessary or used at the moment, might be useful when assigning priority for example)
        - desired classes: list of item objects (from class Item) that the Agent values. If on this list, item gives
                          Agent a utility of 1, if not on the list, utility of 0.
        - cap: maximum amount of items the agent can have
        """
        self.id = id
        self.desired_items = desired_items
        self.desired_items_c = desired_items_c
        self.cap = cap
        self.c_value = c_value

    def valuation(self, bundle):
        """
        Compute the utility the agent gets from a particular bundle of items

        @param bundle: list of items (from class Item)
        @return: utility given to the agent by that bundle (int)
        """
        # T=bundle.copy()
        # # x=[*range(len(bundle))]
        # # x.reverse()
        # for g in bundle:
        #     if items[g].item_id not in self.desired_items:
        #         T.remove(g)
        slots = set()
        slots_c = set()
        for item in bundle:
            if item in self.desired_items_c:
                slots_c.add(item)
            elif item in self.desired_items:
                slots.add(item)
        return min(len(slots) +(self.c_value * len(slots_c)), self.cap)

    def marginal_contribution(self, bundle, item):
        """
        Compute the marginal utility the agent gets form adding a particular item to a particular bundle of items

        @param bundle: list of items (from class Item)
        @param item: marginal item (from class Item)
        @return: marginal utility obtained by adding item to bundle (either 0, 1 or c).
        """

        T = bundle.copy()
        current_val = self.valuation(T)
        T.append(item)
        new_val = self.valuation(T)
        return new_val - current_val

    def exchange_contribution(self, bundle, og_item, new_item):
        """
        Determine whether the agent can exchange original_item for new_item and keep the same utility

        @param bundle: list of items (from class Item)
        @param og_item: original item in the bundle (from class Item)
        @param new_item: item we might exchange the og item for (from class Item)
        @return: True if utility obtained by exchanging item is the same or more, False otherwise.
        """
        if og_item == new_item:
            return False

        for i in range(len(bundle)):
            if bundle[i] == new_item:
                return False

        T0 = bundle.copy()
        index = []
        for i in range(len(T0)):
            if T0[i] == og_item:
                index.append(i)
        if len(index) == 0:
            return False

        T0.pop(index[0])
        T0.append(new_item)

        og_val = self.valuation(bundle)
        new_val = self.valuation(T0)
        if og_val == new_val:
            return True
        else:
            return False
