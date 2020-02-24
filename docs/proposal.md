---
layout: default
title:  Proposal
---

##	Proposal


### Summary

Our project is a minecraft rendition of Wumpus World. In our Wumpus World implementation, the agent has to navigate several worlds of dynamic size, trying to collect a piece of gold while avoiding hazards. These hazards come in the form of a single Wumpus, and any number of pits. These hazards gives feedback to the agent in the blocks adjacent to them. A block next to a Wumpus will notify the agent through a stench, a block next to a pit will notify the agent through a breeze, and a block next to both these dangers will notify the agent with both a stench and a breeze. Dying by any of the hazards will yield a large penalty in the scoring system. Our goal is to create an AI that is able to navigate these worlds in such a way that it maximizes the score it gets.

### Algorithms

We will use a shortest-path algorithm for the agent to find its way back to the starting point after either determining that it either can't complete its objective safely or if it found the gold.

### Evaluation

Scoring our agent is very simple. We will base the performance of out agent on the score our agent is able to score in a set number of worlds (tentatively 10). We will average the score and see what is the highest score it is able to score. The actual number we will use have to wait until we implement the worlds.

### Appointment Date

April 24th 4:30pm.
