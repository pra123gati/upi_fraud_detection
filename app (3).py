import streamlit as st
# (Paste the rest of your Streamlit code here)



import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model
model = joblib.load("upi_fraud_model.pkl")

# Transaction type encoding (ensure it matches training data)
transaction_types = {"CASH_OUT": 0, "TRANSFER": 1, "PAYMENT": 2, "DEBIT": 3, "CASH_IN": 4}

# Function to predict fraud
def predict_fraud(data):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return "🚨 Fraud Detected!" if prediction == 1 else "✅ Transaction Safe"

# Streamlit UI
st.title("🔍 UPI Fraud Detection System")

# Input fields
step = st.number_input("📅 Transaction Step (Time)", min_value=0, value=1)
trans_type = st.selectbox("🔄 Transaction Type", list(transaction_types.keys()))
amount = st.number_input("💰 Transaction Amount (INR)", min_value=0.0)
oldbalanceOrg = st.number_input("🏦 Sender's Old Balance", min_value=0.0)
newbalanceOrig = st.number_input("🏦 Sender's New Balance", min_value=0.0)
oldbalanceDest = st.number_input("🏦 Receiver's Old Balance", min_value=0.0)
newbalanceDest = st.number_input("🏦 Receiver's New Balance", min_value=0.0)
isFlaggedFraud = st.radio("⚠️ Is Transaction Flagged?", [0, 1])
balance_diff_sender = oldbalanceOrg - newbalanceOrig
balance_diff_receiver = newbalanceDest - oldbalanceDest

# Predict button
if st.button("Check Fraud"):
    transaction = {
        "step": step,
        "type": transaction_types[trans_type],
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "isFlaggedFraud": isFlaggedFraud,
        "balance_diff_sender": balance_diff_sender,
        "balance_diff_receiver": balance_diff_receiver
    }
    result = predict_fraud(transaction)
    st.write(f"### {result}")
