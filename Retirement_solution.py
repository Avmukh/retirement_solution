import streamlit as st
import pandas as pd
import locale

# --- Set Locale for INR Formatting ---
try:
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')  # Fallback

def format_inr(amount):
    try:
        return locale.currency(amount, grouping=True)
    except:
        return f"₹{amount:,.2f}"

# --- Page Config ---
st.title("Retirement & SWP Calculator")

# --- Core Functions ---
def calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years):
    future_monthly_expense = monthly_expense * ((1 + inflation_rate / 100) ** years_until_retirement)
    annual_expense = future_monthly_expense * 12
    corpus_needed = sum(annual_expense / ((1 + inflation_rate / 100) ** year) for year in range(post_retirement_years))
    return corpus_needed

def simulate_swp(corpus, swp_amount, return_rate, years):
    balance = corpus
    monthly_return = (1 + return_rate / 100) ** (1/12) - 1
    results = []
    for month in range(1, years * 12 + 1):
        interest = balance * monthly_return
        balance += interest - swp_amount
        results.append((month, balance))
        if balance <= 0:
            break
    return results

# --- Tabs ---
tab1, tab2 = st.tabs(["Retirement Corpus", "SWP Simulation"])

with tab1:
    st.header("Retirement Corpus Estimator")
    monthly_expense = st.number_input("Current Monthly Expense (INR)", value=30000.0)
    years_until_retirement = st.number_input("Years Until Retirement", value=20)
    inflation_rate = st.number_input("Expected Inflation Rate (%)", value=6.0)
    post_retirement_years = st.number_input("Expected Years in Retirement", value=25)

    if st.button("Calculate Corpus"):
        corpus = calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years)
        st.success(f"Estimated Retirement Corpus Required: {format_inr(corpus)}")

with tab2:
    st.header("SWP Simulator")
    corpus = st.number_input("Retirement Corpus (INR)", value=1_00_00_000.0)
    swp_amount = st.number_input("Monthly SWP Amount (INR)", value=40000.0)
    return_rate = st.number_input("Expected Annual Return Rate (%)", value=8.0)
    years = st.number_input("Years to Simulate", value=30)

    if st.button("Simulate SWP"):
        results = simulate_swp(corpus, swp_amount, return_rate, int(years))
        df = pd.DataFrame(results, columns=["Month", "Balance"])

        st.write("**SWP Simulation Results**")
        st.line_chart(df.set_index("Month"))

        df["Year"] = ((df["Month"] - 1) // 12) + 1
        yearly_df = df.groupby("Year")["Balance"].last().reset_index()

        st.write("**Year-End Balances**")
        st.bar_chart(yearly_df.set_index("Year"))

        if not df.empty and df.iloc[-1]['Balance'] <= 0:
            st.warning(f"Corpus exhausted in month {df.iloc[-1]['Month']}")

        df["Formatted Balance"] = df["Balance"].apply(format_inr)
        st.dataframe(df[["Month", "Formatted Balance"]])

# --- Footer ---
st.markdown(
    "<hr style='margin-top:40px;'><div style='text-align:center;'>Made with ❤️ by <b>Sri AvMukh (Avik Mukherjee) </b></div>",
    unsafe_allow_html=True
)
