#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import numpy as np

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def board_to_grid(board, N):
    return np.array(list(board)).reshape(N, N)

def move_on_board(pos, N):
    return 0 <= pos[0] < N and 0<= pos[1] < N

def possible_pichu_moves(board, player):
    pichu_boards = []
    
    player = player
    all_player_moves = []
    num_jump_moves = 0

    
    #set player variables
    if player == 'w':
        forward, backward, last_row  = 1, -1, N-1
        pichu, pikachu, raichu = 'w', 'W', '@'
        opp_pichu, opp_pikachu, opp_raichu = 'b', 'B', '$'

    if player == 'b':
        forward, backward, last_row  = -1, 1, 0
        pichu, pikachu, raichu = 'b', 'B', '$'
        opp_pichu, opp_pikachu, opp_raichu = 'w', 'W', '@'

    #find player pichus
    row, col = np.where(board == pichu )
    all_pichus = np.column_stack((row,col))

    for pichu_pos in all_pichus:
        # check one diagonal ahead in each direction
        diag_1_l = np.array([forward*1,1])
        diag_1_r = np.array([forward*1,-1])
        diag_1 = np.vstack([np.add(pichu_pos, diag_1_l),
                            np.add(pichu_pos, diag_1_r)])
        diag_1_moves = [tuple(move) for move in diag_1]

        # if space one diagional ahead is empty, add to possible moves list
        to_empty_space = []
        for move in diag_1_moves:
            if move_on_board(move, N) and board[move]=='.':
                to_empty_space=move

                # add board configs for possible moves
                new_board = board.copy()        
                new_board[tuple(pichu_pos)]='.'

                new_row = move[0]
                if new_row == last_row:
                    new_board[move]=raichu
                else:
                    new_board[move]=pichu

                pichu_boards.append(new_board)

        #check two diagonal spaces ahead
        diag_2_l = np.array([forward*2,2])
        diag_2_r = np.array([forward*2,-2])
        diag_2 = np.vstack([np.add(pichu_pos, diag_2_l),
                            np.add(pichu_pos, diag_2_r)])
        diag_1_2 = np.concatenate((diag_1, diag_2), axis = 1).reshape(-1, 2,2)
        diag_1_2_moves = [[tuple(move[0]), tuple(move[1])] for move in diag_1_2]

        #if pichu can jump over opp pichu to an empty space, add to possible moves list

        for move in diag_1_2_moves:
            if move_on_board(move[1], N):
                jump_avail = board[move[0]]+board[move[1]]==opp_pichu+'.'

                if jump_avail:
                    pichu_jump =move[1]
                    new_board = board.copy()        
                    new_board[tuple(pichu_pos)]='.'
                    new_board[move[0]]='.'

                    new_row = pichu_jump[0]
                    if new_row == last_row:
                        new_board[pichu_jump]=raichu
                    else:
                        new_board[pichu_jump]=pichu

                    pichu_boards.append(new_board)
                    num_jump_moves += 1
    

    return pichu_boards, num_jump_moves

def possible_pikachu_moves(board, player):
    pikachu_boards = []
    
    player = player
    all_player_moves = []

    num_jump_moves = 0

    
    #set player variables
    if player == 'w':
        forward, backward, last_row  = 1, -1, N-1
        pichu, pikachu, raichu = 'w', 'W', '@'
        opp_pichu, opp_pikachu, opp_raichu = 'b', 'B', '$'

    if player == 'b':
        forward, backward, last_row  = -1, 1, 0
        pichu, pikachu, raichu = 'b', 'B', '$'
        opp_pichu, opp_pikachu, opp_raichu = 'w', 'W', '@'
    
    #find player pikachus
    row, col = np.where(board == pikachu)
    all_pikachus = np.column_stack((row, col))

    all_moves = []
    move_range = 3
    forward_moves = [(x*forward,0) for x in range(1,move_range+1)]
    right_moves = [(0,x) for x in range(1, move_range+1)]
    left_moves = [(0,x*-1) for x in range(1, move_range+1)]
    all_moves.append(forward_moves)
    all_moves.append(right_moves)
    all_moves.append(left_moves)


   
    # pikachu moves to empty spaces
    
    moves_1_2 = []
    moves_1_2.append(forward_moves[:2])
    moves_1_2.append(left_moves[:2])
    moves_1_2.append(right_moves[:2])
    
    pos_1_2 = []
    for n in range(len(all_pikachus)):
        pos = np.add(all_pikachus[n], moves_1_2)        
        pos_1_2.append([[tuple(x) for x in pos[n]] for n in range(len(moves_1_2))])


    for i, pikachu_pos in enumerate(pos_1_2):
        current_pikachu = tuple(all_pikachus[i])
        for direction in pikachu_pos:
            path = []
            for move in direction:
                if move_on_board(move, N):
                    path.append(move)
            board_view =[board[path[n]] for n in range(len(path))]
            for j , step in enumerate(board_view):
                if step =='.':
                    new_board = board.copy()        
                    new_board[current_pikachu]='.'

                    new_row = path[j][0]
                    if new_row == last_row:
                        new_board[path[j]]=raichu
                    else:
                        new_board[path[j]]=pikachu
                    pikachu_boards.append(new_board)
                else:
                    break


    pos_1_2_3 = []
    for n in range(len(all_pikachus)):
        pos = np.add(all_pikachus[n], all_moves)        
        pos_1_2_3.append([[tuple(x) for x in pos[n]] for n in range(len(all_moves))])


    # pikachu jumps to empty space
    for i, pikachu_pos in enumerate(pos_1_2_3):
        current_pikachu = tuple(all_pikachus[i])
        for direction in pikachu_pos:
            path = []
            for move in direction:
                if move_on_board(move, N):
                    path.append(move)
            board_view =[board[path[n]] for n in range(len(path))]

            try:
                if board_view[0] in opp_pichu+opp_pikachu and board_view[1] =='.':
                    new_board = board.copy()        
                    new_board[current_pikachu]='.'
                    new_board[path[0]]='.'

                    new_row = path[1][0]
                    if new_row == last_row:
                        new_board[path[1]]=raichu
                    else:
                        new_board[path[1]]=pikachu
                    pikachu_boards.append(new_board)
                    num_jump_moves += 1
            except:
                pass

            try:
                if board_view[0] in opp_pichu+opp_pikachu and board_view[1]=='.' and board_view[2]=='.':
                    new_board = board.copy()        
                    new_board[current_pikachu]='.'
                    new_board[path[0]]='.'

                    new_row = path[2][0]
                    if new_row == last_row:
                        new_board[path[2]]=raichu
                    else:
                        new_board[path[2]]=pikachu
                    pikachu_boards.append(new_board)
                    num_jump_moves += 1
            except:
                pass

            try:
                if board_view[0] == '.' and board_view[1] in opp_pichu+opp_pikachu and board_view[2]=='.':
                    new_board = board.copy()        
                    new_board[current_pikachu]='.'
                    new_board[path[1]]='.'

                    new_row = path[2][0]
                    if new_row == last_row:
                        new_board[path[2]]=raichu
                    else:
                        new_board[path[2]]=pikachu
                    pikachu_boards.append(new_board)
                    num_jump_moves +=1
            except:
                pass

    return pikachu_boards, num_jump_moves
        


def possible_raichu_moves(board, player):
    raichu_boards = []
    
    player = player
    all_player_moves = []

    num_jump_moves = 0

    #set player variables
    if player == 'w':
        forward, backward, last_row  = 1, -1, N-1
        pichu, pikachu, raichu = 'w', 'W', '@'
        opp_pichu, opp_pikachu, opp_raichu = 'b', 'B', '$'

    if player == 'b':
        forward, backward, last_row  = -1, 1, 0
        pichu, pikachu, raichu = 'b', 'B', '$'
        opp_pichu, opp_pikachu, opp_raichu = 'w', 'W', '@'
    
    #find player raichus
    row, col = np.where(board == raichu)
    all_raichus = np.column_stack((row, col))


    all_moves = []
    move_range = N
    forward_moves = [(x*forward,0) for x in range(1,move_range)]
    backward_moves=[(x*backward, 0) for x in range(1, move_range)]
    right_moves = [(0,x) for x in range(1, move_range)]
    left_moves = [(0,x*-1) for x in range(1, move_range)]
    diag_II = [(x*forward, x) for x in range(1, move_range)]
    diag_I = [(x*backward, x) for x in range(1, move_range)]
    diag_III = [(x*backward, x*-1) for x in range(1, move_range)]
    diag_IV = [(x*forward, x*-1) for x in range(1, move_range)]
    all_moves.append(forward_moves)
    all_moves.append(backward_moves)
    all_moves.append(right_moves)
    all_moves.append(left_moves)
    all_moves.append(diag_I)
    all_moves.append(diag_II)
    all_moves.append(diag_III)
    all_moves.append(diag_IV)


    all_pos = []
    for raichu_pos in all_raichus:
        pos = np.add(raichu_pos, all_moves)
        all_pos.append([[tuple(x) for x in pos[n]] for n in range(len(all_moves))])


    # raichu moves to empty spaces
    for i, raichu_pos in enumerate(all_pos):
        current_raichu = tuple(all_raichus[i])
        for direction in raichu_pos:
            path = []
            for move in direction:
                if move_on_board(move, N):
                    path.append(move)
            board_view =[board[path[n]] for n in range(len(path))]
            for j , step in enumerate(board_view):
                if step =='.':
                    new_board = board.copy()        
                    new_board[current_raichu]='.'
                    new_board[path[j]]=raichu
                    raichu_boards.append(new_board)
                else:
                    break


    # pikachu jumps to empty space
    for i, raichu_pos in enumerate(all_pos):
        current_raichu = tuple(all_raichus[i])
        for direction in raichu_pos:
            path = []
            for move in direction:
                if move_on_board(move, N):
                    path.append(move)
            board_view =[board[path[n]] for n in range(len(path))]


            for step in board_view:
                if step in opp_pichu+opp_pikachu+opp_raichu:
                    first_opp = board_view.index(step)
                    before_first_opp = board_view[:first_opp]
                    empty_before = all([x == '.' for x in before_first_opp])
                    if not empty_before:
                        break
                    else:
                        after = board_view[first_opp:]
                        if len(after)==1:
                            break
                        else:
                            for n, step in enumerate(after[1:],1):
                                if step == '.':
                                    new_board = board.copy()        
                                    new_board[current_raichu]='.'
                                    new_board[path[first_opp]]='.'
                                    new_board[path[first_opp+n]]=raichu
                                    raichu_boards.append(new_board)
                                    num_jump_moves += 1
                                else:
                                    break
                        break
                
    return raichu_boards, num_jump_moves

def successors(board, player):
    
    all_player_moves = []
       
    all_player_moves.append(possible_pichu_moves(board, player)[0])
    all_player_moves.append(possible_pikachu_moves(board, player)[0])
    all_player_moves.append(possible_raichu_moves(board, player)[0])
    all_player_moves = [board for piece in all_player_moves for board in piece]
    
    return all_player_moves


def tree_1_2(board, player):

    # set players
    player = player
    if player == 'w':
        opp_player = 'b'
    if player =='b':
        opp_player ='w'


    tree = [] # (depth, nodes by parent)

    # place initial_board at root node 
    #(board, depth, parent_idx)
    d = 0
    tree.append([[board, d, 'na', float('-inf')]])

    d = 1
    #whose turn is it?
    if d % 2 == 1:
        who_moves = player
    else:
        who_moves = opp_player

    #add successors to tree
    parent_boards = [node[0] for node in tree[d-1]]

    d_nodes = []
    for n, parent_board in enumerate(parent_boards):
        d_nodes.append([[succ, d, n, float('inf')] for succ in successors(parent_board, who_moves)])
    tree.append(d_nodes)

    return tree

def is_terminal_state(board, player):
    # count number of pieces each player had on the board
    
    if player == 'w':
        max_player = 'w'
        min_player = 'b'
    
    if player == 'b':
        max_player = 'b'
        min_plyaer = 'w'
    
    if max_player == 'w':
        max_pieces='wW@'
        min_pieces = 'bB$'
    
    if max_player == 'b':
        max_pieces = 'bB$'
        min_pieces = 'wW@'
    

    unique, counts = np.unique(board, return_counts = True)
    pieces_on_board = dict(zip(unique, counts))
    
    max_total = 0
    for piece in max_pieces:
        try:
            max_total+=pieces_on_board[piece]
        except:
            continue

    min_total = 0
    for piece in min_pieces:
        try:
            min_total += pieces_on_board[piece]
        except:
            continue
    return (max_total == 0  or min_total ==0, min_total, max_total)

def win_in_avail_moves(tree):
#check leaf nodes for terminal states

    player_wins = []
    leaf_idx = len(tree)-1
    for i, group in enumerate(tree[leaf_idx]):
        for j, node in enumerate(group):
            check_terminal = is_terminal_state(node[0], player)
            if check_terminal[0] and check_terminal[1]==0:
                win_board = tree[leaf_idx][i][j][0].flatten()
                return True, ''.join([str(x) for x in win_board])
    return False, ''
    

def add_to_tree(tree, d, player, opp_player):
    
    if d % 2 ==0:
        max_node = True
        alpha_beta = float('-inf')
        who_moves = opp_player
    else:
        max_node = False
        alpha_beta = float('inf')
        who_moves = player

    d_nodes = []
    for group in tree[d-1]:
        for n, board in enumerate([x[0] for x in group]):
            d_nodes.append([[succ, d, n, alpha_beta]for succ in successors(board, who_moves)])
    tree.append(d_nodes)


    return tree

def weighted_pieces(board, player):

    if player == 'w':
        max_player = 'w'
        min_player = 'b'

    if player == 'b':
        max_player = 'b'
        min_player = 'w'

    if max_player == 'w':
        max_pieces='wW@'
        min_pieces = 'bB$'

    if max_player == 'b':
        max_pieces = 'bB$'
        min_pieces = 'wW@'


    unique, counts = np.unique(board, return_counts = True)
    pieces_on_board = dict(zip(unique, counts))
    
    max_weighted_pieces = 0
    weights = [10,20,50]

    for i, piece in enumerate(max_pieces):
        try:
            max_weighted_pieces += weights[i]*pieces_on_board[piece]
        except:
            continue

    min_weighted_pieces = 0
    weights = [10,20,50]

    for i, piece in enumerate(min_pieces):
        try:
            min_weighted_pieces += weights[i]*pieces_on_board[piece]
        except:
            continue

    return max_weighted_pieces-min_weighted_pieces


def jump_moves_avail(board, player):
    
    jump_moves = []
       
    jump_moves.append(possible_pichu_moves(board, player)[1])
    jump_moves.append(possible_pikachu_moves(board, player)[1])
    jump_moves.append(possible_raichu_moves(board, player)[1])
    
    return sum(jump_moves)

def pi_pik_travel(board, player):
    player = player
    if player == 'w':
        pichu = 'w'
        pikachu = 'W'

    if player == 'b':
        pichu = 'b'
        pikachu = 'B'

    row, col = np.where(((board == pichu) | (board == pikachu)))
    row
    if len(row)>0:

        if player == 'b':
            squared_dist = [(N-1-x)**2 for x in row]

        if player == 'w':
            squared_dist = [x**2 for x in row]

        return np.mean(squared_dist)
    else:
        return 0

def evaluation_func(board, player, opp_player):
    weights = [7, 5, 1]
    features = np.array([weighted_pieces(board, player),
                        jump_moves_avail(board, player)-jump_moves_avail(board, opp_player),
                        pi_pik_travel(board, player)-pi_pik_travel(board,opp_player)])
    
    return sum(features*weights)


###  given (N, player (w or b), board, timelimit (sec)) return the next best move for the player
def find_best_move(board, N, player, timelimit):
    choice_str = board

    while True:
        time.sleep(1)
        yield choice_str

        # set players
        player = player
        if player == 'w':
            opp_player = 'b'
        if player =='b':
            opp_player ='w'
        
        board = board_to_grid(board, N)

        # first two layers of tree
        tree = tree_1_2(board, player)

        # check if there is a winning move availalbe
        win = win_in_avail_moves(tree)
        if win[0]:
            choice_str = win[1]
            print (choice_str)
            return choice_str
            
            
        else:
            d = len(tree)-1
            for i, group in enumerate(tree[d]):
                group_max = [float('-inf'),i,'']
                for j, node in enumerate(group):
                    node[3]=(evaluation_func(node[0], player, opp_player))
                    if node[3]> group_max[0]:
                        group_max = [node[3],i,j]

            choice = tree[d][group_max[1]][group_max[2]][0]
            choice_str = ''.join([str(x) for x in choice.flatten()])

            #if no winning moves are available, build the game tree to horizon
            # current depth of tree (root is 0)
            d = len(tree)-1

            #depth of next layer of tree (root is 0)
            d = len(tree)
            # number of levels to add to tree
            horizon = 1

            for i in range(horizon):
                add_to_tree(tree,d, player, opp_player)
                d+=1
            

            #minimize
            # calculate evaluation function for each leaf nodes
            d = len(tree)-1
            evaluations = []
            for i, group in enumerate(tree[d]):
                group_min = [float('inf'),i,'']
                for j, node in enumerate(group):
                    node[3]=(evaluation_func(node[0], player, opp_player))
                    if node[3]< group_min[0]:
                        group_min = [node[3],i,j]
                evaluations.append(group_min)

            # find index of max of min values
            max_of_mins = [x[0] for x in evaluations].index(max([x[0] for x in evaluations]))

            #board for max of mins
            choice = tree[1][0][max_of_mins][0]
            choice_str = ''.join([str(x) for x in choice.flatten()])



if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
