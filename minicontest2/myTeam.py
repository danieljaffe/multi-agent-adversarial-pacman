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

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    def value(state, cur_depth, agent_index, a, b):
      """if state.isWin() == True or state.isLose() == True:
        return self.evaluationFunction(state)"""
      if agent_index == 1:
        cur_depth -= 1
      if (cur_depth == 0):
        return gameState.getScore()

      # For Pacman
      if agent_index % 2 == 1:
        bestValue = -9999999999
        next_agent_index = (agent_index + 1) % gameState.getNumAgents()
        legalMoves = state.getLegalActions(agent_index)
        if (len(legalMoves) == 0):
          return gameState.getScore()
        for action in legalMoves:
          next_state = state.generateSuccessor(agent_index, action)
          next_state_value = value(next_state, cur_depth, next_agent_index, a, b)
          bestValue = max(bestValue, next_state_value)
          a = max(a, bestValue)
          if b < a:
            break
        return bestValue

      # For Ghost
      if agent_index % 2 == 0:
        bestValue = 9999999999
        next_agent_index = (agent_index + 1) % gameState.getNumAgents()
        legalMoves = state.getLegalActions(agent_index)
        if (len(legalMoves) == 0):
          return gameState.getScore()
        for action in legalMoves:
          next_state = state.generateSuccessor(agent_index, action)
          next_state_value = value(next_state, cur_depth, next_agent_index, a, b)
          bestValue = min(bestValue, next_state_value)
          b = min(b, bestValue)
          if b < a:
            break
        return bestValue

    alpha = -9999999999
    beta = 9999999999
    a = -9999999999
    b = 9999999999
    agent_index = self.index
    scores = []
    legalMoves = gameState.getLegalActions(agent_index)
    for action in legalMoves:
      bestValue = -9999999999
      next_state = gameState.generateSuccessor(agent_index, action)
      self.depth = 2
      next_state_value = value(next_state, self.depth, agent_index + 1, a, b)
      scores.append(next_state_value)
      bestValue = max(bestValue, next_state_value)
      a = max(a, bestValue)
      if b < a:
        break

    # FOR SELECTING MOVE ONLY
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
    return legalMoves[chosenIndex]