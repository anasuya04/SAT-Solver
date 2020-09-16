# SAT-Solver
Given a boolean formula a SAT Solver determines whether the formula is satisfiabe or not. This is an implimentation of DPLL agorithm.

Python Code file named "cnf.py" conatin the code to for solver to apply to the problems provided in cnf form.

	
	Instruction for the input file:
		
		1) This folder contain files with extention .cnf , use the name of the files in command line arguments to test the program for respective input file.
		
	Instructions for running the python code file:
		
		1) To run the py code on termonal , just write the following command:
				
				python cnf.py
 [input_file] [heuristic : FL , WBI , WBC,DC]
			e.g.    python cnf.py my.cnf WBC ( Default one is FL)
	
			where after program name, first argument is name of input file and next is the heuristic.
	
	Instructions for checking the output:
		
		1) on console , you can check the result for the particular input.

		2) Assignment for the valid and satisfiable clauses can also be checked from "Assignment.txt".
						
	Writeup is include in folder named : "SAT_SOLVER.pdf"
