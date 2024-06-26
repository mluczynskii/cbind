# Test Validator

This script is used to validate test cases for a program.

## Usage

```
python3 validator.py [-t {auto, manual}] [-v] [-cases i j k]
```
## Flags

-v: Verbose mode. Shows detailed information about failed tests
-cases i j k: Runs specific test cases (space-separated list)
-t {auto, manual}: Test type: auto (unit tests) or manual (manual tests). Default: auto.

## Note

To compile the final program using a different Makefile than the one provided in the main directory, you need to add a ,"makefile" to the test_cases/case_i/src directory.

Additionally, make sure to set the path to the Lua source in the makefile.