from flask import Flask, request, jsonify, render_template, redirect, url_for,session,flash
import joblib
import numpy as np
import secrets
from models import db, User, Doctor, Feedback, TrainingData # type: ignore # 👈 Import models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate  # Import Flask-Migrate
from flask_sqlalchemy import SQLAlchemy
from app import db

app = Flask(__name__,static_folder='static')
app.secret_key = secrets.token_hex(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heart_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# ✅ Load Model and Preprocessing Objects
try:
    model = joblib.load("heart_disease_model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Error: Model file(s) not found! Ensure they are present in the directory.")
    exit()

# ✅ Helper function for safe encoding
def safe_transform(label_encoder, value):
    if value in label_encoder.classes_:  
        return label_encoder.transform([value])[0]  
    else:
        return 0  
# ✅ Home Route
@app.route('/')
def home():
    return render_template("homepage.html")

# ✅ Prediction Page
@app.route('/prediction')
def prediction():
    return render_template('index.html')

# ✅ Login Page
@app.route('/login')
def login():
    return render_template('login.html')

# Define the missing 'index' route
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/doctors-list', endpoint='doctors')  # Adding endpoint explicitly
def doctors_list():
    return render_template('doctors.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Collect the email and message from the feedback form
        email = request.form['email']
        message = request.form['message']
        
        # Create a new feedback instance
        new_feedback = Feedback(email=email, message=message)
        
        # Add the feedback to the session and commit to the database
        db.session.add(new_feedback)
        db.session.commit()
        
        flash('✅ Feedback submitted successfully!', 'success')  # Success message to the user
        return redirect(url_for('view_feedback'))  # Redirect to home page after submitting feedback
    
    return render_template('feedback.html')  # If GET request, render the feedback form


@app.route('/add_training_data', methods=['POST'])
def add_training_data():
    try:
        new_data = TrainingData(
            age=int(request.form['age']),
            gender=request.form['gender'],
            cholesterol=int(request.form['cholesterol']),
            blood_pressure=int(request.form['blood_pressure']),
            heart_rate=int(request.form['heart_rate']),
            smoking=request.form['smoking'],
            alcohol=request.form['alcohol'],
            exercise=int(request.form['exercise']),
            family_history=request.form['family_history'],
            diabetes=request.form['diabetes'],
            obesity=request.form['obesity'],
            stress=int(request.form['stress']),
            blood_sugar=int(request.form['blood_sugar']),
            angina=request.form['angina'],
            chest_pain=request.form['chest_pain'],
            target=int(request.form['target'])  # Assuming this is a necessary column
        )
        db.session.add(new_data)
        db.session.commit()

        flash('✅ Training data added successfully!', 'success')

        # Redirect to the view_training_data route to show all added data
        return redirect(url_for('view_training_data'))

    except Exception as e:
        flash(f'❌ Failed to add training data: {str(e)}', 'danger')
        return redirect(url_for('admin_login'))  # In case of error, redirect to the admin dashboard



# Route for adding a doctor
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    if request.method == 'POST':
        id_no = request.form['id_no']
        name = request.form['name']
        specialization = request.form['specialization']
        location = request.form['location']

        # Save to DB
        new_doctor = Doctor(id_no=id_no, name=name, specialization=specialization, location=location)
        db.session.add(new_doctor)
        db.session.commit()

        flash('Doctor added successfully!', 'success')

    # Fetch updated data for admin dashboard
    doctors = Doctor.query.all()
    users = User.query.all()
    feedbacks = Feedback.query.all()
    training_data = TrainingData.query.all()

    # Optional: Indicate we want to open the View Doctor tab
    return render_template("admin_login.html", doctors=doctors, users=users, feedbacks=feedbacks, training_data=training_data, open_section="viewDoctorSection")

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "senthilv979@gmail.com" and password == "admin123":
            session['admin'] = True
            flash('✅ Admin login successful!', 'success')
            # After login, show dashboard
        else:
            flash('❌ Invalid credentials, please try again.', 'danger')
            return render_template('admin_login.html')

    # Check if admin is logged in before showing dashboard
    if 'admin' not in session:
        return render_template('admin_login.html')

    users = User.query.all()
    doctors = Doctor.query.all()
    training_data = TrainingData.query.all()
    feedbacks = Feedback.query.all()

    return render_template('admin_login.html',
                           users=users,
                           doctors=doctors,
                           training_data=training_data,
                           feedbacks=feedbacks)

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))



@app.route('/view_users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@app.route('/view_doctors')
def view_doctors():
    doctors = Doctor.query.all()
    return render_template('view_doctor.html', doctors=doctors)


@app.route('/view_training_data')
def view_training_data():
    training_data = TrainingData.query.all()
    return render_template('view_training_data.html', training_data=training_data)

@app.route('/view_feedback')
def view_feedback():
    # Fetch the feedback from your database
    feedback_list = Feedback.query.all()  # Replace with your actual function to fetch feedback
    return render_template('view_feedback.html', feedbacks=feedback_list)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not registered. Please register first.", "error")
            return redirect(url_for('user_login'))

        if user.password != password:
            flash("Incorrect password. Try again.", "error")
            return redirect(url_for('user_login'))

        # Set session for the logged-in user
        session['user_id'] = user.id
        session['user_email'] = user.email
        flash("Login successful!", "success")
        return redirect(url_for('user_login'))
    return render_template('user_login.html')

# ✅ Abstract Page
@app.route('/abstract')
def abstract():
    return render_template('abstract.html')

# ✅ Future Scope Page
@app.route('/future_scope')
def future_scope():
    return render_template('future_scope.html')

# ✅ Model Accuracy Page
@app.route('/model_accuracy')
def model_accuracy():
    return render_template('model_accuracy.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        print("✅ Received data:", data)  # Debugging line

        if not data:
            return jsonify({"error": "No data received"}), 400

        features = [
            float(data['Age']),
            safe_transform(label_encoders['Gender'], data['Gender']),
            float(data['Cholesterol']),
            float(data['Blood_Pressure']),
            float(data['Heart_Rate']),
            safe_transform(label_encoders['Smoking'], data['Smoking']),
            safe_transform(label_encoders['Alcohol Intake'], data['Alcohol_Intake']),
            safe_transform(label_encoders['Family History'], data['Family_History']),
            safe_transform(label_encoders['Diabetes'], data['Diabetes']),
            float(data['Exercise_Hours']),
            safe_transform(label_encoders['Obesity'], data['Obesity']),
            float(data['Stress_Level']),
            float(data['Blood_Sugar']),
            safe_transform(label_encoders['Exercise Induced Angina'], data['Exercise_Induced_Angina']),
            safe_transform(label_encoders['Chest Pain Type'], data['Chest_Pain_Type']),
        ]

        features = np.array(features).reshape(1, -1)
        features = scaler.transform(features)

        prediction = model.predict(features)[0]

        emoji = "😞" if prediction == 1 else "😀"
        message = "Heart Disease Detected 😞" if prediction == 1 else "No Heart Disease 😀"
        advice = np.random.choice([
            "Maintain a balanced diet rich in fruits and vegetables.",
            "Exercise regularly for at least 30 minutes a day.",
            "Avoid smoking and limit alcohol intake.",
            "Manage stress through meditation or yoga.",
            "Regular health checkups are recommended."
        ])
        accuracy = "85%"  

        return render_template("result.html", message=message, emoji=emoji, advice=advice, accuracy=accuracy)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Doctor List Data
doctors = [
    {"id": 1, "name": "Dr. A Kumar", "specialization": "Cardiologist", "location": "Chennai"},
    {"id": 2, "name": "Dr. B Sharma", "specialization": "General Physician", "location": "Bangalore"},
    {"id": 3, "name": "Dr. C Reddy", "specialization": "Diabetologist", "location": "Hyderabad"},
]

@app.route('/doctors')
def doctors_list():
    doctor = Doctor.query.all()
    print("✅ Doctors Data:", doctors)
    return render_template("doctors.html", doctors=doctors)

@app.route('/book_appointment/<int:doctor_id>')
def book_appointment(doctor_id):
    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if not doctor:
        return "Doctor not found", 404
    return render_template("appointment.html", doctor=doctor)

@app.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    date = request.form.get("date")
    time = request.form.get("time")
    doctor_name = request.form.get("doctor_name")

    return render_template("confirmation.html", name=name, email=email, phone=phone, date=date, time=time, doctor_name=doctor_name)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()  

        features = [
            float(data['Age']),
            safe_transform(label_encoders['Gender'], data['Gender']),
            float(data['Cholesterol']),
            float(data['Blood_Pressure']),
            float(data['Heart_Rate']),
            safe_transform(label_encoders['Smoking'], data['Smoking']),
            safe_transform(label_encoders['Alcohol Intake'], data['Alcohol_Intake']),
            safe_transform(label_encoders['Family History'], data['Family_History']),
            safe_transform(label_encoders['Diabetes'], data['Diabetes']),
            float(data['Exercise_Hours']),
            safe_transform(label_encoders['Obesity'], data['Obesity']),
            float(data['Stress_Level']),
            float(data['Blood_Sugar']),
            safe_transform(label_encoders['Exercise Induced Angina'], data['Exercise_Induced_Angina']),
            safe_transform(label_encoders['Chest Pain Type'], data['Chest_Pain_Type']),
        ]

        features = np.array(features).reshape(1, -1)
        features = scaler.transform(features)

        prediction = model.predict(features)[0]

        response = {
            "prediction": int(prediction),
            "emoji": "😞" if prediction == 1 else "😀",
            "message": "Heart Disease Detected 😞" if prediction == 1 else "No Heart Disease 😀",
            "advice": np.random.choice([
                "Maintain a balanced diet rich in fruits and vegetables.",
                "Exercise regularly for at least 30 minutes a day.",
                "Avoid smoking and limit alcohol intake.",
                "Manage stress through meditation or yoga.",
                "Regular health checkups are recommended."
            ]),
            "accuracy": "85%"
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
