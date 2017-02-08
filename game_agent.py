"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import sample_players
from random import randint

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    curr_moves = game.move_count
    opp_moves = 0.0 # game.forecast_move(game.get_player_location(player)).move_count
    return float(curr_moves - opp_moves)
    #raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=100.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        print('get_move legal moves: %s' % legal_moves)
        if(len(legal_moves)==0):
            return (-1,-1)
        if(game.move_count <=1):
            return game.get_player_location(self)
        move = legal_moves[randint(0, len(legal_moves) - 1)]
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            
            if(self.iterative): #IDS
                depth = 1
                while(self.time_left):
                    if(self.method == 'minimax'):
                        _,move = self.minimax(game,depth)
                    elif(self.method == 'alphabeta'):
                        _,move = self.alphabeta(game, depth)
                    depth +=1
                #game.apply_move(move)
            else: #DFS
                if(self.method == 'minimax'):
                    _,move = self.minimax(game,self.search_depth)
                elif(self.method == 'alphabeta'):
                    _,move = self.alphabeta(game, self.search_depth)
                #game.apply_move(move)
                
            return move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            #game.apply_move(move)
            return move

        # Return the best move from the last completed search iteration
        #raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing player (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        list_moves = game.get_legal_moves()
        
        if self.time_left() < self.TIMER_THRESHOLD:
            return self.score(game, self),list_moves[0]
        
        # TODO: finish this function!
        if(depth == 0 or len(list_moves)==0):
            return self.score(game,self),(-1,-1)
        best_move = list_moves[0]
        best_score = 0.0
        if(maximizing_player):
            best_score = float('-inf')
            for a in list_moves:
                clone = game.forecast_move(a)

                score,move = self.minimax(clone, depth-1,False)
                if(score >= best_score):
                    best_move = a
                    best_score = score
            return best_score,best_move
        else:
            best_score = float('inf')
            for a in list_moves:
                clone = game.forecast_move(a)

                score,move = self.minimax(clone, depth-1,True) 
                if(score < best_score):
                    best_move = a
                    best_score = score
            return best_score,best_move
        return best_score,best_move
        #raise NotImplementedError

  
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        list_moves = game.get_legal_moves()
        if self.time_left() < self.TIMER_THRESHOLD:
            return self.score(game, self),(-1,-1)
        
        

        if(depth == 0 or len(list_moves)==0):
            print('depth 0 loop for %s at depth: %s' % (len(list_moves),list_moves))
            return self.score(game,self),(-1,-1)
        best_move = list_moves[0]
        #print(list_moves)
        best_score = 0.0
        #print(self.time_left())
        
        if(maximizing_player):
            best_score = float('-inf')
            
            for a in list_moves:
                clone = game.forecast_move(a)
                #clone_legal_moves = clone.get_legal_moves(self)
                
                score,move = self.alphabeta(clone, depth -1, alpha, beta, False)
                print('max for loop %s for move %s' % (score,move))
                alpha = max(alpha,score)
                if(best_score < score):
                    best_move = a
                    best_score = score
                if(score>= beta):
                    return score,a
                alpha= max(alpha,score)    
            return best_score,best_move
        else:
            best_score = float('inf')
            for a in list_moves:
                clone = game.forecast_move(a)
                score,move = self.alphabeta(clone, depth -1, alpha, beta, True)
                print('min for loop %s for move %s' % (score,move))
                beta = min(beta,score)
                if(score <= best_score):
                    best_move = a
                    best_score = score 
                if(score <=alpha):
                    return score,a
                beta = min(beta,score)
            return best_score,best_move
