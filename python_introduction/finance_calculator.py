# calculate and provide feedback on a user’s monthly savings 
# and potential future savings without applying conditional statements.

#    User Input for Financial Details:
# Prompt the user for their monthly income: “Enter your monthly income: ”.
income = int(input("Enter your monthly income: "))

# Ask for their total monthly expenses: “Enter your total monthly expenses: ”.
expenses = int(input("Enter your monthly expenses: "))

# Calculate Monthly Savings:
savings = income - expenses

#    Project Annual Savings: Assume a simple annual interest rate of 5%.
projected_savings = int(savings * 12 + (savings * 12 * 0.05))

#Output Results:Your monthly savings are $1000.
#Projected savings after one year, with interest, is: $12600.

#        Display the user’s monthly savings.
print("Your monthly savings are ${}.".format(savings))
#        Display the projected annual savings after including interest.
print("Projected savings after one year, with interest, is: ${}.".format(projected_savings))

#
