# calculate and provide feedback on a user’s monthly savings and potential future savings

# Prompt the user for their monthly income and expenses
income = int(input("Enter your monthly income: "))
expenses = int(input("Enter your monthly expenses: "))

# Calculate Monthly Savings and annual savings
savings = income - expenses
projected_savings = savings * 12 + (savings * 12 * 0.05)

# Display the user’s monthly savings and  the projected annual savings
print("Your monthly savings are ${}.".format(savings))
print("Projected savings after one year, with interest, is: ${}.".format(projected_savings))

