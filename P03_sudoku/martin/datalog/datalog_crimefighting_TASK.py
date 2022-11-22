#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:38:21 2017

@author: tugg
update: vissejul, bachmdo2, stdm (Nov 27, 2018)
"""
import pandas as pa
from pyDatalog import pyDatalog

# ---------------------------------------------------------------------------
# Social graph analysis:
# work through this code from top to bottom (in the way you would use a R or Jupyter notebook as well...) and write datalog clauses
# and python code in order to solve the respective tasks. Overall, there are 7 tasks.
# ---------------------------------------------------------------------------
calls = pa.read_csv('P03_sudoku/martin/datalog/calls.csv', sep='\t', encoding='utf-8')
texts = pa.read_csv('P03_sudoku/martin/datalog/texts.csv', sep='\t', encoding='utf-8')

suspect = 'Quandt Katarina'
contact = 'Scheunemann Dario'
company_Board = ['Soltau Kristine', 'Eder Eva', 'Michael Jill']

pyDatalog.create_terms('knows', 'has_link', 'can_reach', 'paths', 'A', 'B', 'C', 'D', 'P', 'P2', 'X', 'Y', 'many_more_needed')
pyDatalog.clear()

# First, treat calls as simple social links (denoted as knows), that have no date
for i in range(0, 50):
    +knows(calls.iloc[i, 1], calls.iloc[i, 2])


# Task 1: Knowing someone is a bi-directional relationship -> define the predicate accordingly
# A knows B if B knows A
knows(A, B) <= knows(B, A)
print((X==suspect) & (knows(X, Y)))
print((Y==suspect) & (knows(X, Y)))
# Task 2: Define the predicate has_link in a way that it is true if a connection exists (path of people knowing the next link)
# A has a link to B if A knows B
has_link(A, B) <= knows(A, B)
# Adds transitivity
has_link(A, C) <= knows(A, B) & has_link(B, C) & (A != C)
print((X==suspect) & (has_link(X, Y)))
# Hints:
#   check if your predicate works: at least 1 of the following asserts should be true (2 if you read in all 150 communication records)
#   (be aware of the unusual behaviour that if an assert evaluates as true, an exception is thrown)
# assert (has_link('Quandt Katarina', company_Board[0]) == ())
# assert (has_link('Quandt Katarina', company_Board[1]) == ())
# assert (has_link('Quandt Katarina', company_Board[2]) == ())


# Task 3: You already know that a connection exists; now find the concrete paths between the board members and the suspect
# Hints:
#   if a knows b, there is a path between a and b
#   (X._not_in(P2)) is used to check whether x is not in path P2
#   (P==P2+[Z]) declares P as a new path containing P2 and Z
paths(A,B,P) <= paths(A,C,P2) & knows(C,B) & (A!=B) & (A._not_in(P2)) & (B._not_in(P2)) & (P==P2+[C])
paths(A,B,P) <= knows(A,B) & (P==[])

# Task 4: There are too many paths. We are only interested in short paths.
# Find all the paths between the suspect and the company board that contain five people or less


# ---------------------------------------------------------------------------
# Call-Data analysis:
# Now we use the text and the calls data together with their corresponding dates
# ---------------------------------------------------------------------------
date_board_decision = '12.2.2017'
date_shares_bought = '23.2.2017'
pyDatalog.create_terms('called', 'texted', 'contacted', 'P1', 'P2', 'Date')
pyDatalog.clear()

for i in range(0, 50):  # calls
    +called(calls.iloc[i, 1], calls.iloc[i, 2], calls.iloc[i, 3])

for i in range(0, 50):  # texts
    +texted(texts.iloc[i, 1], texts.iloc[i, 2], texts.iloc[i, 3])

called(P1, P2, Date) <= called(P2, P1, Date)  # calls are bi-directional


# Task 5: Again we are interested in links, but this time a connection is only valid if the links are descending in date;
#         find out who could have actually sent the information by adding this new restriction
# Hints:
#   You are allowed to naively compare the dates lexicographically using ">" and "<";
#   it works in this example (but is evil in general)
contacted(P1, P2, Date) <= called(P1, P2, Date)
contacted(P1, P2, Date) <= texted(P1, P2, Date)

# Task 6: Find all the communication paths that lead to the suspect (with the restriction that the dates have to be ordered correctly)


# Final task: after seeing this information, who, if anybody, do you think gave a tip to the suspect?


# General hint (only use on last resort!):
#   if nothing else helped, have a look at https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
