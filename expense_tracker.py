import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File to save expenses
FILE = "expenses.csv"

# Categories
CATEGORIES = ["Food", "Rent", "Travel", "Shopping", "Bills", "Entertainment", "Other"]

# Load data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# Sidebar for budget
st.sidebar.header("Budget Settings")
monthly_budget = st.sidebar.number_input("Monthly Budget (₹)", value=15000, step=500)

# Expense Entry
st.header("💸 Expense Tracker")
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", CATEGORIES)
    description = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=1, step=10)
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = {"Date": date, "Category": category, "Description": description, "Amount": amount}
        df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("✅ Expense added!")

# Show data
st.subheader("📊 All Expenses")
st.dataframe(df)

# Summary
total_spent = df["Amount"].sum()
remaining = monthly_budget - total_spent

st.subheader("💰 Summary")
st.write(f"**Total Spent:** ₹{total_spent}")
st.write(f"**Remaining Budget:** ₹{remaining}")

# Category-wise chart
if not df.empty:
    st.subheader("📌 Expenses by Category")
    cat_summary = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    cat_summary.plot.pie(autopct="%.1f%%", ax=ax)
    st.pyplot(fig)
