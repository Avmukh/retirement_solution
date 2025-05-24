import streamlit as st
import pandas as pd
import locale

# --- Locale for INR Formatting ---
try:
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')  # fallback

def format_inr(amount):
    try:
        return locale.currency(amount, grouping=True)
    except:
        return f"₹{amount:,.2f}"

# --- Page Setup ---
st.set_page_config(page_title="Retirement & SWP Planner", layout="centered")
st.title("🧓 Retirement & SWP Calculator")

# --- Tabs ---
tab1, tab2 = st.tabs(["📈 Retirement Corpus", "💸 SWP Simulation"])

# --- Functions ---
def calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years):
    future_expense = monthly_expense * ((1 + inflation_rate / 100) ** years_until_retirement)
    annual_expense = future_expense * 12
    corpus = sum(annual_expense / ((1 + inflation_rate / 100) ** year) for year in range(post_retirement_years))
    return corpus

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

# --- Retirement Corpus ---
with tab1:
    st.subheader("Estimate Retirement Corpus Needed")
    monthly_expense = st.number_input("Current Monthly Expense (INR)", value=30000)
    years_until_retirement = st.number_input("Years Until Retirement", value=20)
    inflation_rate = st.number_input("Expected Inflation Rate (%)", value=6.0)
    post_retirement_years = st.number_input("Years after Retirement", value=25)

    if st.button("Calculate Corpus"):
        corpus = calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years)
        st.success(f"Estimated Corpus Required: {format_inr(corpus)}")

# --- SWP Simulation ---
with tab2:
    st.subheader("Simulate Monthly Withdrawal from Corpus")
    corpus = st.number_input("Starting Corpus (INR)", value=1_00_00_000.)
    swp_amount = st.number_input("Monthly Withdrawal (INR)", value=40000.)
    return_rate = st.number_input("Annual Return Rate (%)", value=8.0)
    years = st.number_input("Simulation Period (Years)", value=30)

    if st.button("Run SWP Simulation"):
        data = simulate_swp(corpus, swp_amount, return_rate, int(years))
        df = pd.DataFrame(data, columns=["Month", "Balance"])

        st.line_chart(df.set_index("Month"))

        df["Year"] = ((df["Month"] - 1) // 12) + 1
        yearly_df = df.groupby("Year")["Balance"].last().reset_index()

        st.bar_chart(yearly_df.set_index("Year"))

        if df.iloc[-1]['Balance'] <= 0:
            st.warning(f"Corpus exhausted in month {df.iloc[-1]['Month']}.")

        df["Formatted Balance"] = df["Balance"].apply(format_inr)
        st.dataframe(df[["Month", "Formatted Balance"]])

# --- Footer ---
st.markdown(
    "<hr style='margin-top:40px;'><div style='text-align:center;'>Made with ❤️ by <b>Sri AvMukh (Avik Mukherjee) </b></div>",
    unsafe_allow_html=True
)
