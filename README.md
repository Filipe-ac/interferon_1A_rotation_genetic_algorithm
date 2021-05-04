# interferon_1A_rotation_genetic_algorithm
Python implementation of the genetic algorithm to optimize body rotation for Interferon Beta-1a (*Rebif*) shots

## About:
The Interferon Beta-1a medication is administered subcutaneously, usually trhice a week, and it can be injected in approximately 30 spots over the patient's body, in the sparsest fashion possible. The objective of this program is to apply the genetic algorithm to find an optimal application rotation. Note that not all possible spots are suitable for all patients, so the answer to this problem may vary from person to person.

## Dependencies

Numpy

#### Optional dependencies:

Matplotlib (If one would like to plot the solutions. Ultimately not necessary)

## Documentation:


First of all, you must download the "rotation.py" script and the "coordinates" file. The latter contains the pixel coordinates of the application spots, based on a suggestion from an official image distributed in Brazil:

<img src="https://user-images.githubusercontent.com/78453361/114648406-1d542700-9cb5-11eb-9b56-c470074df9e9.png" width="500">


Please, note that this is not an indication of where one should apply the medicine. Always consult with a health professional. More information can be found in [https://www.rebif.com/en]

One can generate their own points creating a file named "coordinates" with 3 columns, for the x, y and z dimensions of each point.

####   Run from command line
The parameters are tested and should converge in some minutes. To run the default options just type in command line (linux):    
    `python rotation.py`

If you want to exclude any points:  
    `python rotation.py -e [list of points to exlude]`
    
Accepted formats for points are:  
`[p1,p2,...,pn]` or `p1,p2,...,pn`

To modify the parameters, one can pass the following arguments:

- -i: Number of iterations. Default = 50000  
- -e: Points to exclude. Default = ''; (Acceptable entries are [1,2..], 1,2,..)  
- -npop: Population number. Default = 100  
- -b: number of best individuals to keep (fraction of the total number of individuals). Default = 20  
- -w: number of worst individuals to keep (fraction of the total number of individuals). Default = 10  
- -m: mutation probability. Default = 0.7  
- -c: couple probability. Default = 0.7  
 

To control the output:

- -n: name of the destination folder. Default = interferon_rotation  
- -plots: if 1, will generate plots of the solutions. Default = 0  
- -v: Verbose (0 or 1). Default = 0  


For test purposes:

- -p: coordinates of the points. Default = coordinates, will get the coordinates from the file "coordinates".  
    other built-in options are: "sphere", "spiral" or "circle", which will create random points in these geometries.   
- -np: number of points (only relevant if -p equals "sphere", "spiral" or "circle"). Default = 30 

## The Objective Function:

The recommendation is to distance the applications from one another as much as possible, and avoid the same area for at least 3 applications. Hence, the objective function must keep some "memory". With that in mind, the objective function that we will minimize consists in the sum of the distances of the three previous steps, weighted by a decreasing exponential function, calculated for all points.  

To visualize the behavior of the algorithm, we will plot the result in a circle with 30 points, in which the first rotation was randomly generated. 

<img src="https://user-images.githubusercontent.com/78453361/114650184-2abee080-9cb8-11eb-8c93-b0d5b65e863f.png" width="500">

## Complete rotation:
Here is a possible solution based on *rebif* points definition used in a suggestion published in Brazil, as discussed above:

1, 30, 14,  5, 20, 24, 16,  6, 19, 21, 28, 11,  3,  2, 27, 29,  4,  7, 23, 26,  8, 15, 18, 22, 12, 10, 17, 25, 13,  9
 

## Comparing with manual solution:

The motivation for this program was build a better rotation for my wife. 

My first attempt consisted in manually set a rotationa, which yielded this value for the objective function defined above:  
Manual result: 0.01500911342024823 (1/distance)

Using the algorithm:           
Algorithm: 0.008883459711788349 (1/distance)


## Validation:

In order to validate the code, we cretated 100 points in a circle and minimize the path that cover all points each time, returning to the initial point. The images above show the first path (radomly genereted) and the final path.![_tmp00000](https://user-images.githubusercontent.com/78453361/113072812-50b79180-919e-11eb-94ba-4ee2159d3654.png)![_tmp117159](https://user-images.githubusercontent.com/78453361/113072823-56ad7280-919e-11eb-8ba5-b4f874111dc5.png)



The convergencie plot is show below:

![image](https://user-images.githubusercontent.com/78453361/113073076-c9b6e900-919e-11eb-83d0-2911cc743a3d.png)
