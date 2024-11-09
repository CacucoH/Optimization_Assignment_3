# Assignment 3
Write a computer program in any programming language (e.g. Python, C++) to find initial
basic feasible solution for given transportation problem by using
(a) North-West corner method,
(b) Vogel’s approximation method,
(c) Russell’s approximation method.

# Solution
The final version of a program `combined_version.py` solves a problem using 3 methods requested by the task and prints all necessary information.

In case of problem invalidity returns:
- ”The method is not applicable!” - If, for example, costs matrix contains value <= 0
- ”The problem is not balanced!” - If problem is unbalanced

# Example of inputs
Program ask for Supply, Demand and Costs.
Example of inserting this problem:

[example table](https://i.imgur.com/e8LnLRo.png)
```inputs
Enter the supply values (space-separated): 7 9 18
Enter the demand values (space-separated): 5 8 7 14
Enter the cost matrix (3 rows, 4 columns):
Enter the costs for supply point 1: 19 30 50 10
Enter the costs for supply point 2: 70 30 40 60
Enter the costs for supply point 3: 40 8 70 20
```