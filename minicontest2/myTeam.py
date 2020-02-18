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


#########################
# ExpectimaxAgent Class #
#########################

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


###############################
# MultiAgentSearchAgent Class #
###############################

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


#####################################
# betterEvaluationFunction Function #
#####################################

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    current_pos = currentGameState.getPacmanPosition()
    current_food = currentGameState.getFood()
    current_ghost_states = currentGameState.getGhostStates()
    # Checks food positions The farther food is away, the larger this number will be. We want to minimize this! Also,
    # the less food on the map, the better so the number of food pellets is really important. This also rewards
    # Pacman with a greater number of points the closer in proximity he is to food.
    food_score = 0
    total_food_dist = 0
    num_food = len(current_food.asList())
    for food in current_food.asList():
        temp = abs(dist(current_pos, food))
        if temp <= 12:
            food_score += 0.1
        if temp <= 11:
            food_score += 0.1
        if temp <= 10:
            food_score += 0.1
        if temp <= 9:
            food_score += 0.1
        if temp <= 8:
            food_score += 0.1
        if temp <= 7:
            food_score += 0.1
        if temp <= 6:
            food_score += 0.2
        if temp <= 5:
            food_score += 0.2
        if temp <= 4:
            food_score += 0.2
        if temp <= 3:
            food_score += 0.5
        if temp <= 2:
            food_score += 0.5
        if temp <= 1:
            food_score += 2
        total_food_dist += temp
    if num_food > 0:
        avg_food_distance = total_food_dist / num_food
        # The more food on the board, the worse the score of this turn. Also the greater the average distance from
        # food, then the worse score as we are likely moving farther from clusters of pellets. Since there are edge
        # cases where this doesn't hold true, the weight of the average pellet distance has a reducing factor on it.
        # I also needed to add a scalar for num_food so that each pellet is worth a bit more.
        food_score -= (num_food * 100) + avg_food_distance

    # Checks ghost positions with the addition of special added weight when ghosts are particularly close. This
    # should prevent Pacman from getting over excited based on pills alone. The larger this number, the better!
    # Certain edge cases where a ghost is close will reduce the ghost score to prevent moves made that will bring
    # Pacman into the danger zone.
    ghost_score = 0
    total_ghost_dist = 0
    num_ghosts = 0
    for ghost in current_ghost_states:
        temp = abs(dist(current_pos, ghost.getPosition()))
        if temp == 5:
            ghost_score -= 0.001
        if temp == 4:
            ghost_score -= 0.02
        if temp == 3:
            ghost_score -= 1
        if temp == 2:
            ghost_score -= 10
        if temp == 1:
            ghost_score -= 100
        if temp == 0:
            ghost_score -= 1000
        total_ghost_dist += temp
        num_ghosts += 1
    if num_ghosts > 0:
        avg_ghost_distance = total_ghost_dist / num_ghosts
        # A larger average distance of ghosts helps means a better game state
        ghost_score += avg_ghost_distance

    total_score = food_score + ghost_score

    if currentGameState.isWin():
        total_score += 100

    return total_score


# Abbreviation
better = betterEvaluationFunction