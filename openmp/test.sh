#!/bin/bash

sizes=(400 600 800 1200 1600 2400 3200 4800 6400 9600)
OUTPUT="times.csv"

# Write header row
echo -n "Run" > $OUTPUT
for s in "${sizes[@]}"; do
  echo -n ",$s" >> $OUTPUT
done

echo "" >> $OUTPUT
  
# Runs
for j in {1..10}; do
  echo -n "$j" >> $OUTPUT
  
  echo "Test $j with each size:"
  for s in "${sizes[@]}"; do
    time=$(./bin/main $s)
    echo -n ",$time" >> $OUTPUT
    echo "$s x $s done!"
  done
    
  echo "" >> $OUTPUT
  echo ""
done
