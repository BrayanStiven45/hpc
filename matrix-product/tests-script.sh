#!/bin/bash

sizes=(400 600)

num_threads=(1 2)


for thread in "${num_threads[@]}"; do
  OUTPUT="times_$thread.csv"
  # Write header row
  echo -n "Run" > $OUTPUT
  for s in "${sizes[@]}"; do
    echo -n ",$s" >> $OUTPUT
  done

  echo "" >> $OUTPUT
  
  echo "Tes with $thread thread: "
  # Runs
  for j in {1..10}; do
    echo -n "$j" >> $OUTPUT
    
    echo "Test $j with each size:"
    for s in "${sizes[@]}"; do
      # time=$(./exe/main.exe $s)
      time=$(./main $s $thread)
      echo -n ",$time" >> $OUTPUT
      echo "$s x $s done!"
    done
      
    echo "" >> $OUTPUT
    echo ""
  done
done 
