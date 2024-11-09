#. Drawing Patterns with Nested Loops 

#promt user for input

pat_size = int(input("Enter the size of the pattern: "))
rows = 0
while rows < pat_size:
    for i in range(pat_size):
        print("*", end='')
    print()
    rows += 1

