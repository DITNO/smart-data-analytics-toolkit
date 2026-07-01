def num_adder(a, b):
   try:
    result = a / b
    return result
   except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
    return None

print(num_adder(5, 10))
print(num_adder(5, 0))