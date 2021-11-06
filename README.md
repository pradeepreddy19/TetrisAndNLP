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

Unfortunately, the scores only went as high as 17.

![](RackMultipart20211106-4-16864fh_html_cf9b86b19ae142b8.png)

**Evaluation Functions:-**

Reference- https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/

While researching evaluation functions, we came across the above source from where we implemented the number of gaps, summation of height of every column, difference in adjacent column heights to get the bumps in the board and also the number of lines filled in a board. Apart from these, we also implemented our own evaluation function which is a weighted row coverage that assigns a higher score to a board if it has its pieces scattered across rather than all of them being mostly placed on a single row. We then take the minimum of this as the best move for the current piece. We tried different combinations of the evaluation functions and we set the sign for each by determining whether to maximize it or minimize it.

We could still only go as high as 17 and the minimum is still 0.

**What could have possibly gone wrong? :-**

While deciding on implementations, we had two further sub-options while adding the next piece into the equation. One is calculating the move for the current piece as well as the next piece every single iteration and returning only the move for the current piece and forgetting about the move generated for the next piece. The other sub-option was to only compute the move for the next piece every iteration and use the move for the current piece from the previous iteration. We found that the scores did not improve after going through with the first sub-option. This is because the optimal move relationship between the first and the subsequent pieces is lost when we recompute the move for the current piece every iteration. Other problems that this resulted in was also a higher time complexity. Another reason for a high time complexity was duplicate boards generated due to rotation/ flipping of symmetrical pieces.

**Scope for a better solution:-**

We could implement sub-option 2 that was discussed above to get a better performance in scores. In order to decrease time complexity we could also try to remove the duplicated pieces.

**What has been turned in:-**

Our code works well and can play a game and can get a non-zero score (5-10 on average). Although it works and does what it says it&#39;ll do, it is not the most optimal and will not perform as good in the tournaments.

**Part - 3: Truth be Told**

**Understanding the given problem** :-

According to the defined problem, we have a dataset that consists of multiple sentences labeled into two classes namely &quot;truthful&quot; (class1) and &quot;deceptive&quot; (class2). We are to use Naive-Bayes assumption on a Bayessian classifier to store parameters calculated from the training phase and use that to classify a test dataset into the two classes.

**Implementing the solution:-**

In order to implement the above defined problem, we first maintained two dictionaries (each for the two classes) where we traversed the entire dataset and stored the count of every unique word/string. We then divided each of these values with the total number of words in the entire dataset. This gives us the probability of a word appearing in a sentence that has been labeled as either class1 or class2. With this, we can determine whether a given sentence belongs to class1 or class2 by multiplying all the probabilities of each word appearing in a sentence with respect to the two classes. This is in such simple form due to the Naive-Bayes assumption.

**Observations and Inferences:-**

At first when we ran the code without any addition to it, we obtained an accuracy of 50% showing that there are equal numbers of sentences in each of the two classes. This is how we knew we needed to get any accuracy above 50%.

One problem we encountered during the implementation is that of very small values of total probability post multiplying that it kept becoming 0 due to the very large number of decimal places. This was taken care through the utilization of negative logarithmic functions. This helped scale the value to storable and comparable values. With this, we could compare the two probabilities for each of the classes to classify the sentences in the test dataset.

We finally obtained an accuracy of 79.75% after implementing Naive-Bayes assumption on the Baysian classifier. It comes to show that although Naive-Bayes assumption doesn&#39;t always hold true, it definitely still performs reasonably well in the real world.
