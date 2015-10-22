# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from searchAgents import FoodSearchProblem, foodHeuristic, manhattanHeuristic
import search

#################
# Team creation #
#################

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
  return [OffensiveAgent(firstIndex), DummyAgent(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)
class OffensiveAgent(CaptureAgent):

    def __init__( self, index, timeForComputing = .1 ):
        self.allFood = 0
        self.first = True
        CaptureAgent.__init__( self, index, timeForComputing)
        print self.red, index, timeForComputing
        self.visibleAgents = []
        self.foodLeft = 0
        self.foodEaten = 0
        self.isPacman = False
        self.a = []
        self.do = True

    def chooseAction(self,gameState):
        #actions = gameState.getLegalActions(self.index)
        #current state
        # self.generateProblem()
        # self.generateGoal()
        # self.


        currObs = self.getCurrentObservation()
        self.isPacman = currObs.getAgentState(self.index).isPacman
        opponents = self.getOpponents(currObs)
        visible =[]
        for x in opponents:
            visible += [currObs.getAgentPosition(x)]
        #print visible
        food =  self.getFood(currObs)
        defendedFood = self.getFoodYouAreDefending(currObs).asList(True)
        foodList = food.asList(True)
        if self.first:
            self.allFood = len(foodList)
            self.first = False
        self.foodLeft = len(foodList)
        self.foodEaten = self.allFood - self.foodLeft
        mypos = gameState.getAgentState(self.index).getPosition()
    #    print self.foodEaten
        act = []
        if self.foodEaten <= 5:
        #s    print 'here'
            goal= self.closest(currObs,foodList,mypos)
        elif self.isPacman :
            #defend and return food
            goal = self.closest(currObs,defendedFood,mypos)
        else:
            self.allFood-=self.foodEaten
            self.foodEaten = 0
            goal= self.closest(currObs,foodList,mypos)
 '''
        #goal = foodList
        #fsp = FoodSearchProblem(currObs,self.index,food,goal,visible)

        #searchAgent = AStarFoodSearchAgent(fsp,foodHeuristic)
    #    searchAgent.registerInitialState(obs,fsp)
        '''
        if len(self.a)<=2:
            print 'why', len(self.a)
            self.do = True
        if mypos == self.initialPosition:
            self.do = True
        if self.do:
            fsp = None
        #    print 'hereeeeeeee'
            goal = foodList
            #print 'goal',goal
            fsp = FoodSearchProblem(currObs,self.index,food,goal,visible)
            self.a = search.aStarSearch(fsp, foodHeuristic)
        #    print 'self' ,self.a
            self.do = False
        '''
        act = self.a.pop(0)
        print 'afterPop ',self.a


        return act

    def getGoal(self,gameState):
        return (0,0)
    def closest(self, gameState, foodList,mypos):
        #print point
        dist = []
        for point in foodList:
            mydist = self.getMazeDistance(mypos, point)
            #print mydist
            dist+= [(point,self.getMazeDistance(mypos, point))]
        minp,_ =  min(dist, key = lambda t: t[1])
        return minp
    def farthest(self, gameState, foodList,mypos):
        #print point
        dist = []
        for point in foodList:
            mydist = self.getMazeDistance(mypos, point)
            #print mydist
            dist+= [(point,self.getMazeDistance(mypos, point))]
        minp,_ =  max(dist, key = lambda t: t[1])
        return minp
