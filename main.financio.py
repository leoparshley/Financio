import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import sys # For exiting gracefully

def calculate_compound_interest(principal, annual_rate_percent, years, monthly_payment=0, compounds_per_year=12):
    """
    Calculates the year-by-year balance for compound interest.

    Args:
        principal (float): The initial amount of money.
        annual_rate_percent (float): The annual interest rate (as a percentage).
        years (int): The number of years to calculate for.
        monthly_payment (float, optional): The regular monthly payment added. Defaults to 0.
        compounds_per_year (int, optional): How many times interest is compounded per year. Defaults to 12 (monthly).

    Returns:
        tuple: A tuple containing:
            - list: A list of years (0 to `years`).
            - list: A list of corresponding balances at the end of each year.
    """
    if annual_rate_percent < 0 or principal < 0 or years < 0 or monthly_payment < 0:
        print("Error: Principal, rate, years, and monthly payment cannot be negative.")
        return None, None # Indicate error

    if compounds_per_year <= 0:
        print("Error: Compounding frequency must be positive.")
        return None, None # Indicate error

    # Convert annual rate percentage to a decimal rate per compounding period
    # Handle the case where rate is 0 separately to avoid division by zero later
    if annual_rate_percent == 0:
        rate_per_period = 0
    else:
        rate_per_period = (annual_rate_percent / 100.0) / compounds_per_year

    yearly_balances = [principal]
    current_balance = principal
    total_periods = years * compounds_per_year

    periods_calculated = 0
    for year in range(1, years + 1):
        for _ in range(compounds_per_year):
            periods_calculated += 1
            # Calculate interest for the period
            interest = current_balance * rate_per_period
            current_balance += interest
            # Add monthly payment (if any) *after* compounding for the period
            current_balance += monthly_payment

            # Ensure we don't exceed the total number of periods for the final year
            if periods_calculated >= total_periods:
                break

        yearly_balances.append(current_balance)
        # Break outer loop if inner loop already hit the total period limit
        if periods_calculated >= total_periods:
            break

    # Ensure the years list matches the balances list length
    year_list = list(range(years + 1))
    # If calculation stopped early due to periods, trim year list
    if len(yearly_balances) < len(year_list):
         year_list = year_list[:len(yearly_balances)]

    return year_list, yearly_balances

def get_float_input(prompt):
    """Gets positive float input from the user with validation."""
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt):
    """Gets positive integer input from the user with validation."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("Please enter a non-negative whole number.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def main():
    """Main function to run the compound interest calculator."""
    scenarios = [] # List to store results for plotting

    print("--- Compound Interest Calculator ---")

    while True:
        print("\nEnter details for a new scenario:")
        principal = get_float_input("Initial Principal Amount (e.g., 1000): $")
        annual_rate_percent = get_float_input("Annual Interest Rate (e.g., 5 for 5%): % ")
        years = get_int_input("Number of Years (e.g., 10): ")

        monthly_payment = 0.0
        while True:
            add_payment = input("Add regular monthly payments? (yes/no): ").strip().lower()
            if add_payment in ['yes', 'y']:
                monthly_payment = get_float_input("Monthly Payment Amount: $")
                break
            elif add_payment in ['no', 'n']:
                monthly_payment = 0.0
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")

        # --- Calculation ---
        year_list, balance_list = calculate_compound_interest(principal, annual_rate_percent, years, monthly_payment)

        if year_list is None: # Check if calculation failed
             print("Skipping this scenario due to input error.")
        else:
             # --- Store scenario details for plotting ---
             label = f"P=${principal:,.0f}, r={annual_rate_percent}%, Yrs={years}"
             if monthly_payment > 0:
                 label += f", PMT=${monthly_payment:,.0f}/mo"
             scenarios.append({
                 "years": year_list,
                 "balances": balance_list,
                 "label": label,
                 "final_balance": balance_list[-1] # Store final balance for sorting legend
             })
             print(f"Scenario added. Final balance after {years} years: ${balance_list[-1]:,.2f}")


        # --- Ask to add another scenario ---
        while True:
            another = input("\nAdd another scenario to compare? (yes/no): ").strip().lower()
            if another in ['yes', 'y', 'no', 'n']:
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")

        if another in ['no', 'n']:
            break

    # --- Plotting ---
    if not scenarios:
        print("\nNo valid scenarios were calculated. Exiting.")
        sys.exit() # Exit if no scenarios were added

    print("\nGenerating plot...")
    fig, ax = plt.subplots(figsize=(10, 6)) # Create figure and axes object

    # Sort scenarios by final balance for a potentially clearer legend
    scenarios.sort(key=lambda x: x['final_balance'], reverse=True)

    # Plot each scenario
    for scenario in scenarios:
        ax.plot(scenario["years"], scenario["balances"], marker='o', linestyle='-', markersize=4, label=scenario["label"])

    # --- Formatting the plot ---
    ax.set_title('Compound Interest Growth Comparison')
    ax.set_xlabel('Years')
    ax.set_ylabel('Account Balance ($)')

    # Format y-axis to display currency
    formatter = mticker.FormatStrFormatter('$%,.0f') # Show $ sign, comma separator, no decimals
    ax.yaxis.set_major_formatter(formatter)

    ax.legend(title="Scenarios (Highest final balance first)") # Add legend to identify lines
    ax.grid(True, linestyle='--', alpha=0.6) # Add grid for readability
    plt.tight_layout() # Adjust layout to prevent labels overlapping
    plt.show() # Display the plot

    print("\nPlot displayed. Close the plot window to exit the program.")

if __name__ == "__main__":
    main()