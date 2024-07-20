import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from ml.main import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI()

# Define a request body for the inference endpoint
class InferenceRequest(BaseModel):
    features: list

# Placeholder function for training the model
def train_model():
    # Load your dataset
    df = pd.read_csv('data.csv')  # Make sure to replace 'your_dataset.csv' with your actual dataset file
    
    # Select features and target based on your dataset
    selected_features = ['interest_rate', 'loan_amount', 'outstanding_balance', 'salary', 'age']
    X = df[selected_features]
    y = df['Loan Status']  

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the GradientBoostingClassifier
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy with GradientBoostingClassifier: {accuracy}")
    
    # Save the trained model
    joblib.dump(model, 'best_model.joblib')
    pass

# Placeholder function for making predictions
def make_prediction(features):
    # Load the trained model (ensure you have a model saved as 'best_model.joblib')
    model = joblib.load('best_model.joblib')
    prediction = model.predict([features])
    return prediction[0]

@app.post("/train/")
async def train():
    try:
        train_model()
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/", response_model=str)
async def predict(request: InferenceRequest):
    try:
        prediction = make_prediction(request.features)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))