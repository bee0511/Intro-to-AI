from util import manhattanDistance
from game import Directions
import random, util
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
            "minimaxScore" function is a function that returns the score when 
            the game ends or the defined depth is reached. 
            The function would maximize score for "Pacman" and minimize score for "ghosts".
            
            For Pacman's maximization part, the function should find the maximum 
            score of the results obtained by running minimaxScore() with next agent, 
            the current depth, and the child game state. 
            
            Similarly, in the ghost minimization part, the function should find 
            the minimum score with the same function and parameters.

            Finally, to perform the maximum action for Pacman, traverse 
            through Pacman's legal moves and use minimaxScore() during the process.
            
        """  
        def minimaxScore(agent, depth, gameState):
            # check whether game is ended or reaches the defined depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState) # return score
            
            # get next agent and update depth when all the agents have been traversed
            next_agent = agent + 1
            if gameState.getNumAgents() == next_agent:
                next_agent = 0
                depth += 1
                
            # if the agent is Pacman, return maximum score for all legal action of the agent
            if agent == 0:
                return max(minimaxScore(next_agent, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent))
            
            # if the agent is the ghost, return minimum score for all legal action of the agent
            else:
                return min(minimaxScore(next_agent, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent))

        maximum_score = float("-inf")
        move = random.choice(gameState.getLegalActions(0))
        # iterate all the Pacman's legal actions
        for act in gameState.getLegalActions(0):
            score = minimaxScore(1, 0, gameState.getNextState(0, act))

            # update score and move when score > maximum score
            if score > maximum_score:
                maximum_score = score
                move = act
                
        return move
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
           The algorithm is similar to Minimax, but it uses two values, alpha (a) 
           and beta (b), as thresholds to determine if pruning is necessary. 
           
           Then, define an "alphabetaprune()" function that returns the score
           if the game ends or the defined depth is reached. The function should 
           maximize or minimize Pacman or ghosts, just like in Minimax. Additionally, 
           the function should use alpha (a) and beta (b) to determine if pruning is necessary.
           
           Finally, to perform the maximum action for the root (Pacman), traverse 
           through Pacman's legal moves and use "alphabetaprune()" during the process.
            
        """

        def alphabetaprune(agent, depth, gameState, a, b):
            # check whether game is ended or reaches the defined depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            # get next agent and update depth when all the agents have been traversed
            next_agent = agent + 1 
            if gameState.getNumAgents() == next_agent:
                next_agent = 0
                depth += 1
                    
            # if the agent is Pacman, find the maximum score for all legal action of the agent and prune the unnecessary branch
            if agent == 0:
                score = float("-inf")
                
                for act in gameState.getLegalActions(agent):
                    
                    # find the maximum score of Pacman
                    score = max(score, alphabetaprune(next_agent, depth, gameState.getNextState(agent, act), a, b))
                    
                    # prune the branch
                    if score > b:
                        return score
                    
                    # update alpha
                    a = max(a, score)
                    
                return score
            
            # if the agent is ghosts, find the minimum score for all legal action of the agent and prune the unnecessary branch
            else:
                score = float("inf")
                for act in gameState.getLegalActions(agent):
                    
                    # find minimum score of the ghost
                    score = min(score, alphabetaprune(next_agent, depth, gameState.getNextState(agent, act), a, b))
                    
                    # prune the branch
                    if score < a:
                        return score
                    
                    # update beta
                    b = min(b, score)
                    
                return score
        
        alpha = float("-inf")
        beta = float("inf")
        maximum_score = float("-inf")
        move = gameState.getLegalActions(0)[0]
        # iterate all the Pacman's legal actions
        for act in gameState.getLegalActions(0):
            
            score = alphabetaprune(1, 0, gameState.getNextState(0, act), alpha, beta)
            
            # update score and move when score > maximum score
            if score > maximum_score:
                maximum_score = score
                move = act

            # update alpha
            alpha = max(alpha, maximum_score)

        return move
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
            Similar to Minimax, define an "expectimax" function that returns the 
            score if the game ends or the defined depth is reached. The function 
            should maximize for Pacman when the "agent" is 0 but choose the branch 
            by expected score for ghosts (chance) when the "agent" is not 0.

            Finally, to perform the maximum action for the root (Pacman), traverse 
            through Pacman's legal moves and use "expectimax()" during the process.
            
        """
        def expectimax(agent, depth, gameState):
            # check whether game is ended or reaches the defined depth
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            # get next agent and update depth when all the agents have been traversed
            next_agent = agent + 1
            if gameState.getNumAgents() == next_agent:
                next_agent = 0
                depth += 1
            
            # if the agent is Pacman, return maximum score for all legal action of the agent 
            if agent == 0:
                return max(expectimax(next_agent, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent))
            
            # if the agent is ghost, return the expected score for all legal action of the agent 
            else: 
                return sum(expectimax(next_agent, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))

        maximum_score = float("-inf")
        move = gameState.getLegalActions(0)[0]
        # iterate all the Pacman's legal actions
        for act in gameState.getLegalActions(0):
            
            score = expectimax(1, 0, gameState.getNextState(0, act))
            
            # update score and move when score > maximum score
            if score > maximum_score:
                maximum_score = score
                move = act

        return move
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    This code defines an evaluation function for a Pacman game. 
    It calculates a score for the current game state based on several game 
    features, such as the current score, distance to the closest food, distance 
    to the closest active ghost, and distance to the closest scared ghost. The 
    function also takes into account the presence of capsules and the number of 
    remaining food pellets. The game features are combined using a weighted 
    linear combination to produce a final score. If Pacman loses the game, 
    the score returned is negative infinity. If Pacman wins the game, the score 
    returned is positive infinity.
    """    
    
    # if Pacman lose the game, return the score as negative infinity
    if currentGameState.isLose(): 
        return float("-inf")
    
    # if Pacman win the game, return the score as positive infinity
    elif currentGameState.isWin():
        return float("inf")
    
    score = currentGameState.getScore()
    
    pacman_pos = currentGameState.getPacmanPosition()
    ghost_positions = currentGameState.getGhostPositions()
    distance_to_closest_active_ghost = float("inf")
    distance_to_closest_scared_ghost = float("inf")
    flg_active_ghost_too_close = 0
    flg_scared_ghost_too_close = 0
    
    food_list = currentGameState.getFood().asList()
    food_count = len(food_list)
    distance_to_closest_food = float("inf")
    
    capsules_count = len(currentGameState.getCapsules())
    
    # find the closest food distance for all the food left on the board
    food_distances = [manhattanDistance(pacman_pos, food_position) for food_position in food_list]
    if food_count > 0:
        distance_to_closest_food = min(food_distances)

    # a function to compute distance between the ghost and Pacman
    def getManhattanDistances(ghosts): 
        return map(lambda g: util.manhattanDistance(pacman_pos, g.getPosition()), ghosts)

    # find all the scared ghosts and active ghost
    scared_ghosts, active_ghosts = [], []
    for ghost in currentGameState.getGhostStates():
        if not ghost.scaredTimer:
            active_ghosts.append(ghost)
        else: 
            scared_ghosts.append(ghost)
            
    # compute the distance to the closest active ghost
    if active_ghosts:
        distance_to_closest_active_ghost = min(getManhattanDistances(active_ghosts))
        
    # if active ghost is too close, set the flag to be 1
    if distance_to_closest_active_ghost < 2:
        flg_active_ghost_too_close = 1
    
    # comput the distance to the closest scared ghost
    if scared_ghosts:
        distance_to_closest_scared_ghost = min(getManhattanDistances(scared_ghosts))
        
    # if scared ghost is too close, set the flag to be 1
    if distance_to_closest_scared_ghost < 2:
        flg_scared_ghost_too_close = 1
    
    game_feature = [score,
                    distance_to_closest_food,
                    1.0 / distance_to_closest_active_ghost,
                    flg_active_ghost_too_close,
                    1.0 / distance_to_closest_scared_ghost,
                    flg_scared_ghost_too_close,
                    capsules_count,
                    food_count]
    
    weight = [1,
              -1.5,
              -2,
              -100,
              20,
              100,
              -20,
              -4]
    
    # compute the final score as the linear combination of game features
    final_score = 0
    for i in range(len(game_feature)):
        final_score += game_feature[i] * weight[i]
        
    return final_score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
