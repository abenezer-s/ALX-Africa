# calculate and provide feedback on a user’s monthly savings and potential future savings

# Prompt the user for their monthly income and expenses
monthly_income = int(input("Enter your monthly income: "))
monthly_expenses = int(input("Enter your monthly expenses: "))

# Calculate Monthly Savings and annual savings
monthly_savings = monthly_income - monthly_expenses
projected_savings = Monthly_Savings * 12 + (Monthly_Savings * 12 * 0.05)

# Display the user’s monthly savings and  the projected annual savings
print("Your monthly savings are ${}".format(monthly_savings))
print("Projected savings after one year, with interest, is: ${}.".format(projected_savings))

