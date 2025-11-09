from django.utils import timezone 
from django.db import models
import joblib
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class Prediction(models.Model):  # Changed from IrisMeasurement to Prediction
    # Input features
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    
    # Prediction results
    prediction = models.CharField(max_length=50)  # ML prediction
    confidence = models.FloatField()

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    prediction_type = models.CharField(max_length=10, choices=[
        ('form', 'Form Submission'),
        ('api', 'API Call'),
    ], default='form')
    
    def __str__(self):
        return f"{self.prediction} ({self.confidence:.2%}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
    
    SPECIES_CHOICES = [
        ('setosa', 'Setosa'),
        ('versicolor', 'Versicolor'),
        ('virginica', 'Virginica'),
    ]
    
    def predict_species(self):
        """Use the trained model to predict species"""
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
            model = joblib.load(model_path)
            
            # Prepare input features
            features = np.array([[self.sepal_length, self.sepal_width, 
                                self.petal_length, self.petal_width]])
            
            # Make prediction
            prediction = model.predict(features)[0]
            species_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
            
            self.prediction = species_map[prediction]
            self.save()
            
            return self.prediction
        except FileNotFoundError:
            return "Model not trained yet"

class MLModel(models.Model):
    name = models.CharField(max_length=100)
    model_file = models.FileField(upload_to='ml_models/')
    accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    
    @classmethod
    def train_new_model(cls):
        """Class method to train and save a new model"""
        iris = load_iris()
        X = iris.data
        y = iris.target
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)
        
        # Save model to file
        model_path = 'iris_model.joblib'
        joblib.dump(model, model_path)
        
        # Create or update MLModel instance
        ml_model, created = cls.objects.get_or_create(name='Iris Classifier')
        ml_model.accuracy = accuracy
        ml_model.is_active = True
        ml_model.save()
        
        return ml_model
    
    def __str__(self):
        return f"{self.name} (Accuracy: {self.accuracy:.2f})"