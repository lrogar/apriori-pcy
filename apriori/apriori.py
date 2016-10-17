import sys
import timeit

basket_num = 0 # How many baskets to read from the data set
filename = "dataset.txt"
support = 0
items_count = dict()
freq_items = list()
freq_pairs_count = dict()

# Establish the value for the support threshold.
def set_init_vals():
    if (len(sys.argv) > 2):
        global support
        global basket_num
        support = int(sys.argv[1])
        basket_num = int(sys.argv[2])
        
        print ""
        print "Support Threshold:", support
        print "Sample size:", basket_num, "baskets"
        
    else:
        print "Please enter two arguments: Support threshold and number of baskets to evaluate."
        sys.exit(0)
    
def pass1():
    
    line_count = 0
    
    infile = open(filename)
    
    # Read items from the file, each line interpreted as a basket
    for line in infile: 
        line = line.rstrip() # strip off newline and any other trailing whitespace
        basket = line.split()
        line_count += 1
        # Go through every item in every basket (line)
        for item in basket:
            # If the item is already in the directory,
            if item in items_count:
                # then increment it's count.
                items_count[item] += 1
                # print "Count for", item, "was incremented to", items_count[item],"on the directionary"
            else:
                # Otherwise, add it and set its count to 1
                items_count[item] = 1
                # print item, "was added to the dictionary"
        
        global basket_num
        if line_count == basket_num:
            break
        
    infile.close()
     
    # Filter dictionary so only frequent items are stored. At this point, counts no longer matter.
    global freq_items
    freq_items = (({item: count for item, count in items_count.items() if count >= support}).keys())
    
    # print "Frequent items found:", len(freq_items)
    # print freq_items
                
# Need to create candidate pairs
def between_passes():
        
    for i in range(0, len(freq_items)):
        for j in range (i+1, len(freq_items)):
            # print "Finding pairs"
            freq_pairs_count[(freq_items[i], freq_items[j])] = 0
                
# Check that the candidate pair is frequent itself as well
def pass2():
    
    infile = open(filename) # (filename, 'r') is assumed
            
    for line in infile: 
        line = line.rstrip()
        basket = line.split()
        for pair in freq_pairs_count:
            # print "Checking if potential pairs are frequent"
            if(pair[0] in basket and pair[1] in basket):
                freq_pairs_count[pair] += 1
                # print "Found frequent pair"
                
    infile.close()
    
    # Print frequent pairs found
    # print ""
    # print "Frequent pairs:"
    # for pair in freq_pairs_count:
        # if freq_pairs_count[pair] >= support:
            # print pair, freq_pairs_count[pair]
    # print ""
    
    i = 1;
    freq_pairs = dict()
    
    for pair in freq_pairs_count:
        if freq_pairs_count[pair] >= support:
            freq_pairs[pair] = freq_pairs_count[pair]
            
    sorted_freq_pairs = sorted(freq_pairs.items(), key=lambda x: (-x[1], x[0]))
    
    # Print frequent pairs found
    print ""
    print "Frequent pairs:"
    for pair in sorted_freq_pairs:
        if i == 101:
            break
        else:
            print pair
            i+=1
    print ""

# start = timeit.default_timer()
set_init_vals()
pass1()
between_passes()
pass2()
# end = timeit.default_timer()
# runtime = end - start

# print "Run time:", runtime, "secs"
# print ""
 
# results = str(basket_num) + ", " + str(support) + ", " + str(runtime) + "\n"
# open("apriori_results.txt", "a").write(results)