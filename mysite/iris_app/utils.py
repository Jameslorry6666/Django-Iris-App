import joblib
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

def get_trained_model():
    """Get the trained model, training if necessary"""
    model_path = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
    
    if not os.path.exists(model_path):
        return train_and_save_model()[0]  # Return just the model
    
    return joblib.load(model_path)

def train_and_save_model():
    """Train and save the model, return model, accuracy and path"""
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    model_path = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
    joblib.dump(model, model_path)
    
    accuracy = model.score(X_test, y_test)
    
    return model, accuracy, model_path

def predict_iris_features(sepal_length, sepal_width, petal_length, petal_width):
    """Make prediction using the trained model"""
    model = get_trained_model()
    features = [[sepal_length, sepal_width, petal_length, petal_width]]
    prediction = model.predict(features)[0]
    species_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    return species_map[prediction]