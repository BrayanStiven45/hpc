# #! /bin/bash
# for j in {1..10}
# do
# for i in 10 100
# do
# ./main $i >> times2.doc
# done
# done

#!/bin/bash

OUTPUT="times.csv"

# Define sizes (columns)
sizes=(10 100 200 300)

# Write header row
echo -n "Run" > $OUTPUT
for s in "${sizes[@]}"; do
    echo -n ",$s" >> $OUTPUT
done
echo "" >> $OUTPUT

# Runs
for j in {1..10}; do
    echo -n "$j" >> $OUTPUT
    
    for s in "${sizes[@]}"; do
        time=$(./main $s)
        echo -n ",$time" >> $OUTPUT
    done
    
    echo "" >> $OUTPUT
done
