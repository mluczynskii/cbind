#!/bin/bash
gcc -c src/api.c -I./include -fdump-tree-original-raw -o api.o
python3 ../cbind/parser.py api.c.005t.original
python3 ../cbind/main.py dump.json -o src/binding.c
make main
make clean

# TODO: loop over cases
./main scripts/case_1.lua
if [[ "$?" -eq 0 ]]; then 
  echo "Test passed!"
  exit 0
else 
  echo "Test failed..."
  exit 1
fi 