import random
import sys
def nqueens(nr):
	show(min_conflicts(list(range(nr)), nr), nr)

#print the solution if it exists
def show(soln, nr):
	for i in range(nr):
		row = ['~'] * nr
		for col in range(nr):
			if soln[col] == nr - 1 - i:
				row[col] = 'Q'
		print(''.join(row))

#passing in number of iterations to overcome situations where min-conflicts chokes
#due to critical-ratio issues
#this should not matter in most cases
def min_conflicts(soln, nr, iters=1000000):
        #initialize queens to random positions
        def random_pos(li, filt):
                return random.choice([i for i in range(nr) if filt(li[i])])
        
        for k in range(iters):
                conflicts = find_conflicts(soln, nr)
                if sum(conflicts) == 0:
                        return soln
                column = random_pos(conflicts, lambda i: i>0)
                con = [hits(soln, nr, column, row) for row in range(nr)]
                soln[column] = random_pos(con,lambda i: i == min(con))

            
def find_conflicts(soln, nr):
        return [hits(soln, nr, col, soln[col]) for col in range(nr)]

def hits(soln, nr, col, row):
	total = 0
	for i in range(nr):
		if i == col:
			continue
		if soln[i] == row or abs(i - col) == abs(soln[i] - row):
			total += 1
	return total

#try running n-queens with n=64 etc.
nqueens(8)
