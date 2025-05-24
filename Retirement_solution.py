import streamlit as st
import pandas as pd
from babel.numbers import format_currency

# --- Helper for INR Formatting ---
def format_inr(amount):
    try:
        return format_currency(amount, 'INR', locale='en_IN')
    except:
        return f"₹{amount:,.2f}"
    
# --- Page Config ---
st.set_page_config(page_title="Retirement & SWP Calculator", layout="centered")
st.title("🧓 Retirement & SWP Calculator")

# --- Core Functions ---
def calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years):
    future_monthly_expense = monthly_expense * ((1 + inflation_rate / 100) ** years_until_retirement)
    annual_expense = future_monthly_expense * 12
    corpus_needed = sum(annual_expense / ((1 + inflation_rate / 100) ** year) for year in range(post_retirement_years))
    return corpus_needed

def simulate_swp(corpus, swp_amount, return_rate, years):
    balance = corpus
    monthly_return = (1 + return_rate / 100) ** (1 / 12) - 1
    results = []
    for month in range(1, int(years * 12) + 1):
        interest = balance * monthly_return
        balance += interest - swp_amount
        results.append((month, balance))
        if balance <= 0:
            break
    return results

# --- Tabs ---
tab1, tab2 = st.tabs(["📈 Retirement Corpus", "💸 SWP Simulation"])

# --- Retirement Corpus Tab ---
with tab1:
    st.header("Estimate Required Retirement Corpus")

    monthly_expense = st.number_input("Current Monthly Expense (INR)", value=30000.0, step=1000.0)
    years_until_retirement = st.number_input("Years Until Retirement", value=20)
    inflation_rate = st.number_input("Expected Inflation Rate (%)", value=6.0, step=0.5)
    post_retirement_years = st.number_input("Years Expected After Retirement", value=25)

    if st.button("Calculate Corpus"):
        corpus = calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years)
        st.success(f"Estimated Retirement Corpus Required: {format_inr(corpus)}")

# --- SWP Simulation Tab ---
with tab2:
    st.header("Simulate Systematic Withdrawal Plan (SWP)")

    corpus = st.number_input("Initial Corpus (INR)", value=1_00_00_000.0, step=1_00_000.0)
    swp_amount = st.number_input("Monthly Withdrawal (INR)", value=40000.0, step=1000.0)
    return_rate = st.number_input("Expected Annual Return (%)", value=8.0, step=0.5)
    years = st.number_input("Simulation Duration (Years)", value=30)

    if st.button("Run SWP Simulation"):
        results = simulate_swp(corpus, swp_amount, return_rate, years)
        df = pd.DataFrame(results, columns=["Month", "Balance"])

        if df.empty:
            st.error("Corpus exhausted immediately. Try reducing the SWP amount.")
        else:
            st.write("📉 Monthly Balance Over Time")
            st.line_chart(df.set_index("Month"))

            df["Year"] = ((df["Month"] - 1) // 12) + 1
            yearly_df = df.groupby("Year")["Balance"].last().reset_index()

            st.write("📊 Year-End Corpus Balance")
            st.bar_chart(yearly_df.set_index("Year"))

            if df.iloc[-1]["Balance"] <= 0:
                st.warning(f"⚠️ Corpus exhausted in month {df.iloc[-1]['Month']}.")

            df["Formatted Balance"] = df["Balance"].apply(format_inr)
            st.dataframe(df[["Month", "Formatted Balance"]])

# --- Footer ---
st.markdown(
    "<hr style='margin-top:40px;'><div style='text-align:center;'>"
    "Made with ❤️ by <b>Sri AvMukh (Avik Mukherjee)</b></div>",
    unsafe_allow_html=True
)
