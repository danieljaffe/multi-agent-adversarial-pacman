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
import math

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='DummyAgent', second='DummyAgent'):
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
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


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


###########
# Minimax #
###########

class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # This agent is Pacman
        agentIndex = 0
        local_depth = self.depth
        action = self.expectimax(gameState, local_depth, agentIndex)
        return action

    # Credit to this tutorial for help understanding what I need to do here. He explains the algorithm and why it
    # should work. Obviously, hes design doesn't solve our problem here, but its helped to point me in the right
    # direction. https://www.youtube.com/watch?v=l-hh51ncgDI
    def expectimax(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            best_action = None
            max_score = -math.inf
            for action in gameState.getLegalActions(agentIndex):
                score = self.expectimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                if score > max_score:
                    max_score = max(max_score, score)
                    best_action = action
            if depth == self.depth:
                return best_action
            else:
                return max_score
        else:
            final_ghost = agentIndex == gameState.getNumAgents() - 1
            min_score = math.inf
            if final_ghost:
                next_depth = depth - 1
                next_agent = 0
            else:
                next_depth = depth
                next_agent = agentIndex + 1
            scores = []
            legal_actions = gameState.getLegalActions(agentIndex)
            for action in legal_actions:
                score = self.expectimax(gameState.generateSuccessor(agentIndex, action), next_depth, next_agent)
                scores.append(score)
            min_score = sum(scores) / len(scores)
            return min_score