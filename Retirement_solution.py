import math

def calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years):
    # Calculate future monthly expense adjusted for inflation
    future_monthly_expense = monthly_expense * ((1 + inflation_rate / 100) ** years_until_retirement)
    # Annual expense during retirement
    annual_expense = future_monthly_expense * 12
    # Total retirement corpus needed
    corpus_needed = 0
    for year in range(post_retirement_years):
        corpus_needed += annual_expense / ((1 + inflation_rate / 100) ** year)
    return corpus_needed

def simulate_swp(corpus, swp_amount, return_rate, years):
    balance = corpus
    monthly_return = (1 + return_rate / 100) ** (1/12) - 1
    results = []
    for month in range(1, years * 12 + 1):
        interest = balance * monthly_return
        balance += interest
        balance -= swp_amount
        results.append((month, balance))
        if balance <= 0:
            break
    return results

def main():
    while True:
        print("\n===== Retirement & SWP Calculator =====")
        print("1. Calculate Retirement Corpus Needed")
        print("2. Simulate SWP Plan")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            monthly_expense = float(input("Enter current monthly expense (INR): "))
            years_until_retirement = int(input("Years left until retirement: "))
            inflation_rate = float(input("Expected annual inflation rate (%): "))
            post_retirement_years = int(input("Expected number of years in retirement: "))

            corpus = calculate_retirement_corpus(monthly_expense, years_until_retirement, inflation_rate, post_retirement_years)
            print(f"\nEstimated Retirement Corpus Required: ₹{corpus:,.2f}")

        elif choice == '2':
            corpus = float(input("Enter current retirement corpus (INR): "))
            swp_amount = float(input("Enter monthly withdrawal (SWP) amount (INR): "))
            return_rate = float(input("Expected annual return on investment during retirement (%): "))
            years = int(input("Number of years to simulate: "))

            swp_schedule = simulate_swp(corpus, swp_amount, return_rate, years)
            for month, balance in swp_schedule:
                print(f"Month {month}: Balance = ₹{balance:,.2f}")
            if swp_schedule[-1][1] <= 0:
                print("\nWarning: Your retirement corpus will be exhausted by month", swp_schedule[-1][0])

        elif choice == '3':
            print("Exiting the calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
