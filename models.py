from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_no = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)


class TrainingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    cholesterol = db.Column(db.Integer)
    blood_pressure = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    smoking = db.Column(db.String(10))
    alcohol = db.Column(db.String(10))
    exercise = db.Column(db.Integer)
    family_history = db.Column(db.String(10))
    diabetes = db.Column(db.String(10))
    obesity = db.Column(db.String(10))
    stress = db.Column(db.Integer)
    blood_sugar = db.Column(db.Integer)
    angina = db.Column(db.String(10))
    chest_pain = db.Column(db.String(10))
    target = db.Column(db.Integer)

    def __init__(self, age, gender, cholesterol, blood_pressure, heart_rate, smoking, alcohol, exercise, family_history, diabetes, obesity, stress, blood_sugar, angina, chest_pain, target):
        self.age = age
        self.gender = gender
        self.cholesterol = cholesterol
        self.blood_pressure = blood_pressure
        self.heart_rate = heart_rate
        self.smoking = smoking
        self.alcohol = alcohol
        self.exercise = exercise
        self.family_history = family_history
        self.diabetes = diabetes
        self.obesity = obesity
        self.stress = stress
        self.blood_sugar = blood_sugar
        self.angina = angina
        self.chest_pain = chest_pain
        self.target = target
     # Chest pain type

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)  # Add this column
    message = db.Column(db.Text, nullable=False)
    
    def __init__(self, email, message):
        self.email = email
        self.message = message

def get_feedback_from_database():
    # Query the Feedback table to get all feedback records
    feedbacks = Feedback.query.all()
    return feedbacks