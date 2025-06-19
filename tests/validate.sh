#!/bin/bash
make

PASSED=0
TOTAL=0
for filename in scripts/*.lua; do
  [[ -e "$filename" ]] || continue
  echo "Running case $filename..."
  TOTAL=$((TOTAL + 1))
  ./main "$filename"
  if [[ "$?" -eq 0 ]]; then 
    echo -e "\033[32mPassed!\033[0m"
    PASSED=$((PASSED + 1))
  else 
    echo -e "\033[31mFailed...\033[0m"
  fi 
done

make clean distclean 2>/dev/null 1>/dev/null

if [[ "$PASSED" -ne "$TOTAL" ]]; then 
  echo -e "Passed $PASSED/$TOTAL tests... 🤕🤕"
  exit 1
else
  echo -e "\n🎉🎊🥳🎈🎂🎁💃🕺🏆✨🎆🎇"
  echo "Every test passed!"
  echo "🎉🎊🥳🎈🎂🎁💃🕺🏆✨🎆🎇"
  exit 0
fi

