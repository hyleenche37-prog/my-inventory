import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Connect to Supabase using secrets (set these in GitHub/Streamlit later)
url: str = st.secrets["https://wnlqacxktltvqrcworoq.supabase.co"]
key: str = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndubHFhY3hrdGx0dnFyY3dvcm9xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNzMzMzIsImV4cCI6MjA4OTk0OTMzMn0.e2cnyFTBpcxwl4onnBcECSib9pUB4UuEhZ-D7TDG_9A"]
supabase: Client = create_client(url, key)

st.title("🚀 Business ERP (Supabase + GitHub)")

# --- INPUT SECTION ---
with st.expander("➕ Add New Daily Entry"):
    with st.form("entry_form"):
        date_input = st.date_input("Select Date")
        item = st.selectbox("Item", ["EGGS", "SMOKY"])
        bought = st.number_input("N.I.B (Qty Bought)", value=0)
        sold = st.number_input("Items Sold", value=0)
        mpesa = st.number_input("MPESA Received", value=0.0)
        cash = st.number_input("Actual Cash Received", value=0.0)
        exp = st.number_input("T. Expenses", value=0.0)
        labour = st.number_input("Labour", value=350.0)
        
        if st.form_submit_button("Submit to Cloud"):
            data = {
                "date": str(date_input), "product_name": item,
                "qty_bought": bought, "qty_sold": sold,
                "mpesa_received": mpesa, "cash_received": cash,
                "expenses": exp, "labour": labour
            }
            supabase.table("daily_records").upsert(data).execute()
            st.success("Synced with Database!")

# --- REPORTING SECTION ---
st.subheader("Business Performance")
response = supabase.table("daily_records").select("*").execute()
if response.data:
    df = pd.DataFrame(response.data)
    
    # Logic from your Excel
    df['Total_BP'] = df['qty_bought'] * 16 # Simplified for example
    df['Total_Sales'] = df['qty_sold'] * 30 
    
    # Show the table
    st.dataframe(df)
    
    # Totals
    total_profit = df['Total_Sales'].sum() - (df['Total_BP'].sum() + df['expenses'].sum() + df['labour'].sum())
    st.metric("Total Profit to Date", f"KES {total_profit:,.2f}")