# ffteam.py

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import keyboardAgents
import game
from util import nearestPoint
import os

#############
# Factories #
#############


def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """
    # The following line is an example only; feel free to change it.
    return [FFAgent(firstIndex), FFAgent(secondIndex)]

##########
# Agents #
##########


class FFAgent(CaptureAgent):
    def __init__( self, index, timeForComputing = .1 ):
        CaptureAgent.__init__( self, index, timeForComputing)
        self.visibleAgents = []

    def createPDDLobjects(self):
        obs = self.getCurrentObservation()
        grid = obs.getWalls()
        locations = grid.asList(False)

        result = ''
        for (x, y) in locations:
            result += 'p_%d_%d ' % (x, y)

        return result

    def createPDDLfluents(self):
        result = ''
        obs = self.getCurrentObservation()
    
        (myx, myy) = obs.getAgentPosition(self.index)
        if obs.getAgentState(self.index).isPacman is True:
            result += '(AGENT_AT p_%d_%d) ' % (myx, myy)
        else:
            result += '(AGENT_AT p_%d_%d) ' % (myx, myy)

        #
        # Model opponent team if visible
        #
        self.visibleAgents = []
        other_team = self.getOpponents(obs)
        distances = obs.getAgentDistances()
        for i in other_team:
            if obs.getAgentPosition(i) is None:
                continue
            (x, y) = obs.getAgentPosition(i)
            if obs.getAgentState(i).isPacman is False:
                result += '(ENEMY_PHANTOM_AT p_%d_%d) ' % (x, y)
                if distances[i] < 2:
                    result += '(PHANTOM_NEAR p_%d_%d) ' % (x, y)
            else:
                self.visibleAgents.append(i)
                result += '(ENEMY_PACMAN_AT p_%d_%d) ' % (x, y)

        team = self.getTeam(obs)
        teamPos = []
        for i in team:
            if obs.getAgentPosition(i) is None:
                continue
            if i == self.index:
                continue
            (x, y) = obs.getAgentPosition(i)
            teamPos.append((x, y))

            if obs.getAgentState(i).isPacman is False:
                result += '(PHANTOM_AT p_%d_%d) ' % (x, y)
            else:
                result += '(PACMAN_AT p_%d_%d) ' % (x, y)

        #
        # Food.
        #
        food = self.getFood(obs).asList(True)
        for (x, y) in food:
            result += '(CHEESE_AT p_%d_%d) ' % (x, y)

        #
        # Capsule
        #
        capsule = self.getCapsules(obs)
        for (x, y) in capsule:
            result += '(CAPSULE_AT p_%d_%d) ' % (x, y)

        grid = obs.getWalls()
        for y in range(grid.height):
            for x in range(grid.width):
                if grid[x][y]:
                    continue
                for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                    if (0 <= x + dx < grid.width) and (0 <= y + dy < grid.height) and not grid[x + dx][y + dy]:
                        result += '(CAN_GO p_%d_%d p_%d_%d) ' % (x, y, x+dx, y+dy)
        return result

    def createPDDLgoal(self):
        result = ''
        obs = self.getCurrentObservation()
        food = self.getFood(obs).asList(True)
        for (x, y) in food:
            if self.closest(obs, (x, y)):
                result += '(not (CHEESE_AT p_%d_%d)) ' % (x,y)

        capsule = self.getCapsules(obs)
        for (x, y) in capsule:
            if self.closest(obs, (x, y)):
                result += '(not (CAPSULE_AT p_%d_%d)) ' % (x,y)
        grid = obs.getWalls()
        goal_x = grid.width/2 + int(not self.red)
        pos = obs.getAgentState(self.index).getPosition()
        result += '(AGENT_AT p_%d_%d) ' % (goal_x,
                                            min([y for y in range(grid.height)
                                                 if not grid[goal_x][y]],
                                                 key=lambda y: self.getMazeDistance((goal_x, y), pos)))
        return result

    def generatePDDLproblem(self):
        lines = list()
        lines.append("(define (problem strips-log-x-1)\n")
        lines.append("   (:domain pacman-strips)\n")
        lines.append("   (:objects \n")
        lines.append(self.createPDDLobjects() + "\n")
        lines.append("   )\n")
        lines.append("   (:init \n")
        lines.append(self.createPDDLfluents() + "\n")
        lines.append("   )\n")
        obs = self.getCurrentObservation()
        (x, y) = obs.getAgentPosition(self.index)
        #
        #I'M A PHANTOM
        #
        if obs.getAgentState(self.index).isPacman is False:
            lines.append("   (:goal \n")
            if len(self.visibleAgents) != 0:
                lines.append("  (PACMAN_DEAD) \n")
            else:
                lines.append("  ( and  \n")
                lines.append(self.createPDDLgoal() + "\n")
                lines.append("  )\n")
            lines.append("   )\n")
        #
        #I'M A PACMAN
        #
        else:
            lines.append("   (:goal \n")
            lines.append("     ( and (not (PACMAN_DEAD))  \n")
            lines.append(self.createPDDLgoal() + "\n")
            lines.append("     )\n")
            lines.append("   )\n")

        lines.append(")\n")
        cd = os.path.dirname(os.path.abspath(__file__))
        with open("%s/problem%d.pddl" % (cd, self.index), "w") as f:
            f.writelines(lines)

    def runPlanner(self):
        cd = os.path.dirname(os.path.abspath(__file__))
        os.system("./ff -s 2 -o {dir}/domain.pddl -f {dir}/problem{idx}.pddl > {dir}/solution{idx}.txt"
                  .format(dir=cd, idx=self.index))

    def parseSolution(self):
        cd = os.path.dirname(os.path.abspath(__file__))
        f = open("%s/solution%d.txt"%(cd,self.index),"r")
        lines = f.readlines()
        f.close()

        for line in lines:
            pos_exec = line.find("0: ")  #First action in solution file
            if pos_exec != -1:
                command = line[pos_exec:]
                command_splitted = command.split(' ')
                x = int(command_splitted[3].split('_')[1])
                y = int(command_splitted[3].split('_')[2])
                return (x, y)
        #
        # Empty Plan, Use STOP action, return current Position
        #
        if line.find("ff: goal can be simplified to TRUE. The empty plan solves it") != -1:
            return self.getCurrentObservation().getAgentPosition(self.index)
        print lines

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)

        bestAction = random.choice(actions)

        self.generatePDDLproblem()
        self.runPlanner()
        (newx, newy) = self.parseSolution()

        print "Target: ", newx, newy
         
        for a in actions:
            succ = self.getSuccessor(gameState, a)
            if succ.getAgentPosition(self.index) == (newx, newy):
                bestAction = a
        print self.index, bestAction, self.getCurrentObservation().getAgentPosition(self.index), (newx, newy)

        return bestAction

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        print pos
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def closest(self, gameState, point):
        print point
        mypos = gameState.getAgentState(self.index).getPosition()
        mydist = self.getMazeDistance(mypos, point)
        mindist = min(self.getMazeDistance(gameState.getAgentState(t).getPosition(), point)
                      for t in self.getTeam(gameState))
        return mydist == mindist


def dist(pos0, pos1):
    x0, y0 = pos0
    x1, y1 = pos1
    return math.abs(x0 - x1) + math.abs(y0 - y1)
