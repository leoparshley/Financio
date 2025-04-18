import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

def calculate_compound_interest(principal, annual_rate_percent, years, monthly_payment=0, compounds_per_year=12):
    if annual_rate_percent < 0 or principal < 0 or years < 0 or monthly_payment < 0:
        return None, None

    if compounds_per_year <= 0:
        return None, None

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
            interest = current_balance * rate_per_period
            current_balance += interest
            current_balance += monthly_payment
            if periods_calculated >= total_periods:
                break
        yearly_balances.append(current_balance)
        if periods_calculated >= total_periods:
            break

    year_list = list(range(len(yearly_balances)))
    return year_list, yearly_balances

# --- Streamlit UI ---
st.title("Compound Interest Calculator")

num_scenarios = st.number_input("How many scenarios do you want to compare?", min_value=1, max_value=5, value=1, step=1)

scenarios = []

for i in range(num_scenarios):
    st.subheader(f"Scenario {i + 1}")
    principal = st.number_input(f"Principal Amount for Scenario {i + 1}", min_value=0.0, value=1000.0, step=100.0)
    rate = st.number_input(f"Annual Interest Rate (%) for Scenario {i + 1}", min_value=0.0, value=5.0, step=0.1)
    years = st.number_input(f"Number of Years for Scenario {i + 1}", min_value=1, value=10, step=1)
    monthly_payment = st.number_input(f"Monthly Payment Amount for Scenario {i + 1}", min_value=0.0, value=0.0, step=10.0)

    year_list, balance_list = calculate_compound_interest(principal, rate, years, monthly_payment)

    if year_list is not None:
        label = f"P=${principal:,.0f}, r={rate}%, Yrs={years}"
        if monthly_payment > 0:
            label += f", PMT=${monthly_payment:,.0f}/mo"
        scenarios.append({
            "years": year_list,
            "balances": balance_list,
            "label": label,
            "final_balance": balance_list[-1]
        })

# --- Plotting ---
if scenarios:
    scenarios.sort(key=lambda x: x['final_balance'], reverse=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    for scenario in scenarios:
        ax.plot(scenario["years"], scenario["balances"], marker='o', linestyle='-', markersize=4, label=scenario["label"])

    ax.set_title('Compound Interest Growth Comparison')
    ax.set_xlabel('Years')
    ax.set_ylabel('Account Balance ($)')

    # Fixed formatter
    formatter = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    ax.yaxis.set_major_formatter(formatter)

    ax.legend(title="Scenarios")
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    st.pyplot(fig)