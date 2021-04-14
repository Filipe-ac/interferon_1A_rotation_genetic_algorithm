# interferon_1A_rotation_genetic_algorithm
Python implementation of the genetic algorithm to optimize the body rotation for Interferon Beta-1a (Rebif) shots

UNDER CONSTRUCTION

About:

The Interferon Beta-1a medication is ministrated with a subcutenous injection, usualy trhice a week, that can be applyed in around 30 points over the patient body. It is recomended that the shots are aplayed in as sparse as possible. This program apply the genetic algorithm to obtain a optimized rotatition. Note that not all possible points are suitable for all patiantes, so the answer for this problem may vary from on person to another.

Dependencies:

Numpy

Documentation:

From command line

From command line in linux just call rotation.py - [list of points to exlude]

The parameters are tested to have a good convergence, but can be modified with the following arguments

Parameters to change:
-i number of indivus; Default = 100
-b number of best individuals to keep (fraction of the total number of individuaus); Default = 
-w number of worst individuals to keep (fraction of the total number of individuaus);
-a probability of change of "genetic material" between two solutions; Default = 
-m probability of mutatuin; Default = 
-n name of the destination folder; Default = 

THE OBJECTIVE FUNCTION:

  The recomendation is sparse the applications as much as possible, and wait at least 3 applications to return near to some area, wich force the objective function to keep some memory of what came before. With that in mind, the objective function that we will minimize consist in the sumation of the distancies of the three previous steps, pondarated from a decresing exponential function, for all the points.

To visualize the behavior of the algorithm, we will plot the result apllied on 30 points distributed in a circle:


Complete rotation:

Comparing with manual solution:
 Algorithm              Manua result (1/distance)
0.008883459711788349 0.01500911342024823

Validation:

In order to validate the code, we cretated 100 points in a circle, with a initial path covering all points each time, and used the algorithm to minimize the distancies. The images above show the first path (radomly genereted) and the final path.![_tmp00000](https://user-images.githubusercontent.com/78453361/113072812-50b79180-919e-11eb-94ba-4ee2159d3654.png)![_tmp117159](https://user-images.githubusercontent.com/78453361/113072823-56ad7280-919e-11eb-8ba5-b4f874111dc5.png)



The convergencie plot is show below:

![image](https://user-images.githubusercontent.com/78453361/113073076-c9b6e900-919e-11eb-83d0-2911cc743a3d.png)
