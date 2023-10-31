def greedysymmetric(n,start_conf):
    
    m = int((int(n/2)+1)/2)
    #ammount of rows = 2*m
    
    total = int(n*(n+1)/2)
    #ammount of slots = total - 1

    blocks = [[1 for column in range(n)] for row in range(m)]

    solution = [[0 for column in range(n)] for row in range(2*m)]

    row_sum = [0 for row in range(2*m)]

    delta = [0 for row in range(2*m)]
    larger = [0 for row in range(2*m)]

    sol_sum = [[] for row in range(2*m)]

    #function to print information
    def printdata():
##        print('available blocks:')
##        for i in range(m):
##            print(blocks[i])
##        for i in range(m):
##            print(blocks[-i-1])
        print('starting configuration:')
        print(start_conf)
        print('solution:')
        for i in range(2*m):
            print(solution[i])
        print('solution sum:')
        for i in range(2*m):
            print(sol_sum[i])
        #print('row_sum:',row_sum)

    #Set up starting configuration
    for i in range(m):
        s = start_conf[i]
        blocks[i][s-1]= 0
        solution[i][0] = s
        solution[-i-1][-1] = s
        row_sum[i] = s
        sol_sum[i].append(s)
        s = start_conf[-i-1]
        blocks[i][s-1]=0
        solution[-i-1][0] = s
        solution[i][-1] = s
        row_sum[-i-1] = s
        sol_sum[-i-1].append(s)

    #printdata()

    #main loop
    for slot in range(1,total):
        #print('slot:',slot) #flag
        #check if slot is already filled
        if any(slot in row for row in sol_sum):
            #print('slot already covered')
            continue
        #if slot in row_sum:
         #   print('slot already covered')
          #  continue
        #order largest gaps between rows and slot
        for row in range(2*m):
            delta[row] = slot - row_sum[row]
            larger[row] = delta[row]
        larger.sort(reverse=True)
        #check in order if it is possible to add block
        ended=0
        for row in range(2*m):
            cand_block = larger[row]
            cand_row = delta.index(cand_block)
            compl_row = 2*m - 1 - cand_row
            check_row = min(cand_row, compl_row)
            #print('check_row:',check_row) #flag
            #print('cand_row',cand_row) #flag
            #print('cand_block:',cand_block) #flag
            
            #check if we need a block bigger than the biggest block
            if cand_block>n:
                #print('row needs too big of a block. row:',cand_row)
                break
            if cand_block<0:
                #print('could not cover slot:',slot)
                break
            
            #if it is possible to add block, add it
            if blocks[check_row][cand_block-1]:
                #print('block accepted') #flag
                blocks[check_row][cand_block-1] = 0
                ind = solution[cand_row].index(0)
                cind = n - 1 - ind
                solution[cand_row][ind] = cand_block
                solution[compl_row][cind] = cand_block
                row_sum[cand_row]+=cand_block
                sol_sum[cand_row].append(row_sum[cand_row])
                if row_sum[cand_row]==total-row_sum[compl_row]:
                    res_compl = [total - x for x in sol_sum[cand_row][-2::-1]]
                    res_cand = [total - x for x in sol_sum[compl_row][-2::-1]]
                    sol_sum[compl_row].extend(res_compl)
                    sol_sum[cand_row].extend(res_cand)
                    
                ended=1
                #printdata()
                break
            #print('block rejected') #flag
        #check if slot was not filled
        if ended==0:
##            print('slot not covered / problem. slot:', slot)
##            printdata()
##            for i in range(2*m):
##               print('row:',i,'block needed:',slot - row_sum[i])
##            print('from the other side:')
##            for i in range(2*m):
##               print('row:',i,'block needed:',total - row_sum[-i-1]-slot)
            break

    #check solution
    if ended:
        print('─' * 10)
        print('\n')
        print('solution found')
        printdata()

    return ended

#end of function


#function creating all possible combinations
def n_length_combo(lst, n):
     
    if n == 0:
        return [[]]
     
    l =[]
    for i in range(0, len(lst)):
         
        m = lst[i]
        remLst = lst[i + 1:]
         
        remainlst_combo = n_length_combo(remLst, n-1)
        for p in remainlst_combo:
             l.append([m, *p])
           
    return l

#search loop for starting configurations
while True:
    try:
        n = int(input("Please enter the maximum size of blocks (n): "))
    except ValueError:
        print("Sorry, I didn't understand that.")
        continue

    if n < 0:
        print("Sorry, your response must not be negative.")
        continue
    elif n%4 != 2:
        print('Your answer needs to be congruent to 2 mod 4 for the algorithm to run')
    else:
        #n is a valid size
        break

l = int(n/2)

available_blocks = [x for x in range(2,n+1)]
num_of_sol=0

combinations = n_length_combo(available_blocks,l)
for lst in combinations:
    start_conf=[1]
    start_conf.extend(lst)
    num_of_sol += greedysymmetric(n,start_conf)

print('─' * 10)
print('\n')
print('Number of solutions found: ',num_of_sol)
#greedysymmetric(10,[1, 2, 4, 5, 7, 8])
