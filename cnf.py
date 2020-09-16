import random
import sys
import time
def readfile(file):
    f=open(file)
    cluases=[]
    for x in f:
        if ( x[0] == 'c' ):#if line start with 'c' then its comment line so skip that line
            continue
        if ( x[0] == 'p' ):# if line start with 'p' then this line contain no of variables and clauses
        
            varlist=x.split()
            var=varlist[2]# var contain no of variables in cnf
            continue
        clause=x.split()
        #print(clause)
        lit=[]
        for v in clause[:-1]:#every line end with '0', so by [:-1] we discard that last 0
        
            lit.append(int(v))#list of literals
        cluases.append(lit)#list of clauses
    return cluases,int(var)
#boolean constraint propagation
def resolution(cnf,unit_clause):#parameter to the function cnf and unit_clause
    new_cnf=[]#list for modified cnf after applying unit_resolution
    for clauses in cnf:
        if unit_clause in clauses:
            continue    #remove this clause from cnf as the whole clause becomes true
        if -unit_clause in clauses:
            if(len(clauses)==1):# if clause consists of only negation of the unit_clause ,then clause becomes false,so it is inconsistent
                return -1 # if inconsistent return -1
            new_clause=[]
            for x in clauses:#else remove the negation as it becomes false and does not affect the clause
                if (x!=-unit_clause):
                    new_clause.append(x)
            new_cnf.append(new_clause)
        else:
            new_cnf.append(clauses)
    return new_cnf # return modified cnf after applying unit resolution

#function to get the unit_clauses from cnf
def unit_resolution(cnf):
    unit_clauses=[]
    var_list=[]
    for clause in cnf:
        if(len(clause)==1):
            unit_clauses.append(clause)#list of unit clauses
    if(len(unit_clauses)==0):# if no unit_clause return the cnf
        return cnf,var_list
    else:
        while unit_clauses:
            unit_clause=unit_clauses[0]# take the first unit_clause from the list and apply resolutio
            cnf=resolution(cnf,unit_clause[0])
            var_list=var_list+[unit_clause[0]]# variable list to keep track the assignments
            if(cnf==-1):# if after resolution cnf becomes -1 that mean inconsistent
                return -1,[]# return -1(inconsistent) and emty assignment list
            if(len(cnf)==0):# if cnf itself bacomes emty then return empty cnf and assignment list
                return cnf,var_list
            unit_clauses=[]
            for clause in cnf:# else calculate unit clauses from modified cnf
                if(len(clause)==1):
                    unit_clauses.append(clause)

    return cnf,var_list #at end return new modified cnf and assignment list
#function to count the frequency of literals
def get_literal(cnf):
    count={}
    for clause in cnf:
        for lit in clause:
            if lit in count:
                count[lit]+=1
            else:
                count[lit]=1
    return count
#function to get the literal which have maximum count
def frequent_lit(cnf):
    count=get_literal(cnf)
    return max(count, key=count.get)

#Weighted binaries heuristic
def Weighted_binary(cnf, weight=5):
    count={}
    for clause in cnf:
        for lit in clause:
            if lit in count:
                count[lit] += weight ** -(len(clause)-3)
            else:
                count[lit] = weight ** -(len(clause)-3)
    return count
#to get literals with maximum weight
def max_weight_binary(cnf):
    count = Weighted_binary(cnf)
    return max(count, key=count.get)
#Backbone search heuristic
def Backbone(cnf, weight=2):
    count={}
    for clause in cnf:
        for lit in clause:
            if lit in count:
                count[lit] += weight ** -(len(clause)-3)
            else:
                count[lit] = weight ** -(len(clause)-3)
    return count
#to get literal with maximum weight where wight=2
def max_weight_back(cnf):
    count = Backbone(cnf)
    return max(count, key=count.get)

# get difference of count
def difference_count(formula):
    count = {}
    for clause in formula:
        for lit in clause:
            if lit in count:
                if lit > 0:
                    count[lit] += 1
                else:
                    count[-lit] += - 1
            else:
                if lit > 0:
                    count[lit] = 1
                else:
                    count[-lit] = - 1
    return count
def diff_count(cnf):
    counter = difference_count(cnf)
    max_p_literal = max(counter, key=counter.get)
    max_n_literal = min(counter, key=counter.get)
    if counter[max_p_literal] >= abs(counter[max_n_literal]):
        return max_p_literal
    return max_n_literal
# diffrent huristics

def diffrent_huristics(heuristic):
    heuristics = {
        'FL'    : frequent_lit,
        'WBI'    : max_weight_binary,
        'WBA'   : max_weight_back,
        'DC'   : diff_count,
    }
    try:
        return heuristics[heuristic]
    except:
        sys.exit("ERROR:Not valid heuristic.")

#dpll
def dpll(cnf,assignment,heuristic):
    cnf,unit_assign=unit_resolution(cnf)# first apply unit resolution on the cnf
    assignment+=unit_assign # append the assiment done by unit_resolution to the resultant assignment
    if (cnf==-1):# after unit resolution if cnf becomes -1 that means cnf is inconsistent
        return [] #return emty list to understand that cnf becomes inconsistent
    if(len(cnf)==0):#cnf becomes empty that mean cnf is satisfiable
        return assignment# as cnf is satisfiable so return assignment
    var=heuristic(cnf)#choose decision variable whose count is maximum in the clauses of cnf
    sol=dpll(resolution(cnf,var),assignment+[var],heuristic)# first apply unit resolution on cnf depending on decision variable,then call dpll on the resultant cnf recursively
    if(len(sol)==0):#if sol becomes empty that means inconsistant, so we have to backtrack and check for the negation of the decision variable
        sol=dpll(resolution(cnf,-var),assignment+[-var],heuristic)
    return sol
#main
def main():
    start = time.time()
    fout= open('output_file',"w")
    if len(sys.argv) < 2 or len(sys.argv) > 3 :
        sys.exit("Invalid argument list")
    if len(sys.argv) == 3:
        heuristic = diffrent_huristics(sys.argv[2])
    else:
        heuristic = frequent_lit
    clauses, no_of_vars = readfile(sys.argv[1])#read cnf file,clauses contain list of clauses
    ans=dpll(clauses,[],heuristic)# call dpll with empty assignment list and cnf formula
    end = time.time()
    print('time : '+ str(end-start))
    if(len(ans)==0):#if dpll returns empty list that mean all truth values of unit clause and decision variables leads to inconsistent that mean unsatisfiable
        print("Unsatisfiable")
        fout.write('Unatisfiable\n')
    else:
        for x in range(1,no_of_vars+1):#if a variable is not in assignment list that mean the truth value of that variable does not matter so we assign it to true 
            if x not in ans and -x not in ans:
                ans.append(x)
        ans.sort(key=abs)#sort the assignment list to show the output
        print('Satisfiable')
        print(ans)
        fout.write('Satisfiable\n')
        fout.write("Assignment:\n"+' '.join([str(x) for x in ans]) + ' 0')
    fout.close()
if __name__ == '__main__':
    main()