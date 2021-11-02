# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys

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
#
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
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
#        print("*********************************This is where the code understanding snippet runs**************************************")
 #       print("The column of the the upper left block is ",quintris.col)
  #      print("The row of the upper left block is ",quintris.row)
   #     print("The current piece is ", quintris.get_piece())


        ### The following code will not work beacuse of the inplace operations
        # current_board= quintris.get_board() #### Store these values in current_board identifier as the operation we perfom here are in place operations
        # current_score= 0
        # current_piece= quintris.get_piece()
        # next_piece= quintris.get_next_piece()
        # print("The current board is the following :")
        # for i in current_board:
        #     print( i) 
        # print("The current score of the board is ",current_score)
        # moves_and_evaluation=self.successor_boards(quintris.get_piece(),current_board)
        # quintris.state=(current_board,current_score)
        # print("The board after I reassign it back again")
        # new_board=quintris.get_board()
        # for i in new_board:
        #     print( i)
        # new_current_piece= quintris.get_piece()
        # new_next_piece= quintris.get_next_piece()
         
         # Check whether the previus board and the new assigned board are equal or not
        # print("The value of equality for boards is ",current_board==new_board)
        # print("The value of equality for curret pieces", current_piece==new_current_piece)
        # print("The value of equality for next pieces", next_piece== new_next_piece)
         #   print("The value given by the evaluation function is ",self.evaluation_function(quintris.get_board(),"N_of_empty_blocks"))
      #  print("The next piece is ",quintris.get_next_piece())
       # board_for_print=quintris.get_board()
        #for i in board_for_print:
         #   print(i)
       # print(len(quintris.get_board()),"X", len(quintris.get_board()[0]))
       # print("***********************************This is where the code understanding snippets ends************************************")
        moves= self.successor_boards(quintris.get_piece(),quintris.get_board())
        
        return moves

    def evaluation_function(self,board,type_val):

        if type_val=="N_of_empty_blocks":
            return 25*15-sum([1 for i in board for a in i if a=="x"])

        elif type_val=="Weighted_row_coverage":
            val=0 
            for i in range(len(board)):
                val= val+ (25 -i) * sum([1 for i in board[i] if i=="x"])
            return val


    def get_x_positions(self, piece, val_col):
        if piece[0][0][0]=="x":
            val_col=val_col+0
        elif piece[0][0][1]=="x":
            val_col=val_col-1
        elif piece[0][0][2]=="x":
            val_col=val_col-2
        else:
            val_col=val_col-3
        x_positions=[[i,j+val_col] for i in range(len(piece[0])) for j in range(len(piece[0][0])) if piece[0][i][j]=="x"]
        return x_positions

    def legal_positions(self,x_positions,n_row,n_col):
         return sum([1 for x in x_positions if x[0]>=0 and x[0]<n_row and x[1]>=0 and x[1]<n_col]) == 5


    def successor_boards(self,piece,board):
        #print("Move the given piece to left by one block")
        #quintris.left()
        #quintris.down()
        # return "bd"+str(self.evaluation_function(quintris.get_board(),"N_of_empty_blocks"))
        moves={}

        # print("The piece at the beginnig is piece",piece)
        #Moves include given piece, rotated 90, rotated 180, rotated 270 and their flipped verisons(all rotations
        x_row= piece[1]
        x_col= piece[2]

        possible_left=list(range(0,x_col))
        possible_right=list(range(x_col+1,len(board[0])))
        possible_moves= possible_left+possible_right

        piece_copy=piece[0]
        rotated_90 = [ "".join([ str[i] for str in piece_copy[::-1] ]) for i in range(0, len(piece_copy[0])) ]
        rotated_pieces= { 0: ["",piece_copy], 90: ["n",rotated_90], 180: ["nn", [ str[::-1] for str in piece_copy[::-1] ]], 270: ["nnn",[ str[::-1] for str in rotated_90[::-1] ]] }

        # If the the given piece is symmetric across some axis then we will get duplicates, so lets take a move only that are unique
        # unique_pieces=[]
        # while len(rotated_pieces)>0:
        #     print("Pradeep")
        #     print(rotated_pieces)
        #     print("Unique pieces are ",unique_pieces)
        #     if len(rotated_pieces)>=2:
        #         keys=list(rotated_pieces.keys())
        #         for i in range(len(rotated_pieces)-1):
        #             for j in range(i+1,len(rotated_pieces)):
        #                 if rotated_pieces[keys[i]]==rotated_pieces[keys[j]]:
        #                     print("equality")
        #                     unique_pieces.append(rotated_pieces[i])
        #                     rotated_pieces.pop(keys[i])
        #                     keys.pop(i)
        #                     rotated_pieces.pop(keys[j-1])
        #                     keys.pop(j-1)
        #                     break
        #                 elif i==len(rotated_pieces)-2 and rotated_pieces[keys[0]] not in unique_pieces:
        #                     unique_pieces.append(rotated_pieces[keys[0]])
        #                     rotated_pieces.pop(keys[0])
        #                     keys.pop(0)
        #                 elif i==len(rotated_pieces)-2 and rotated_pieces[keys[0]] in unique_pieces:
        #                     rotated_pieces.pop(keys[0])
        #                     keys.pop(0)

        #     else:
        #         print("Pradeep in else")
        #         unique_pieces.append(rotated_pieces[keys[0]])
        #         rotated_pieces.pop(keys[0])

        # print("The rotated pieces and the unique pieces are the following")
        # for i in rotated_pieces:
        #     print("-------------")
        #     for j in rotated_pieces[i]:
        #         print(j)
        # print("___________________- unique pieces are teh followwing ")

        # for i in unique_pieces:
        #     print("-------------")
        #     for j in i:
        #         print(j)

        # # Adding the position and of row and column to the the unique pieces

        # for i in range(len(unique_pieces)):
        #     unique_pieces[i]= (unique_pieces[i],x_row,x_col)
        


        # print(possible_moves)

        n_row=len(board)
        n_col=len(board[0])

        # rotated_90 = [ "".join([ str[i] for str in piece[::-1] ]) for i in range(0, len(piece[0])) ]
        # rotated_pieces= { 0: piece, 90: rotated_90, 180: [ str[::-1] for str in piece[::-1] ], 270: [ str[::-1] for str in rotated_90[::-1] ] }

        # # If the the given piece is symmetric across then we may get duplicates, so lets take a move only that are unique
        # rotated_pieces_lst=list(rotated_pieces.values)
        # unique_pieces=[]
        # while rotated_pieces_lst:
        #     if len(rotated_pieces_lst)>=2:
        #         for i in range(len(rotated_pieces_lst)-1):
        #             if piece[i]==piece[i+1]:
        #                 unique_pieces.append(piece[i])
        #                 rotated_pieces_lst.pop(i)
        #                 rotated_pieces_lst.pop(i+1)
        #                 break
        #     else:
        #         unique_pieces.append(rotated_pieces_lst[0])
        #         rotated_pieces_lst.pop(0)

        # print("The rotated pieces and the unique pieces are the following")
        # for i in rotated_pieces:
        #     print("-------------")
        #     for j in rotated_pieces[i]:
        #         print(j)
        # print("___________________- unique pieces are teh followwing ")

        # for i in rotated_pieces_lst:
        #     print("-------------")
        #     for j in i:
        #         print(j)

        for each in rotated_pieces:
            piece=(rotated_pieces[each][1],x_row,x_col)
            if each ==0:
                rotate_moves=""
            else:
                rotate_moves="n"*(int(each/90))
            ## Try moving the piece to all possible left and right positions and then calculate the evaluation function
            for i in possible_moves:
                x_positions=self.get_x_positions(piece,i)
                # print(x_positions)
                legal_pos_flg=self.legal_positions(x_positions,n_row,n_col)
                # print(x_positions,legal_pos_flg)
                if legal_pos_flg and x_col-i>0:
                    moves[rotate_moves+"b"*(x_col-i)]=[x_positions,9999999]
                elif legal_pos_flg:
                    moves[rotate_moves+"m"*(i-x_col)]=[x_positions,9999999]
            # print(moves)

            # print(x_row, x_col, possible_left, possible_right)

        
            # piece_copy=piece
            # piece=piece[0]
            # ### Took the following code from the backend code
            

            # piece=piece_copy
            # Understanding the given piece
            # print("This information is related to the given piece")
            # print("The size of the given piece is ", len(piece[0]), " ", len(piece[0][0]))

            

            # Try moving piece down:
            for move in moves:
                x_positions=moves[move][0].copy()
                temp_board=board.copy()

                for i in range(len(temp_board)):
                # print("I love EAI class because of the ----",i)
                    val=0
                    flag=0
                    val= sum([1 for j in x_positions if  temp_board[j[0]][j[1]]=="x"])

                    if val>0:      
                        for i in range( len(x_positions)):
                            x_positions[i][0]=x_positions[i][0]-1
                        break

                    else:
                        for i  in range(len( x_positions)):
                            row_index=[i[0]   for i in x_positions]
                            if max(row_index)<24:
                                x_positions[i][0]=x_positions[i][0]+1
                            else:
                                flag=1
                    if flag==1:
                        break                    
                # print(x_positions)
                # print("Board before assignment")
                # for i in temp_board:
                #     print(i+"|||||")
                for i in x_positions:
                    temp_board[i[0]]= temp_board[i[0]][0:i[1]]+"x"+temp_board[i[0]][i[1]+1:]
                # print("Board after assignment")
                # for i in temp_board:
                #     print(i+"|||||")

                board_val_by_evaluation_function=self.evaluation_function(temp_board,"Weighted_row_coverage")
                moves[move][1]=board_val_by_evaluation_function
                # print("The value given by the evaluation function is ", board_val_by_evaluation_function)
        # print(moves)

        # print("Pradeep")
        # print("Successors are the  following:")
       # print(piece)
        # piece=piece[0]
        # ### Took the following code from the backend code 
        # rotated_90 = [ "".join([ str[i] for str in piece[::-1] ]) for i in range(0, len(piece[0])) ]
        # rotated_pieces= { 0: piece, 90: rotated_90, 180: [ str[::-1] for str in piece[::-1] ], 270: [ str[::-1] for str in rotated_90[::-1] ] }
        # for i in rotated_pieces:
        #     print("-------------")
        #     for j in rotated_pieces[i]:
        #         print(j)
        ## From here it is our own code
    #    print(piece)
    #    print(board)

        pos_moves=[x for x in moves]
        eval_moves=[moves[x][1]  for x in moves]
        return pos_moves[eval_moves.index(min(eval_moves))]
        # return "bd"+str(self.evaluation_function(quintris.get_board(),"N_of_empty_blocks"))

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #what
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            ### remove the following code
            print("The length of the board is", len(board))
            ########
            
            
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


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



