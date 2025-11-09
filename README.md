# Iris Classification Django App

A machine learning web application built with Django that classifies Iris flowers into three species based on their measurements.

## Features

- 🌿 **Iris Species Prediction**: ML model to predict Setosa, Versicolor, or Virginica
- 📊 **Database Storage**: All predictions are stored in PostgreSQL/SQLite
- 🔌 **REST API**: JSON API for programmatic access
- 🎯 **Model Training**: Web interface to retrain the ML model
- 📈 **Prediction History**: View all past predictions

## Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML, CSS, JavaScript
- **ML**: Scikit-learn, Random Forest
- **Database**: SQLite/PostgreSQL
- **Deployment**: Ready for production

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jameslorry666/Django-Iris-App.git
cd Django-Iris-App
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
