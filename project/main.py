#import MalmoAI_DFS_Dijkstra as MalmoAI
#import MalmoAI_DFS as MalmoAI
import MalmoAI_AStar as MalmoAI
#import MalmoAI_AStar_noH as MalmoAI
import worldGenerator
import feed_back

try:
	from malmo import MalmoPython
except:
	import MalmoPython

import os
import sys
import time
import json
import random


if __name__ == "__main__":
    record = open('WumpusRecords20.txt', 'a')
    scoreDict = {}
    sizeSequence = []
    for n in range(20):
        sizeSequence.append((8, 2))
    for n in range(20):
        sizeSequence.append((10, 4))
    for n in range(20):
        sizeSequence.append((14, 7))
    for n in range(20):
        sizeSequence.append((18, 8))
    for n in range(20):
        sizeSequence.append((22, 10))



    #[(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),(16,10),]
    #[(6,0), (8,1) , (12,8), (16,12), (20,25)] 
    #[(20,25)]
    # world = [ ['glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','wool','air','wool','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','wool','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','wool','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','wool','air','wool','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','wool','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','obsidian','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','obsidian','stone','obsidian','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','obsidian','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','gold_block','glass'],
    #         ['glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass'] ]

    # world = [ ['glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','wool','air','wool','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','wool','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','wool','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','wool','air','wool','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','wool','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','obsidian','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','obsidian','stone','obsidian','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','obsidian','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','glass'],
    #         ['glass', 'stone','stone','stone','stone','stone','stone','stone','stone','stone','stone','gold_block','glass'],
    #         ['glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass','glass'] ]

    scores = []
    #sizeSequence = [1]
    for item in sizeSequence:
        start, world, wumpus = worldGenerator.generateWorldMatrix(item[0],item[0],item[1]) 
        #start = [1,1]
        #wumpus = [8,7]
        worldXML = worldGenerator.worldToXML(start, world, wumpus)
        # Mission and AI stuff
        missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                            
                              <About>
                                    <Summary>Wumpus world!</Summary>
                              </About>
                              
                              <ServerSection>
                                    <ServerInitialConditions>
                                      <Time>
                                        <StartTime>6000</StartTime>
                                        <AllowPassageOfTime>false</AllowPassageOfTime>
                                      </Time>
                                      <Weather>clear</Weather>
                                      <AllowSpawning>false</AllowSpawning>
                                    </ServerInitialConditions>
                                    <ServerHandlers>
                                      <FlatWorldGenerator generatorString="3;7,2*3,2;1;village"/>
                                      <DrawingDecorator>
                                            <DrawSphere x="0" y="3" z="0" radius="100" type="air"/>                    
                                      </DrawingDecorator>''' + worldXML + '''
                                      <ServerQuitWhenAnyAgentFinishes/>
                                    </ServerHandlers>
                              </ServerSection>
                              
                              <AgentSection mode="Survival">
                                    <Name>MalmoTutorialBot</Name>
                                    <AgentStart>
                                      <Placement x="1" y="1" z="1" yaw="270" pitch="60"/>
                                    </AgentStart>
                                    <AgentHandlers>
                                      <ObservationFromFullStats/>
                                      <DiscreteMovementCommands/>
                                      <AbsoluteMovementCommands/>
                                      <AgentQuitFromTouchingBlockType>
                                        <Block type="torch"/>
                                      </AgentQuitFromTouchingBlockType>
                                      <ChatCommands/>
                                      <MissionQuitCommands/>
                                    </AgentHandlers>
                              </AgentSection>
                            </Mission>'''

    # Create default Malmo objects:

        agent_host = MalmoPython.AgentHost()
        try:
                agent_host.parse( sys.argv )
        except RuntimeError as e:
                print('ERROR:',e)
                print(agent_host.getUsage())
                exit(1)
        if agent_host.receivedArgument("help"):
                print(agent_host.getUsage())
                exit(0)

        my_mission = MalmoPython.MissionSpec(missionXML, True)
        my_mission_record = MalmoPython.MissionRecordSpec()

        # Attempt to start a mission:
        max_retries = 3
        for retry in range(max_retries):
                try:
                        agent_host.startMission( my_mission, my_mission_record )
                        break
                except RuntimeError as e:
                        if retry == max_retries - 1:
                                print("Error starting mission:",e)
                                exit(1)
                        else:
                                time.sleep(2)

    # Loop until mission starts:
        print("Waiting for the mission to start ", end=' ')
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
                print(".", end="")
                time.sleep(0.1)
                world_state = agent_host.getWorldState()
                for error in world_state.errors:
                        print("Error:",error.text)

        print()
        print("Mission running ", end=' ')
        '''
        agent_host.sendCommand("turn 1")
        time.sleep(1)
        agent_host.sendCommand("turn 1")
        time.sleep(1)
        agent_host.sendCommand("turn 1")
        time.sleep(1)
        agent_host.sendCommand("turn 1")
        time.sleep(1)
        agent_host.sendCommand("turn 1")
        time.sleep(1)
        agent_host.sendCommand("turn 1")
        time.sleep(1)
        #agent_host.sendCommand("turn -1")
        '''
#'''
    # Loop until mission ends:
        while world_state.is_mission_running:

                print(".", end="")
                #time.sleep(0.1)

                world_state = agent_host.getWorldState()
                game = feed_back.feedback(world)
                wumpusAI = MalmoAI.MalmoAI()
                game.map = world
                climbed = False
                foundGold = False
                tp_command = "tp " + str(game.get_current_location()[0]+0.5)+ " 1 " + str(game.get_current_location()[1]+0.5)
                agent_host.sendCommand(tp_command)
                while True:
                        #input()
                        world_state = agent_host.getWorldState()
                        if world_state.is_mission_running == False:
                            game.score -= 10000
                            break
                        #input()
                        print(game.get_state())
                        print(game.get_current_location())
                        s, br, b, g = game.get_state()
                        #direction = input("direction: ")
                    
                        action = wumpusAI.getMovement(s, br, g, b)
                        #input()
                        game.process(action)

                        #time.sleep(0.05)
                        time.sleep(0.1)
                        s, br, b, g = game.get_state()
                        if b != True:
                            moveCommand = ""
                            if action == MalmoAI.Movement.NORTH:
                                moveCommand = "moveeast 1"
                            elif action == MalmoAI.Movement.SOUTH:
                                moveCommand = "movewest 1"
                            elif action == MalmoAI.Movement.WEST:
                                moveCommand = "movenorth 1"
                            elif action == MalmoAI.Movement.EAST:
                                moveCommand = "movesouth 1"
                            print("--------Attempt Move: ", moveCommand)
                            agent_host.sendCommand(moveCommand)

                        if action == MalmoAI.Movement.STABN:
                            agent_host.sendCommand("attack 1")
                            agent_host.sendCommand("attack 0")
                        if action == MalmoAI.Movement.STABS:
                            agent_host.sendCommand("turn 1")
                            #time.sleep(1.0)
                            agent_host.sendCommand("turn 1")
                            time.sleep(.5)

                            agent_host.sendCommand("attack 1")
                            #agent_host.sendCommand("attack 0")
                            #agent_host.sendCommand("turn 0")
                            time.sleep(.5)
                            agent_host.sendCommand("turn -1")
                            #time.sleep(1.0)
                            agent_host.sendCommand("turn -1")

                        if action == MalmoAI.Movement.STABE:
                            agent_host.sendCommand("turn 1")
                            #agent_host.sendCommand("move 1")
                            time.sleep(.5)
                            #agent_host.sendCommand("turn 0")

                            agent_host.sendCommand("attack 1")
                            #agent_host.sendCommand("attack 0")
                            
                            time.sleep(.5)
                            agent_host.sendCommand("turn -1")
                            
                        if action == MalmoAI.Movement.STABW:
                            agent_host.sendCommand("turn -1")
                            #agent_host.sendCommand("move 1")
                            time.sleep(.5)
                            #agent_host.sendCommand("turn 0")

                            agent_host.sendCommand("attack 1")
                            #agent_host.sendCommand("attack 0")

                            time.sleep(.5)
                            agent_host.sendCommand("turn 1")
                            #agent_host.sendCommand("turn 0")

                        print("Current Score: ", game.score)
                        if (action == MalmoAI.Movement.GRAB):
                                foundGold = True
                                print("GRAB Gold")
                                #time.sleep(1.0)
                                continue
                        if (action == MalmoAI.Movement.CLIMB and game.current_location == game.start_location):
                                climbed = True
                                print("CLIMB out")
                                print("Final Score: ", game.score)
                                scores.append(game.score)
                                if (item not in scoreDict):
                                    scoreDict[item] = []
                                    scoreDict[item].append(game.score)
                                else:
                                    scoreDict[item].append(game.score)
                                print(scoreDict)
                                break;
                                    
                if world_state.is_mission_running == False:
                    print("Agent Died...")
                    print("Final Score: ", game.score)
                    scores.append(game.score)
                    if (item not in scoreDict):
                        scoreDict[item] = []
                        scoreDict[item].append(game.score)
                    else:
                        scoreDict[item].append(game.score)
                    print(scoreDict)
                    agent_host.sendCommand("chat Score = " + str(game.score))
                    break

                for error in world_state.errors:
                        print("Error:",error.text)

                if (climbed):
                        agent_host.sendCommand("chat Score = " + str(game.score))
                        break;

        print()
        print("Mission ended")
        # Mission has ended.
    total = 0
    for s in scores:
        total += s
        record.write(str(s)+',')

    # for n in range(50):
    #     sizeSequence.append((8, 2))
    # for n in range(50):
    #     sizeSequence.append((10, 4))
    # for n in range(50):
    #     sizeSequence.append((14, 7))
    # for n in range(50):
    #     sizeSequence.append((18, 8))
    # for n in range(50):
    #     sizeSequence.append((22, 10))
    # for n in range(50):
    #     sizeSequence.append((14, 7))

    #sizeList = [(8,2), (10,4), (14, 7), (18,8), (22, 10)]
    #f = open("dfs.txt", "a")
    #for x in sizeList:
    #    for y in scoreDict[x]:
    #        f.write(str(x[0]) + "," + str(y) + "\n")
    #f.close()


    avg = total / len(sizeSequence)
    print("Average Score Across All Worlds: ", avg)
    
    record.close()
#'''