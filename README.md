# Allocation

The project focuses on implementing an algorithm for the Mixed Manna problem involving goods and chores as detailed in Viswanathan and Zick [2023]. The algorithm allocates items based on agents' preferences, where goods are valued at c > 1, chores are valued at -1, and indifferent items are valued at 0. Specifically, for the class of Order-Neutral submodular (ONSUB) valuation functions over {c, 0, -1}, the algorithm computes a complete leximin allocation. 

The implementation of the algorithm could have several applications in the real world- dividing chores among roommates, committees across faculty members. In these case, an individual might want to do a certain chore/committee, when another individual negatively values it. With an implementation of the algorithm, further extensions of creating an interface to input preferences can be explored. 


## Running the allocation algorithm
The following command installs the necessary libraries

```
pip install -r requirements.txt
```

To run the allocation algorithm: 

```
python scripts/combined_run.py 
```
This runs the algorithm over an example instance, which has been detailed in the report. 


## References
Vignesh Viswanathan and Yair Zick. Yankee swap: a fast and simple fair allocation mechanism for matroid
rank valuations. In Proceedings of the 22nd International Conference on Autonomous Agents and Multi-
Agent Systems (AAMAS), 2023.

Paula Navarrete Dıaz, Cyrus Cousins, George Bissias, and Yair Zick. Deploying fair and efficient course
allocation mechanisms. 2024.
