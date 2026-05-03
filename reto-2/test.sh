#!/bin/bash

sizes=(1000 10000 100000 1000000 10000000 100000000)
DENSITY=0.5
SEED=31
OUTPUT="times.csv"

mkdir -p bin

gcc -O2 sequential.c -o ./bin/sequential || { echo "Error compiling sequential"; exit 1; }
gcc -O2 openmp.c     -o ./bin/openmp -fopenmp || { echo "Error compiling openmp"; exit 1; }

echo -n "run" > $OUTPUT
for s in "${sizes[@]}"; do
    echo -n ",seq_$s,omp_$s" >> $OUTPUT
done
echo "" >> $OUTPUT

for j in {1..10}; do
    echo "Run $j..."
    echo -n "$j" >> $OUTPUT
    for s in "${sizes[@]}"; do
        t_seq=$(./bin/sequential $s $DENSITY $SEED)
        t_omp=$(./bin/openmp     $s $DENSITY $SEED)
        echo -n ",$t_seq,$t_omp" >> $OUTPUT
    done
    echo "" >> $OUTPUT
done

echo "Ready. Results in $OUTPUT"
