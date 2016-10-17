import sys
import timeit
# from bitmap import BitMap

basket_num = 0 # Lines to read from the data sets
filename = "dataset.txt"
support = 0
bucket_field = 10000 # Everything collides with 1000 only!
items_count = dict()
freq_items = list()
freq_pairs_count = dict()
pairs_hash_map = dict()
bitmap = list()

# Establish the value for the support threshold.
def set_init_vals():
    if (len(sys.argv) > 2):
        global support
        global basket_num
        support = int(sys.argv[1])
        basket_num = int(sys.argv[2])
        
        # print ""
        # print "Support Threshold:", support
        # print "Sample size:", basket_num, "baskets"
        
    else:
        print "Please enter two arguments: Support threshold and number of baskets to evaluate."
        sys.exit(0)
        
def hash(x, y):
    # Hash function we were suggested to use
    return (x ^ y) % bucket_field
    
def pass1():
    
    line_count = 0
    
    infile = open(filename)
    
    # print "[DEBUGGING] In pass 1"
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

        # Keep count for each bucket into which pairs are hashed
        for i in range(0, len(basket)):
            for j in range(i+1, len(basket)):
                pair = (basket[i], basket[j])
                hashed_val = hash(int(pair[0]), int(pair[1]))
                if hashed_val in pairs_hash_map:
                    pairs_hash_map[hashed_val] += 1
                else:
                    pairs_hash_map[hashed_val] = 1
        
        global basket_num
        if line_count == basket_num:
            break
        
    infile.close()
    
    # Filter dictionary so only frequent items are stored. At this point, counts no longer matter.
    global freq_items
    freq_items = (({item: count for item, count in items_count.items() if count >= support}).keys())
                
# Replace the buckets by a bit-vector
def between_passes():
    
    # print "[DEBUGING] Between passes"
    
    position = 0
    # Initialize bitmap to zeros
    bitmap = [chr(0)]*bucket_field
    
    # @Reference: Worked together in this section (bitmap) with Alexandar Mihaylov
    # Convert hash map to bitmap
    for pair in sorted(pairs_hash_map.keys()):
        if pairs_hash_map[pair] >= support:
            bitmap[position/8] = chr(ord((bitmap[position/8])) | ord(chr(1 << (position%8))))
        position += 1
            
    # Generate all possible pairs of frequent items
    for i in range(0, len(freq_items)):
        for j in range(i+1, len(freq_items)):
            if bitmap[hash(int(freq_items[i]), int(freq_items[j]))] > 0:
                # print "Finding pairs"
                freq_pairs_count[(freq_items[i], freq_items[j])] = 0

# Only count pairs that hash to frequent buckets
def pass2():
    
    infile = open(filename) # (filename, 'r') is assumed
    
    # print "[DEBUGGING] Pass 2"
    
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

start = timeit.default_timer()
set_init_vals()
pass1()
between_passes()
pass2()
end = timeit.default_timer()
runtime = end - start

# print "Run time:", timeit.default_timer() - start, "secs"
# print ""

results = str(basket_num) + ", " + str(support) + ", " + str(runtime) + "\n"
open("pcy_results.txt", "a").write(results)