# iris_app/ml_model.py
import pandas as pd
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

def train_and_save_model():
    # Load the Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model in the current directory
    model_path = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model trained and saved at: {model_path}")
    
    # Print accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    return model

# Train the model when this file is run
if __name__ == "__main__":
    train_and_save_model()