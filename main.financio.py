import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

def calculate_compound_interest(principal, annual_rate_percent, years, monthly_payment=0, compounds_per_year=12):
    if annual_rate_percent < 0 or principal < 0 or years < 0 or monthly_payment < 0:
        return None, None

    if compounds_per_year <= 0:
        return None, None

    rate_per_period = (annual_rate_percent / 100.0) / compounds_per_year if annual_rate_percent > 0 else 0

    yearly_balances = [principal]
    current_balance = principal
    total_periods = years * compounds_per_year
    periods_calculated = 0

    for year in range(1, years + 1):
        for _ in range(compounds_per_year):
            periods_calculated += 1
            interest = current_balance * rate_per_period
            current_balance += interest + monthly_payment
            if periods_calculated >= total_periods:
                break
        yearly_balances.append(current_balance)
        if periods_calculated >= total_periods:
            break

    year_list = list(range(len(yearly_balances)))
    return year_list, yearly_balances

st.title("Compound Interest Calculator")

scenarios = []
num_scenarios = st.number_input("How many scenarios do you want to compare?", min_value=1, max_value=5, value=1)

for i in range(num_scenarios):
    st.subheader(f"Scenario {i+1}")
    principal = st.number_input(f"Principal Amount for Scenario {i+1}", min_value=0.0, value=1000.0)
    annual_rate = st.number_input(f"Annual Interest Rate (%) for Scenario {i+1}", min_value=0.0, value=5.0)
    years = st.number_input(f"Number of Years for Scenario {i+1}", min_value=1, value=10)
    monthly_payment = st.number_input(f"Monthly Payment Amount for Scenario {i+1}", min_value=0.0, value=0.0)

    years_list, balances = calculate_compound_interest(principal, annual_rate, years, monthly_payment)
    if years_list:
        scenarios.append({
            "years": years_list,
            "balances": balances,
            "label": f"P=${principal:,.0f}, r={annual_rate}%, Yrs={years}" + (f", PMT=${monthly_payment:,.0f}/mo" if monthly_payment > 0 else ""),
            "final_balance": balances[-1]
        })

if scenarios:
    st.subheader("Compound Interest Growth Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))

    scenarios.sort(key=lambda x: x['final_balance'], reverse=True)
    for scenario in scenarios:
        ax.plot(scenario["years"], scenario["balances"], marker='o', label=scenario["label"])

    ax.set_title('Compound Interest Growth Comparison')
    ax.set_xlabel('Years')
    ax.set_ylabel('Account Balance ($)')
    formatter = mticker.FormatStrFormatter('$%,.0f')
    ax.yaxis.set_major_formatter(formatter)
    ax.legend(title="Scenarios")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)