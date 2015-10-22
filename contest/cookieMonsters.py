# Students:
# Name            Student ID.
# Tou LEE         656128
# Jaime Martinez  642231
from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
import searchAgents
from baselineTeam import DefensiveReflexAgent
from searchAgents import  manhattanHeuristic, SearchAgent,PositionSearchProblem
import search

def createTeam(firstIndex, secondIndex, isRed):
              # first = 'OffensiveAgent', second = 'DummyAgent'):
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
  return [OffensiveAgent(firstIndex), DefensiveAgent(secondIndex)]


class OffensiveAgent(CaptureAgent):

    def __init__( self, index, timeForComputing = .1 ):
        CaptureAgent.__init__( self, index, timeForComputing)
        print self.red, index, timeForComputing
        self.visibleAgents = []
        self.foodLeft = 0
        self.foodEaten = 0
        self.isPacman = False
        self.a = []
        self.first = True
        self.size = 0

    def chooseAction(self,gameState):
        currObs = self.getCurrentObservation()
        self.isPacman = currObs.getAgentState(self.index).isPacman
        opponents = self.getOpponents(currObs)
        self.visibleAgents= []
        for x in opponents:
            self.visibleAgents += [currObs.getAgentPosition(x)]
        food =  self.getFood(currObs)
        capsules =  self.getCapsules(currObs)
        foodList= food.asList(True)
        foodList+=capsules
        defendedFood = self.getFoodYouAreDefending(currObs).asList(True)
        mypos = gameState.getAgentState(self.index).getPosition()
        #check and initialise a few variables only at the start of the game
        if self.first:
            self.allFood = len(foodList)
            self.first = False
            self.width = currObs.getWalls().width
            self.height= currObs.getWalls().height
            self.isRed = currObs.isOnRedTeam(self.index)
            #goal =  random.choice(food.asList(True))
        self.foodLeft = len(foodList)
        self.foodEaten = self.allFood - self.foodLeft
        #CHOOSE GOAL Here
        #threshold = self.foodLeft/3
        threshold = 4

        #Check for opponents, try to find capsule or go back to base,
        #whichever is closer.
        if self.visibleAgents[0] != None or self.visibleAgents[1] != None:
            d2 = self.returnToBaseGoal(currObs,mypos)
            if len(capsules)>0:
                d1 = self.closest(capsules,mypos)
                goal = self.closest([d1,d2],mypos)
            else:
                goal = d2
        elif self.foodEaten <=threshold :
            #while foodEaten is less than threshold keep eating
            goal= self.closest(foodList,mypos)

        elif self.isPacman :
            #defend and return food
            #goal = self.closest(currObs,defendedFood,mypos)
            goal = self.returnToBaseGoal(currObs,mypos)
        else:
            #after touching base, return to eat more food
            self.allFood-=self.foodEaten
            self.foodEaten = 0
            goal= self.closest(foodList,mypos)

        #Using modified version of AnyFoodSearchProblem, more notes in README.txt
        afsp = searchAgents.AnyFoodSearchProblem(currObs,self.index,food,goal,self.visibleAgents,opponents,self.getMazeDistance)
        self.a = search.aStarSearch(afsp, searchAgents.manhattanHeuristic)
        action = None
        if len(self.a) != 0:
            action = self.a.pop(0)
        else:
            action = random.choice(gameState.getLegalActions(self.index))
        return action
    #return the closest base point to my pos
    def returnToBaseGoal(self,currObs,mypos):
        midPoints = []
        if self.isRed:
            w = self.width/2-1
        else:
            w = self.width/2+1
        for i in range(self.height):
            if currObs.hasWall(w,i):
                continue
            else:
                midPoints+=[(w,i)]
        return self.closest(midPoints,mypos)

    def closest(self, foodList,mypos):
        #print point
        dist = []
        for point in foodList:
            mydist = self.getMazeDistance(mypos, point)
            #print mydist
            dist+= [(point,self.getMazeDistance(mypos, point))]
        minp,_ =  min(dist, key = lambda t: t[1])
        return minp


# The security agent that is in charge to kill near by enemies
class DefensiveAgent(OffensiveAgent):

  def __init__( self, index, timeForComputing = .1 ):
    OffensiveAgent.__init__( self, index, timeForComputing)
    self.visibleAgents = []


  def chooseAction(self,gameState):
    currObs = self.getCurrentObservation()
    self.position = currObs.getAgentPosition(self.index)
    opponents = self.getOpponents(currObs)
    defendedFood = self.getFoodYouAreDefending(currObs).asList(True)
    self.visibleAgents = []

    # Check whether there are visible opponents
    for i in opponents:
        if currObs.getAgentPosition(i) is not None:
            self.visibleAgents += [currObs.getAgentPosition(i)]

    # There are no visible opponents
    if len(self.visibleAgents) == 0:
      randomFood = random.choice(defendedFood)
      defendingProblem = PositionSearchProblem(currObs, self.index, randomFood)
    else:
    #  Guard ghost sees opponent and finds it to kill it
      closestOpponent =   self.closest(self.visibleAgents, self.position)
      defendingProblem = PositionSearchProblem(currObs, self.index, closestOpponent)

    actions = search.breadthFirstSearch(defendingProblem)
    # In case that the random position chosen is where the agent is standing
    # give a random action
    if len(actions) != 0:
        return actions[0]
    else:
        return random.choice(gameState.getLegalActions(self.index))
