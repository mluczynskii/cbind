#!/bin/bash
gcc -c src/api.c -I./include -fdump-tree-original-raw=build/api.c.005t.original -o build/api.o
ls ./build
ls .
python3 ../cbind/parser.py build/api.c.005t.original
mv dump.json build/dump.json
python3 ../cbind/main.py build/dump.json -o src/binding.c
make main

# TODO: loop over cases
./main scripts/case_1.lua
if [[ "$?" -eq 0 ]]; then 
  echo "Test passed!"
  exit 0
else 
  echo "Test failed..."
  exit 1
fi 