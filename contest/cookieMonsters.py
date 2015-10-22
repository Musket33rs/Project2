#cookieMonsters.py
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
#from searchAgents import FoodSearchProblem, foodHeuristic, manhattanHeuristic
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
  return [OffensiveAgent(firstIndex), DefensiveReflexAgent(secondIndex)]

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
        treshHold = self.foodLeft/3
        #treshHold = 4
        if self.foodEaten <=treshHold :
            #while foodEaten is less than 5 keep eating
            goal= self.closest(foodList,mypos)
        elif self.isPacman :
            #defend and return food
            #goal = self.closest(currObs,defendedFood,mypos)
            goal = self.getClosestGoal(currObs,mypos)
        else:
            #after touching base, return to eat more food
            self.allFood-=self.foodEaten
            self.foodEaten = 0
            goal= self.closest(foodList,mypos)

        #goal =  random.choice(food.asList(True))
        afsp = searchAgents.AnyFoodSearchProblem(currObs,self.index,food,goal,self.visibleAgents,opponents,self.getMazeDistance)
        self.a = search.aStarSearch(afsp, searchAgents.manhattanHeuristic)
        action = None
        if len(self.a) != 0:
            action = self.a.pop(0)
        else:
            action = random.choice(gameState.getLegalActions(self.index))
        return action
    def getClosestGoal(self,currObs,mypos):
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
