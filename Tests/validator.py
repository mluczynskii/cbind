import os
import subprocess
import filecmp
import argparse
import shutil
import glob

TEST_DIRECTORY = "test_cases"
SOURCE_DIRECTORY = "src"
FILES_TO_KEEP = ['validator.py', 'test_cases', 'Makefile', 'lua_binding_api.h', 'README.md']
PARSER_PATH = "../src/parser/parser.py"
GENERATOR_PATH = "../src/binding-generator/binding-generator.py"
MANUAL_DIRECTORY = "manual"
AUTO_DIRECTORY = "auto"
BINDING_FILE_NAME = "binding.c"
TESTING_FILE = "main"

VERBOSE = False
KEEP_FILES = False

# Copy C program source code from /test_cases/casei/src to the working directory
def copy_src_code(case):
    source_directory = os.path.join(TEST_DIRECTORY, case, SOURCE_DIRECTORY)
    for file_name in os.listdir(source_directory):
        source_file = os.path.join(source_directory, file_name)
        if os.path.isfile(source_file):
            shutil.copy(source_file, ".")

# Generating files with AST for every source file with the .c extension
def generate_AST(case):
    c_files = glob.glob("*.c")

    # Using the -S flag with GCC to generate AST files without compilation; this avoids compilation errors caused by the lack of binding files
    compile_command = f"gcc -S -fdump-tree-original-raw {' '.join(c_files)}"
    result = subprocess.run(compile_command, shell=True)

    if result.returncode == 0:
        return 0
    else:
        print(f"AST generating Error")
        return 1

def compile_with_binding_error(result, message):
    print(message)
    print(result.stdout.decode())
    print(result.stderr.decode())
    return 1

# Make an executable file using the make program
def compile_with_binding(case):
    c_files = glob.glob("*.c.005t.original")
    c_file_arguments = " ".join(c_files)
    
    result1 = subprocess.run(["python3", PARSER_PATH] + c_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result1.returncode != 0:
        return compile_with_binding_error(result1, "Parsing error:")
    
    result2 = subprocess.run(["python3", GENERATOR_PATH, "data.json", f"./{BINDING_FILE_NAME}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result2.returncode != 0:
        return compile_with_binding_error(result2, "Code Generating error:")
    
    result3 = subprocess.run(["make"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result3.returncode != 0:
        return compile_with_binding_error(result3, "Make error:")
    
    return 0

def run_manual_test(case):
    input_directory = os.path.join(TEST_DIRECTORY, case, MANUAL_DIRECTORY, "in")
    output_directory = os.path.join(TEST_DIRECTORY, case, MANUAL_DIRECTORY, "out")

    if not (os.path.exists(input_directory) and os.path.exists(output_directory)):
        print(f"{case}: Manual test not found")
        return 0

    failed_tests = []

    for input_file in sorted(os.listdir(input_directory)):
        input_path = os.path.join(input_directory, input_file)

        test_number = input_file[2:-4]

        expected_output_file = f"out{test_number}.txt"
        expected_output_path = os.path.join(output_directory, expected_output_file)

        result = subprocess.run([f"./{TESTING_FILE}", input_path], capture_output=True, text=True)

        actual_output = result.stdout.strip()

        with open(expected_output_path, "r") as f:
            expected_output = f.read().strip()

        if not (result.returncode == 0 and actual_output == expected_output):
            failed_tests.append((test_number, expected_output, actual_output))

    if failed_tests:
        if VERBOSE:
            print("Failed tests: ")
            for test_number, expected, actual in failed_tests:
                print(f"Nr: {test_number}, Expected: {expected}, Result: {actual} ")
        else:
            print("Failed")
    else:
        print("All tests passed!")

def run_auto_test(case):
    input_directory = os.path.join(TEST_DIRECTORY, case, AUTO_DIRECTORY)

    if not os.path.exists(input_directory):
        print(f"{case}: Auto test not found")
        return 0

    lua_scripts = [f for f in os.listdir(input_directory) if f.endswith(".lua")]

    for script in lua_scripts:
        script_path = os.path.join(input_directory, script)
        
        result = subprocess.run([f"./{TESTING_FILE}", script_path], capture_output=True, text=True)
        
        if result.stderr.strip() == "true":
            print("Success")
        else:
            print("Error: Lua test script execution failed:")
            print(result.stdout)
            print(result.stderr)

def run_case(case, test_type):
    copy_src_code(case)
    if(generate_AST(case)):
        return 1
    if(compile_with_binding(case)):
        return 2
    if test_type == "manual":
        run_manual_test(case)
    else:
        run_auto_test(case)

# Remove test files from the working directory
def cleanup_test_environment():
    all_files = os.listdir('.')

    for file_name in all_files:
        if file_name not in FILES_TO_KEEP:
            if os.path.isfile(file_name):
                os.remove(file_name)
            elif os.path.isdir(file_name):
                os.rmdir(file_name)

def run_cases(selectedCases, test_type):
    if selectedCases == None:
        selectedCases = os.listdir("./test_cases")

    selectedCases = sorted(selectedCases)
    cleanup_test_environment()
    for case in selectedCases:
        print(f"Running : {case}")
        run_case(case, test_type)
        if not KEEP_FILES:
            cleanup_test_environment()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run test cases.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed information about failed tests.")
    parser.add_argument("-cases", "--selected_cases", nargs="+", help="Run specific test cases (space-separated list).")
    parser.add_argument("-t", "--test_type", choices=["auto", "manual"], default="auto", help="Test type: auto (unit tests) or manual (manual tests). Default: auto.")
    parser.add_argument("-k", "--keep_files", action="store_true", help="Keep temporary files after validation")
    args = parser.parse_args()

    VERBOSE = args.verbose
    KEEP_FILES = args.keep_files

    if args.selected_cases:
        selected_cases = [f"case{case}" for case in args.selected_cases]
        run_cases(selected_cases, args.test_type)
    else:
        run_cases(None, args.test_type)