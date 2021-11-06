# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from typing import ByteString
from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import copy 



class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better

class ComputerPlayer:
       
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    # The following function returns the values for the get moves 

    def get_moves(self, quintris):
        #Call the successor function to get the best moves
        moves_current= self.successor_boards()
        return moves_current
        
    # The following function will return the value for the utility of the evaluated value for the given board and based on the utility function
    def evaluation_function(self,board,type_val):
        
        #No.of empty blocks:
        if type_val=="N_of_empty_blocks":
            return 25*15-sum([1 for i in board for a in i if a=="x"])

        # Weighted row coverage. Will try to fill the rows at the bottom first 
        elif type_val=="Weighted_row_coverage":
            val=0 
            for i in range(len(board)):
                val= val+ (25-i)* (sum([1 for i in board[i] if i=="x"])) 
                
            return val

        #Weighted_row_coverage_and_lessgaps : Will try to fill the bottom rows first and with less gaps
        elif type_val=="Weighted_row_coverage_and_lessgaps":
            val=0 
            for i in range(len(board)):
                val= val+ (25-i)* (sum([1 for i in board[i] if i=="x"])) 
                # val= val+ (25-i) *(sum([-1 for i in range(0,len(board[i])-1) if board[i]==board[i+1]]))

            gaps=0
            empties=[]
            for i in range(len(board)):
                if 'x' in board[i]:
                    for index,j in enumerate(board[i]):
                        if j== " ":
                            empties.append((i,index))
            if len(empties)>0:
                for each in empties:
                    if each[0]-1>=0 and each[0]-1<=24:
                        board[each[0]-1][each[1]]=="x"
                        gaps+=1

            height=0
            i=0
            while i< len(board[0]):
                for row in range(len(board)):
                    if board[row][i]=="x":
                        height+=row
                        break

                i=i+1

            height_gap=[]
            i=0
            while i< len(board[0]):
                for row in range(len(board)):
                    if board[row][i]=="x":
                        height_gap.append(row)
                        break
                i=i+1
            column_gap= sum([abs(height_gap[i+1] - height_gap[i]) for  i in range(len(height_gap)-1)])

            line_filled=0
            for each in board:
                x_count=sum([1 for i in each if i=="x"])
                if x_count==15:
                    line_filled+=1
                
            return val-10000*line_filled #+ 1000*gaps

            # +height+column_gap-10000*line_filled+val

        #Gaps: Will try to get a a board that has lowest number of gaps

        elif type_val=="less_gaps":
            gaps=0  
            empties=[]
            for i in range(len(board)):
                if 'x' in board[i]:
                    for index,j in enumerate(board[i]):
                        if j== " ":
                            empties.append((i,index))
            if len(empties)>0:
                for each in empties:
                    if each[0]-1>=0 and each[0]-1<=24:
                        board[each[0]-1][each[1]]=="x"
                        gaps+=1
            return gaps 
        #Heights: Will return the aggregate sum of all heights of all the columns in the board
         
        elif type_val=="heights":
            height=0
            i=0
            while i< len(board[0]):
                for row in range(len(board)):
                    if board[row][i]=="x":
                        height+=row
                        break
                i=i+1
            return height

        elif type_val=="column_gaps":
            height=[]
            i=0
            while i< len(board[0]):
                for row in range(len(board)):
                    if board[row][i]=="x":
                        height.append(row)
                        break
                i=i+1
            column_gap= sum([abs(height[i+1] - height[i]) for  i in range(len(height))-1])
            return height

    # The successor function will create all possible boards for the the given current piece and 
    # and the next piece.
    # In the worst case scenario, the branching factor is 120 fo a a depth of one. Since we are 
    # reaching a depth of two, the number of boards that are generated are 14,400 boards 
    def successor_boards(self):

        #Creating a list that has all possible position of the given piece
        #0 degree roated - Unflipped
        #0 degree roated - Horizontal flipped
        #90 degree roated - Unflipped
        #90 degree roated - Horizontal flipped
        #180 degree roated - Unflipped
        #180 degree roated - Horizontal flipped
        #270 degree roated - Unflipped
        #270 degree roated - Horizontal flipped

        # Once we get all combination of pieces after rotating and flipping,
        # we will then move the piece in the given board towards its left and right all the way upto the end of the board
        # and pull it down. 
        rotation=["0_N","0_H","90_N","90_H","180_N","180_H","270_N","270_H"]
        move_tracker={}
        # visited_boards=[]
        for rotate_angle in rotation:
            #Creating a copy of the board object so that we can use the methods of rotate and flip from backend codes provided by the Professor and without changing the original board
            quintris_game=copy.deepcopy(quintris)

            # For each possible position( by rotating and flipping) capture the relevant instructions in the rotate_move 
            if rotate_angle=="0_N":
                rotate_move=""

            elif rotate_angle=="0_H":
                rotate_move="h"
                quintris_game.hflip()

            elif rotate_angle=="90_N":
                rotate_move="n"
                quintris_game.rotate()


            elif rotate_angle=="90_H":
                rotate_move="hn"
                quintris_game.hflip()
                quintris_game.rotate()


            elif rotate_angle=="180_N":
                rotate_move="nn"
                quintris_game.rotate()
                quintris_game.rotate()

            elif rotate_angle=="180_H":
                rotate_move="hnn"
                quintris_game.hflip()
                quintris_game.rotate()
                quintris_game.rotate()

            elif rotate_angle=="270_N":
                rotate_move="nnn"
                quintris_game.rotate()
                quintris_game.rotate()
                quintris_game.rotate()

            elif rotate_angle=="270_H":
                rotate_move="hnnn"
                quintris_game.hflip()
                quintris_game.rotate()
                quintris_game.rotate()
                quintris_game.rotate()

            # Move pieces to the left (from the given position to the end of the board)
            for left in range(0,quintris_game.get_piece()[2]+1):
                quintris_game_copy= copy.deepcopy(quintris_game)
                temp_board=quintris_game_copy.get_board()
                
                left_tracker=[]
                for i in range(0,left):
                    quintris_game_copy.left()

                    left_tracker.append("b")
                try :
                    quintris_game_copy.down()
                except EndOfGame:
                    pass

                # For each of the pieces repeat the process that we have earlier get the board at a depth of two
                
                #--------------Start: Look Ahead 2nd piece for boards with left moved pieces-----
                rotate_move_next_left=rotate_move+"b"*len(left_tracker)

                rotation_next_left=["0_N","0_H","90_N","90_H","180_N","180_H","270_N","270_H"]
                
                for rotate_angle_left in rotation_next_left:
                    quintris_next_left= copy.deepcopy(quintris_game_copy)
                    if rotate_angle_left=="0_N":
                        rotate_move_left=""

                    elif rotate_angle_left=="0_H":
                        rotate_move_left="h"
                        quintris_next_left.hflip()

                    elif rotate_angle_left=="90_N":
                        rotate_move_left="n"
                        quintris_next_left.rotate()


                    elif rotate_angle_left=="90_H":
                        rotate_move_left="hn"
                        quintris_next_left.hflip()
                        quintris_next_left.rotate()


                    elif rotate_angle_left=="180_N":
                        rotate_move_left="nn"
                        quintris_next_left.rotate()
                        quintris_next_left.rotate()

                    elif rotate_angle_left=="180_H":
                        rotate_move_left="hnn"
                        quintris_next_left.hflip()
                        quintris_next_left.rotate()
                        quintris_next_left.rotate()

                    elif rotate_angle_left=="270_N":
                        rotate_move_left="nnn"
                        quintris_next_left.rotate()
                        quintris_next_left.rotate()
                        quintris_next_left.rotate()

                    elif rotate_angle_left=="270_H":
                        rotate_move_left="hnnn"
                        quintris_next_left.hflip()
                        quintris_next_left.rotate()
                        quintris_next_left.rotate()
                        quintris_next_left.rotate()
                    # Move pieces to the left - Depth 2
                    for next_left_left in range(0,quintris_next_left.get_piece()[2]):
                        quintris_next_left_left= copy.deepcopy(quintris_next_left)                                                
                        next_left_left_tracker=[]
                        # Track the moves
                        for i in range(0,next_left_left):
                            quintris_next_left_left.left()
                            next_left_left_tracker.append("b")    
                        try :
                            quintris_next_left_left.down()
                        except EndOfGame:
                            pass
                        
                        # Append the moves, board and the the value of of evaluation function 
                        move_tracker[rotate_move_next_left+"-_-"+rotate_move_left+"b"*len(next_left_left_tracker)] = (quintris_next_left_left.get_board(),self.evaluation_function(quintris_next_left_left.get_board(),"Weighted_row_coverage_and_lessgaps"))

                    ## Move pieces to the right - Depth 2    

                    for next_left_right in range(0,15-quintris_next_left.get_piece()[2]):
                        quintris_next_left_right= copy.deepcopy(quintris_next_left)                       
                        next_left_right_tracker=[]
                    # Track the moves 
                        for i in range(0,next_left_right):
                            quintris_next_left_right.right()
                            next_left_right_tracker.append("m")
                        try :
                            quintris_next_left_right.down()
                        except EndOfGame:
                            pass
                       
                        # Append the moves, board and the the value of of evaluation function 
                        move_tracker[rotate_move_next_left+"-_-"+rotate_move_left+"m"*len(next_left_right_tracker)] = (quintris_next_left_right.get_board(),self.evaluation_function(quintris_next_left_right.get_board(),"Weighted_row_coverage_and_lessgaps"))

                #--------------End: Look Ahead 2nd piece for boards with left moved pieces-----

                

               
            # Move pieces to the right
            for right in range(0,15-quintris_game.get_piece()[2]):
                quintris_game_copy= copy.deepcopy(quintris_game)                
                right_tracker=[]

                for i in range(0,right):
                    quintris_game_copy.right()
                    right_tracker.append("m")

                quintris_game_copy.down()

                ########Start - right pieces with next piece moved left amd right########
                rotate_move_next_right=rotate_move+"m"*len(right_tracker)

                rotation_next_right=["0_N","0_H","90_N","90_H","180_N","180_H","270_N","270_H"]
                
                for rotate_angle_right in rotation_next_right:
                    quintris_next_right= copy.deepcopy(quintris_game_copy)
                    if rotate_angle_right=="0_N":
                        rotate_move_right=""

                    elif rotate_angle_right=="0_H":
                        rotate_move_right="h"
                        quintris_next_right.hflip()

                    elif rotate_angle_right=="90_N":
                        rotate_move_right="n"
                        quintris_next_right.rotate()


                    elif rotate_angle_right=="90_H":
                        rotate_move_right="hn"
                        quintris_next_right.hflip()
                        quintris_next_right.rotate()


                    elif rotate_angle_right=="180_N":
                        rotate_move_right="nn"
                        quintris_next_right.rotate()
                        quintris_next_right.rotate()

                    elif rotate_angle_right=="180_H":
                        rotate_move_right="hnn"
                        quintris_next_right.hflip()
                        quintris_next_right.rotate()
                        quintris_next_right.rotate()

                    elif rotate_angle_right=="270_N":
                        rotate_move_right="nnn"
                        quintris_next_right.rotate()
                        quintris_next_right.rotate()
                        quintris_next_right.rotate()

                    elif rotate_angle_right=="270_H":
                        rotate_move_right="hnnn"
                        quintris_next_right.hflip()
                        quintris_next_right.rotate()
                        quintris_next_right.rotate()
                        quintris_next_right.rotate()

                    # Move pieces to the left - Depth 2
                    for next_right_left in range(0,quintris_next_right.get_piece()[2]):
                        quintris_next_right_left= copy.deepcopy(quintris_next_right)                        
                        next_right_left_tracker=[]

                        for i in range(0,next_right_left):
                            quintris_next_right_left.left()
                            next_right_left_tracker.append("b")
                        try :
                            quintris_next_right_left.down()
                        except EndOfGame:
                            pass
                        
                        move_tracker[rotate_move_next_right+"-_-"+rotate_move_right+"b"*len(next_right_left_tracker)] = (quintris_next_right_left.get_board(),self.evaluation_function(quintris_next_right_left.get_board(),"Weighted_row_coverage_and_lessgaps"))
                    
                    # Move pieces to the right - Depth 2
                    for next_right_right in range(0,15- quintris_next_right.get_piece()[2]):
                        quintris_next_right_right= copy.deepcopy(quintris_next_right)
                        next_right_right_tracker=[]

                        for i in range(0,next_right_right):
                            quintris_next_right_right.right()
                            next_right_right_tracker.append("m")
                        try :
                            quintris_next_right_right.down()
                        except EndOfGame:
                            pass
                        
                        move_tracker[rotate_move_next_right+"-_-"+rotate_move_right+"m"*len(next_right_right_tracker)] = (quintris_next_right_right.get_board(),self.evaluation_function(quintris_next_right_right.get_board(),"Weighted_row_coverage_and_lessgaps"))

                   
                ########End - right pieces with next piece moved left amd right##########

        #Get the first move for the boards generated by first and second moves         
        pos_moves=[x.split("-_-")[0] for x in move_tracker]
        #Get the utility values for the boards generated by first and second moves   
        eval_moves=[move_tracker[x][1]  for x in move_tracker]
        # Return the move that has the lowest evaluation value
        return pos_moves[eval_moves.index(min(eval_moves))]

    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            
            #Get the moves from the get_moves function 
            moves=self.get_moves(quintris)
        
            for move in moves:
                if move == "b":
                    quintris.left()
                elif move == "m":
                    quintris.right()
                elif move == "n":
                    quintris.rotate()
                elif move == "h":
                    quintris.hflip()
            quintris.down()

        
                
            
            # column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            # index = column_heights.index(max(column_heights))

            # if(index < quintris.col):
            #     quintris.left()
            # elif(index > quintris.col):
            #     quintris.right()
            # else:
            #     quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)
