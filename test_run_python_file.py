
from functions.run_python_file import run_python_file


print("TEST 1: Calculator usage")
print(run_python_file("calculator", "main.py"))

print("\nTEST 2: Calculate 3 + 5")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("\nTEST 3: Calculator tests")
print(run_python_file("calculator", "tests.py"))

print("\nTEST 4: Directory traversal")
print(run_python_file("calculator", "../main.py"))

print("\nTEST 5: Missing file")
print(run_python_file("calculator", "nonexistent.py"))

print("\nTEST 6: Non-Python file")
print(run_python_file("calculator", "lorem.txt"))
