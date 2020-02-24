---
layout: default
title:  Status
---

## Status Report

### Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/FXvRF2sHi5A" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Project Summary

The ultimate goal of this project is to create an AI that is able to navigate through a world with similar rules as the infamous Wumpus World AI problem. The rules of Wumpus World is relatively simple. Each world comes with dangers in the form of a single Wumpus and any number of pits. The goal is to get around these dangers while also actively looking for a randomly placed gold block somewhere in the world. The AI does this through feedbac, given to it by the world, about its current block and its adjacent block. Once the gold is found, the AI needs to find its way back and climb out of the world. 

### Approach

The approach for our AI is simply a set of constraint satisfaction problems. However, the AI is just a piece of our project. To understand what needed to be done, lets go over chronologically everything we had to implement up to and including the actual AI.

The Wumpus World game "manager" was written completely from scratch. The manager's job is to enforce the game's rules. It keeps track of the AI's score (discussed further under Evaluations) as well as the agent's current location by recording a set of coordinates and keeping a 2d array representing the world. The map and the agent's location is cross-referenced every time before the AI takes an action so that appropriate feedback is given to the AI about its surrounding. Everytime the AI is requested to make a move, the AI is given 4 boolean values. They are: stench, breeze, glitter, and bump. A stench signals that there is a Wumpus somewhere adjacent to the agent. Similarly, a breeze indicates that there is at least one pit adjacent to the agent. Glitter indicates that the agent is standing on a spot with gold. Finally, a bump signals that the AI's previous move resulted in it bumping into a wall. The AI is completely blind to the world except for these details given to it by the manager. 

A world generator was also created to facilliate the testing and evaluation of the AI. The world generator uses string manipulation to edit the XML inputs of the Malmo interface to create random worlds that conform to our rules. Currently, a lava block represents the Wumpus and obsidian blocks represent a stench. The obsidian blocks must be placed adjacent to the lava blocks every time it's placed. Likewise, wool blocks representing a breeze must be placed adjacently to a pit represented by an air block. 

As stated, the actual AI that is used to run through the world operates under a set of constraints satisfaction problems introduced by the different feedback it gets from the world. Mainly, this was solved through many if-else statements, parsing through the different combination of feedback and picking an appropriate action. To determine where to go next, the AI keeps a representation of the map, as well as a set of safe locations. Initially, the AI does not know anything about the world, so it slowly maps out the world as it finds safe spaces to move hoping to findd the gold. Should it find the block with the gold, the AI will run a Dijkstra/BFS algorithm (implemented with a priority dictionary implemented by Prof. David Eppstein) to find the shortest path back to the start and climb out. Should the AI exhaust the set of safely movable blocks, it will again find the shortest path back out.

### Evaluation

To grade the AI, a scoring system is used. Dying from either the Wumpus or a pit procures a penalty of -10000 points. Climbing and grabbing at inappropriate times will procure a penalty of -10 points. Getting the gold out successfully nets a score of +1000. Any other action takes -1 point. We run the AI against a a number of worlds varying in size to get an average score among all the worlds. If the AI works flawlessly, the point average should be positive when ran against many worlds. With this in mind, the AI is works if the score averages a positive score, but whether it works well depends on how high of an average score it gets. We are currently still trying multiple methods to determine our highest score.

### Remaining Goals and Challenges

We are still in the process of doing a more rigorous evaluation of the agent. There are still a number of things we are trying so that the agent scores higher. As of right now, we are testing whether or not a different queuing order for possible moves can improve the score. 

Our map is also relatively static; the start and gold blocks are set currently at opposite corners of each other. Part of our plan to run our AI in a more unforgiving world is to randomize these two locations and see if the AI can get the gold safely and effectively. Relating to this, we might also implement a moving Wumpus. The Wumpus will move in a set pattern rather than in random directions. This significantly increases the complexity in the AI's decision making, so whether or not this will ultimately be implemented in our project will be discussed after implementing everything that was aforementioned.
