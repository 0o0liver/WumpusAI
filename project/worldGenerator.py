try:
    from malmo import MalmoPython
except:
    import MalmoPython

import os
import sys
import time
import json
import random

# Optional
def generateStart(sizeX, sizeZ):
    startX = random.randint(1, sizeX-2)
    startZ = random.randint(1, sizeZ-2)
    return [startX, startZ]

def generateGoal(sizeX, sizeZ):
    goalX = random.randint(1, sizeX-2)
    goalZ = random.randint(1, sizeZ-2)
    return [goalX, goalZ]

#def nearStart(start, point):
#    if (point == start or (start[0]-1,start[1]) == point or (start[0]+1,start[1]) == point or (start[0],start[1]-1) == point or (start[0],start[1]+1) == point):
#        return True
#    else:
#        return False

def nearImportant(important, point):
    if (point == important or (important[0]-1,important[1]) == point or (important[0]+1,important[1]) == point or (important[0],important[1]-1) == point or (important[0],important[1]+1) == point):
        return True
    else:
        return False


def generateWorldObstacles(sizeX, sizeZ, numOfPits, start, goal):
    # Randomly generates a world as a 2d matrix
    # randomly places lava(Wumpus) and
    #   air(pits)[random num of pits within a range] inside the map
    # places obsidian on the NSEW faces of lava (if valid)
    # places white wool on NSEW faces of pits (if valid)
    # Outer edges are walls of glass  

    # Generate Lava Coordinates
    lavaX = random.randint(1, sizeX-2)
    lavaZ = random.randint(1, sizeZ-2)
    #while ( (lavaX, lavaZ) == (start) or (lavaX, lavaZ) == (start[0]-1, start[1]) or (lavaX, lavaZ) == (start[0]+1, start[1]) or (lavaX, lavaZ) == (start[0], start[1]-1) or (lavaX, lavaZ) == (start[0], start[1]+1) ):
    while ( nearImportant( start, [lavaX,lavaZ]) ):#or nearImportant(goal, [lavaX,lavaZ]) ):
        lavaX = random.randint(1, sizeX-2)
        lavaZ = random.randint(1, sizeZ-2)
    lava = [lavaX, lavaZ]

    # Generate Multiple Pits
    # numOfPits = 10
    
    pits = []
    for i in range(numOfPits):
        pitX = random.randint(1, sizeX-2)
        pitZ = random.randint(1, sizeZ-2)
        #print("Near Start? ", nearImportant(start, [pitX,pitZ]) )
        while( [pitX,pitZ] in pits or (lava == [pitX,pitZ] ) or nearImportant(start, [pitX,pitZ] )  or nearImportant(goal, [pitX,pitZ] )):# or nearImportant(lava, (pitX,pitZ)) ):
            #print("Old PitX and PitZ: " + str(pitX) + "," + str(pitZ) )
            pitX = random.randint(1, sizeX-2)
            pitZ = random.randint(1, sizeZ-2)
            #print("Making New PitX and PitZ: " + str(pitX) + "," + str(pitZ) )
        pits.append( [pitX,pitZ] )
    
    return lava, pits

def generateWorldMatrix(sizeX, sizeZ, numOfPits):

    # fill whole world
    world = []
    for x in range(sizeX):
        row = []
        for z in range(sizeZ):
            row += ['stone']
        world.append(row)

    for i in range( len(world) ):
        for j in range( len(world[i]) ):
            if ( (i == 0) or (j == 0) or (i == sizeX-1) or (j == sizeZ-1) ):
                world[i][j] = 'glass'

    # generateStart(sizeX, sizeZ)
    start = [1,1]
    #start = generateStart(sizeX, sizeZ)

    # generateGoal(sizeX, sizeZ)
    #goal = [sizeX-2, sizeZ-2]
    goal = generateGoal(sizeX, sizeZ)

    wumpus, pits = generateWorldObstacles(sizeX, sizeZ, numOfPits, start, goal)

    obsidian = []
    if (wumpus[0]-1 > 0):
        obsidian.append( (wumpus[0]-1, wumpus[1]) )
    if (wumpus[0]+1 < sizeX-1):
        obsidian.append( (wumpus[0]+1, wumpus[1]) )
    if (wumpus[1]-1 > 0):
        obsidian.append( (wumpus[0], wumpus[1]-1) )
    if (wumpus[1]+1 < sizeZ-1):
        obsidian.append( (wumpus[0], wumpus[1]+1) )

    wool = []
    for p in pits:
        if (p[0]-1 > 0):
            wool.append( (p[0]-1, p[1]) )
        if (p[0]+1 < sizeX-1):
            wool.append( (p[0]+1, p[1]) )
        if (p[1]-1 > 0):
            wool.append( (p[0], p[1]-1) )
        if (p[1]+1 < sizeZ-1):
            wool.append( (p[0], p[1]+1) )

    #world[wumpus[0]][wumpus[1]] = 'redstone_block'
    
    for o in obsidian:
        world[o[0]][o[1]] = 'obsidian'
    for w in wool:
        if (w in obsidian):
            world[w[0]][w[1]] = 'glowstone'
        else:
            world[w[0]][w[1]] = 'wool'

    #world[start[0]][start[1]] = 'stone'#'emerald_block'
    

    if (wumpus in wool):
        world[wumpus[0]][wumpus[1]] = 'brown_wool'

    for p in pits:
        world[p[0]][p[1]] = 'air'

    world[goal[0]][goal[1]] = 'gold_block'

    return start, world, wumpus

def worldToXML(start, worldMatrix, wumpus):
    # input: 2d Matrix of block values
    # output: XML for generating the world
    # index represents world coordinates
    # i.e. index [0][0] is coordinate x=0, z=0
    # and index [0][1] is coordinate x=0, z=1 and [1][0] is x=1, z=0
    # X++ == forward (North); X-- == backwards (South);
    # Z++ == right (East) ; Z-- == left (West)
    worldXML = '<DrawingDecorator>'
    drawing = ''
    for x in range( len(worldMatrix) ):
        for z in range( len(worldMatrix) ):
            if (worldMatrix[x][z] == 'glass'):
                drawing += '<DrawBlock x="' + str(x) + '" y="' + str(0) + '" z="' + str(z) + '" type="' + worldMatrix[x][z] + '"/>'
                #drawing += '<DrawBlock x="' + str(x) + '" y="' + str(1) + '" z="' + str(z) + '" type="' + worldMatrix[x][z] + '"/>'
            else:
                drawing += '<DrawBlock x="' + str(x) + '" y="' + str(0) + '" z="' + str(z) + '" type="' + worldMatrix[x][z] + '"/>'

    drawing += '<DrawBlock x="' + str(start[0]) + '" y="' + str(1) + '" z="' + str(start[1]) + '" type="redstone_wire"/>'
    drawing += '<DrawBlock x="' + str(wumpus[0]) + '" y="' + str(1) + '" z="' + str(wumpus[1]) + '" type="torch"/>'
    worldXML += drawing + '</DrawingDecorator>'
    
    return worldXML

"""
# Test Main stuffs (run worldGenerator.py on its own in Malmo to see world Generated)

start, world, wumpus = generateWorldMatrix(8,8,2)
worldXML = worldToXML(start,world,wumpus)

# Mission and AI stuff
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,2*3,2;1;village"/>
                  <DrawingDecorator>
                    <DrawSphere x="0" y="3" z="0" radius="100" type="air"/>                    
                  </DrawingDecorator>''' + worldXML + '''
                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                  <Placement x="1" y="1" z="1" yaw="270" pitch="45"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <AbsoluteMovementCommands/>
                  <AgentQuitFromTouchingBlockType>
                    <Block type="torch"/>
                  </AgentQuitFromTouchingBlockType>
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

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)

    world_state = agent_host.getWorldState()

    for row in range(len(world)):
        for col in range(len(world[row])):
            time.sleep(0.5)
            tp_command = "tp " + str(row+0.5)+ " 1 " + str(col+0.5)
            agent_host.sendCommand(tp_command)
            if world_state.is_mission_running == False:
                break
        if world_state.is_mission_running == False:
            break
    
    #blockCommand = "setblock <1,1> <lapis_block>"
    #agent_host.sendCommand(blockCommand)

    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
#"""

