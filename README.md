## Problem 1

### Description of how you formulated the problem
This is an adversarial search problem where a minimax algorithm can be applied.  There are two players taking turns playing a completely observable zero sum game. The player that starts first is the ‘max’ player and will pick the highest possible utility value from a choice of moves.  The player that goes second is the ‘min’ player.  The ‘min’ player will choose the minimum possible utility value from the choices given.  In this way, both players are playing optimally for themselves with is the least optimal for his or her opponent

### Abstraction:
* Initial state:  some random state of the board from which the max player will make a move
* State space:  all possible board configurations
* Successor function: all next possible board configurations that follow the rules for moves from the current state
* Terminal state:  any state where one player has won, i.e., there is only pieces of one color on the board, or a state where neither player can win, i.e. game ends in a draw
* Cost: edge weights are considered uniform, but each state is assessed a value of favorability for the max player and compared against possible states when deciding which move is optimal.
* The objective is to find a path from the initial state to a terminal state where ‘max’ wins or at least reaches the most favorable if a terminal state cannot be reached.


### Minimax Algorithm and Alpha-Beta pruning
Minimax uses depth first search to find the next move that will lead to an optimal outcome.  How deep the search can travel depends on the branching factor of the game.  In this case, the branching factor (successors generated by a given state) can be very high ~ 40.  So searching an exhaustive game tree where all possible terminal states are found is not feasible.  Instead the algorithm can be applied to a depth limited search to return an optimal move looking a small number of moves ahead.  Given some horizon, the leaf nodes of the game tree at the horizon are evaluated and assigned a value based on how favorable that state is for the max player to win the game from that state.  Those values are propagated back up the tree alternating between min and max nodes representing the ‘max’ player choosing the highest value and the ‘min’ player choosing the lowest value.  The evaluation function should be a high positive number for a state favorable to the ‘max’ player and a strong negative number for a state favorable to the ‘min’ player and 0 for a neutral board.  
In addition to limiting the depth of the search, alpha-beta pruning can also be used to increase the efficiency of the search to a limited horizon.  Alpha-beta pruning eliminates searching nodes that have no effect on the optimal choice.  Search below a node that will never be picked is discontinued.  This allows the optimal search to be returned faster and/or allow searching a deeper tree.

### Description of how your program works
Given a board setup and player:
* assign player as max player
* build a game tree to depth of 2  

Find all possible next moves for the max player and see if any of those are terminal states where the ‘max’ player wins.  If so, return that move. If there are no winning moves available, add a depth layer to the game tree and look 2 moves ahead.  
Calculate evaluation function for each leaf node.  Since the leaf nodes are the children of a max node, pick the maximum value of the leaf nodes to propagate up to their respective parent nodes.  Then choose the minimum of the values of the next depth layer up and propagate up to their respective parent nodes.  Then choose the maximum of these propagated values as the optimal move for the max player.  

Data structures
* For ease of reading and moving pieces, board configurations are stored and manipulated as 2D numpy arrays.  
* The tree data is stored in a nested list where the length of the list is the depth of the tree.  Each list representing a depth of the tree is composed of a list of lists that are the successors of each parent node.  For example.  If the root node tree[0] has 23 successors, the length of tree[1] is 1 signifying all the states in tree[1] came from the one state in tree[0].  The list contained inside that list has length of 23 for each of the 23 successors generated by the parent node.  Given this, evaluation function values can be propagated up to the parent node from a child node using the indexes of elements located in lists and sublists.

### Discussion 
As stated earlier, the high branching factor and limited amount of time available to come up with a move means either exhaustively searching a tree with a short horizon, or applying a alpha-beta pruning to be able to search a deeper tree.  The deeper the search, the more likely the optimal choice returned would lead to a win for the ‘max’ player.  However after trying and failing to implement alpha-beta pruning, options for improving performance in game play is the construction of the evaluation function.  
The evaluation function is made up of three components: 
* difference of weighted sum of pieces on the board where pichus, pikachus, and raichus are weighted 1, 2, and 10 respectively.  
* difference of jump moves available to each player
* difference of the mean of the squared distance traveled by pichus and pikachus  

After observing the game played against the random AI and other students’ AIs, these three factors are then weighted depending on the state of the board.
* Initially, when there are no raichus on the board, a slight priority is given to the weighted sum of pieces differential, followed by advancing pichus and pikachus down the board to turn into raichus.
* Once the max player has a raichu, taking opponent pieces is prioritized highly over other factors.
* If there becomes a high differential between weight sum of pieces (max player is the equivalent of over 2 raichus ahead), priority is given to advancing pichus/pikachus to turn into raichus
* Lastly, if the ‘max’ player is the equivalent of 3 raichus ahead, the priority is returned to taking opponent pieces to try to finish the game  
Given the short horizon of the search tree, the evaluation function described above was able to generate moves that could win or play to a draw against other AI players.

**Part - 2: The Game of Quintris:-**

**Understanding the given problem:-**

Although we all know the game of Tetris, implementing Quintris was still quite difficult and frustrating. The requirements were straightforward. We had to try and completely fill as many rows on the board with pieces as possible. It would be ideal to keep filling rows that get taken out of the board and maximize our score indefinitely. At any given point, we know the current piece structure along with the coordinate of the point through which the piece is entering into the board. Along with this, we also know the structure of the next piece. So this gives us two straightforward options for a solution discussed in the next section.

**Possible solutions:-**

Since we know the next piece also during a current move, we could utilize that to make an informed decision on where to place the current piece. Another approach is of course just finding the best move (using some heuristics or evaluation functions) according to just the current piece.

Since the pieces have a distribution in their occurrence, we could also implement expectimax for an additional lookahead piece apart from the immediate one. Everytime we get a piece, we can update it&#39;s occurrence probability by incrementing it&#39;s numerator and incrementing the denominator for all the other pieces as well as this one. Using this probability we can also predict what will be the 3rd piece in the pipeline. Here the depth is 3 with expectimax. Without it, it&#39;s obviously 2 since we will be looking at just the current and the next piece.

In our code, you&#39;ll be able to find depth limited search implemented with the depth limit as 2, i.e, our current move only depends on the current piece and the next piece.

**More about our code (it&#39;s huge) and it&#39;s results:-**

In our implementation, we first concentrated on the &quot;simple&quot; rather than the &quot;animated&quot; game. Once we had implemented the game for the &quot;simple&quot; mode, it wasn&#39;t that hard to implement it for the &quot;animated&quot; mode.

To be honest, we initially ended up spending more time on creating our own functions to obtain coordinates of all the &quot;x&quot;s in the piece, to generate different variations of the pieces by rotating it and then some more code to pull the pieces down to the board. The fact that the code wouldn&#39;t run on windows did not help with the lack of time we had during the midterm week. Running it on silo was also a bit cumbersome due to frequent disconnections. After the first few days, we had to use a Linux VM on VMware Workstation to speed things up. We then resorted to using the functions in the backend code to move around and rotate the pieces in order to generate the succeeding boards from a current point.

We first implemented the approach where we only consider the current piece. We applied 5 evaluation functions and we were able to generate a non-zero score upto 10. We then added the next piece also into the equation. We did this by first rotating and flipping the current piece, generating all possible boards by moving each of those variations to left or right and then taking each of these boards and combining it with variations of the next piece. This resulted in a branching factor of 120.

Unfortunately, the scores only went as high as 37. (could go higher upon more runs)

![](https://github.iu.edu/cs-b551-fa2021/jzayatz-prokkam-harmohan-a2/blob/master/highscore37.jpeg)

**Evaluation Functions:-**

Reference- https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/

While researching evaluation functions, we came across the above source from where we implemented the number of gaps, summation of height of every column, difference in adjacent column heights to get the bumps in the board and also the number of lines filled in a board. Apart from these, we also implemented our own evaluation function which is a weighted row coverage that assigns a higher score to a board if it has its pieces scattered across rather than all of them being mostly placed on a single row. We then take the minimum of this as the best move for the current piece. We tried different combinations of the evaluation functions and we set the sign for each by determining whether to maximize it or minimize it.
With the combination of our own evaluation function and the lines filled evaluation function, we were able to get a score of 37 and we would always get a score that is atleast higher than 5. 

**What could have possibly gone wrong? :-**

While deciding on implementations, we had two further sub-options while adding the next piece into the equation. One is calculating the move for the current piece as well as the next piece every single iteration and returning only the move for the current piece and forgetting about the move generated for the next piece. The other sub-option was to only compute the move for the next piece every iteration and use the move for the current piece from the previous iteration. We found that the scores did not improve after going through with the first sub-option. This is because the optimal move relationship between the first and the subsequent pieces is lost when we recompute the move for the current piece every iteration. Other problems that this resulted in was also a higher time complexity. Another reason for a high time complexity was duplicate boards generated due to rotation/ flipping of symmetrical pieces. Another observation we made was that although our code was able to play the game and take the score to as high as 17, the final board would seem like there were still some space for more pieces to be placed which could have inturn improved our score. Additionally, we noticed that our code played the game such a way that it would always fail to fill a row because of just one or two gaps in between and when we would inturn try to incorporate the gaps evaluation function, the code ended up placing pieces on top of already existing pieces resulting in higher value of height for every column and the game ends sooner. It seems like a trade of an the right weights for them could have helped solve this issue.

**Scope for a better solution:-**

We could implement sub-option 2 that was discussed above to get a better performance in scores. In order to decrease time complexity we could also try to remove the duplicated pieces. A better combinations of weights for the evaluation function could also help our code perform better.

**What has been turned in:-**

Our code works well and can play a game and can get a non-zero score (5-15 on average). Although it works and does what it says it&#39;ll do, it is not the most optimal and will not perform as good in the tournaments.

**Part - 3: Truth be Told**

**Understanding the given problem** :-

According to the defined problem, we have a dataset that consists of multiple sentences labeled into two classes namely &quot;truthful&quot; (class1) and &quot;deceptive&quot; (class2). We are to use Naive-Bayes assumption on a Bayessian classifier to store parameters calculated from the training phase and use that to classify a test dataset into the two classes.

**Implementing the solution:-**

In order to implement the above defined problem, we first maintained two dictionaries (each for the two classes) where we traversed the entire dataset and stored the count of every unique word/string. We then divided each of these values with the total number of words in the entire dataset. This gives us the probability of a word appearing in a sentence that has been labeled as either class1 or class2. With this, we can determine whether a given sentence belongs to class1 or class2 by multiplying all the probabilities of each word appearing in a sentence with respect to the two classes. This is in such simple form due to the Naive-Bayes assumption.

**Observations and Inferences:-**

At first when we ran the code without any addition to it, we obtained an accuracy of 50% showing that there are equal numbers of sentences in each of the two classes. This is how we knew we needed to get any accuracy above 50%.

One problem we encountered during the implementation is that of very small values of total probability post multiplying that it kept becoming 0 due to the very large number of decimal places. This was taken care through the utilization of negative logarithmic functions. This helped scale the value to storable and comparable values. With this, we could compare the two probabilities for each of the classes to classify the sentences in the test dataset.

We finally obtained an accuracy of 79.75% after implementing Naive-Bayes assumption on the Baysian classifier. It comes to show that although Naive-Bayes assumption doesn&#39;t always hold true, it definitely still performs reasonably well in the real world. 
