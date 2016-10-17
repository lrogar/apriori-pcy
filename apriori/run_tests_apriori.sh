#!/bin/bash

#rm apriori_results.txt

for support in {200,500,1000,10000}
do    
    echo $support
    for ((basket = 10000; basket <= 90000; basket+=10000))
    do
	for ((i = 0; i < 5; i++))
	do
	    /usr/local/Cellar/pypy/4.0.0/libexec/bin/pypy apriori.py $support $basket
	done
    done
done

