import streamlit as st
import joblib
import pandas as pd

# Load the model
model = joblib.load('/workspaces/ClaxonHack/ml/best_model.joblib')

# Display the app header
st.title('Loan Status Prediction App')

# Display model performance (This is a placeholder, replace with actual model performance metrics)
st.header('Model Performance')
st.write('Accuracy: 0.88')

# User input features
st.header('Make a Prediction')
# Define input fields
interest_rate = st.number_input('Interest Rate', min_value=0.0, format='%f')
loan_amount = st.number_input('Loan Amount', min_value=0.0, format='%f')
outstanding_balance = st.number_input('Outstanding Balance', min_value=0.0, format='%f')
salary = st.number_input('Salary', min_value=0.0, format='%f')
age = st.number_input('Age', min_value=18, max_value=100, step=1)

# Predict button
if st.button('Predict Loan Status'):
    # Make prediction
    features = [interest_rate, loan_amount, outstanding_balance, salary, age]
    prediction = model.predict([features])[0]
    
    # Display prediction
    st.subheader('Prediction')
    st.write('Loan Status:', 'Approved' if prediction == 1 else 'Not Approved')