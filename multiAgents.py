# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score=0.0
        
        #check distance to Ghosts
        #try to eat ghosts
        for ghost in newGhostStates:
          distanceToGhost=manhattanDistance(ghost.getPosition(), newPos)
          if(distanceToGhost<=1):
            if(ghost.scaredTimer!=0):
              score+=5000
            else:
              score-=500

        #check distance to power pellets
        for capsule in currentGameState.getCapsules():
          distancePellet=manhattanDistance(capsule,newPos)
          if(distancePellet==0):
            score+=500
          else:
            score+=10.0/distancePellet

        #check distance to food
        for x in range(currentGameState.getFood().width):
          for y in range(currentGameState.getFood().height):
            if(currentGameState.getFood()[x][y]):
              distanceFood=manhattanDistance((x,y),newPos)
              if(distanceFood==0):
                score+=100
              else:
                score+=1.0/(distanceFood**2)

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        score,maxMove=self.maxValue(gameState,self.depth)

        return maxMove

    def minValue(self,gameState,agent, depth):  
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "end"

        action=gameState.getLegalActions(agent)
        scores=[]
        if(agent!=gameState.getNumAgents()-1):
          scores =[self.minValue(gameState.generateSuccessor(agent,move),agent+1,depth) for move in action]
        else:
          scores =[self.maxValue(gameState.generateSuccessor(agent,move),(depth-1))[0] for move in action]
        minScore=min(scores)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, action[chosenIndex]

    def maxValue(self,gameState,depth):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "end"

        action=gameState.getLegalActions()
        scores = [self.minValue(gameState.generateSuccessor(self.index,move),1, depth) for move in action]
        score=max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == score]
        chosenIndex = bestIndices[0]
        return score,action[chosenIndex]
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self,gameState):

        def maxAgent(state, depth, alpha, beta):
            if state.isWin() or state.isLose():
                return state.getScore()
            actions = state.getLegalActions(0)
            bestScore = float("-inf")
            score = bestScore
            bestAction = Directions.STOP
            for action in actions:
                score = minAgent(state.generateSuccessor(0, action), depth, 1, alpha, beta)
                if score > bestScore:
                    bestScore = score
                    bestAction = action
                alpha = max(alpha, bestScore)
                if bestScore > beta:
                    return bestScore
            if depth == 0:
                return bestAction
            else:
                return bestScore

        def minAgent(state, depth, ghost, alpha, beta):
            if state.isLose() or state.isWin():
                return state.getScore()
            nextGhost = ghost + 1
            if ghost == state.getNumAgents() - 1:
                nextGhost = 0
            actions = state.getLegalActions(ghost)
            bestScore = float("inf")
            score = bestScore
            for action in actions:
                if nextGhost == 0:
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                    else:
                        score = maxAgent(state.generateSuccessor(ghost, action), depth + 1, alpha, beta)
                else:
                    score = minAgent(state.generateSuccessor(ghost, action), depth, nextGhost, alpha, beta)
                if score < bestScore:
                    bestScore = score
                beta = min(beta, bestScore)
                if bestScore < alpha:
                    return bestScore
            return bestScore
        return maxAgent(gameState, 0, float("-inf"), float("inf"))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        agents = gameState.getNumAgents()

        def calculateMax(gameState, depth):
            actions = gameState.getLegalActions(0)

            if depth > self.depth or gameState.isWin() or not actions:
                return self.evaluationFunction(gameState), None

            successors = []
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                successors.append((calculateMin(successor, 1, depth)[0], action))

            return max(successors)

        def calculateMin(gameState, agent, depth):
            actions = gameState.getLegalActions(agent)
            if not actions or gameState.isLose():
                return self.evaluationFunction(gameState), None

            successors = [gameState.generateSuccessor(agent, action) for action in actions]

            successors = []
            for successor in successors:
                if agent ==0:
                    successors.append(calculateMax(successor, depth + 1))
                else:
                    successors.append(calculateMin(successor, agent + 1, depth))

            averageScore = sum(map(lambda x: float(x[0]) / len(successors), successors))
            return averageScore, None

        return calculateMax(gameState, 1)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
