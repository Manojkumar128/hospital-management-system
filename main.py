"""Hospital Management System - Flask Application"""
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, patient, reception, pharmacy
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    license_number = db.Column(db.String(50))
    available = db.Column(db.Boolean, default=True)
    user = db.relationship('User', backref='doctor')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(5))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(255))
    medical_history = db.Column(db.Text)
    user = db.relationship('User', backref='patient')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    medication = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, filled, completed
    patient = db.relationship('Patient', backref='prescriptions')
    doctor = db.relationship('Doctor', backref='prescriptions')

class MedicineInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float)
    expiry_date = db.Column(db.DateTime)
    category = db.Column(db.String(100))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# Routes - Authentication
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.check_password(data.get('password')):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return jsonify({'success': True, 'role': user.role})
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        role = data.get('role', 'patient')
        
        # Validate input
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Check for duplicate username
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists. Please choose a different username.'}), 400
        
        # Check for duplicate email
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered. Please use a different email or login.'}), 400
        
    
        user = User(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.flush()  # Get the user ID without committing
            
            # Auto-create Doctor or Patient profile
            if role == 'doctor':
                doctor = Doctor(user_id=user.id, specialization='General Practice', phone='N/A')
                db.session.add(doctor)
            elif role == 'patient':
                patient = Patient(user_id=user.id, age=0, gender='N/A', blood_type='N/A', phone='N/A')
                db.session.add(patient)
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Registration failed. Please try again.'}), 400
    return render_template('register.html')

# Routes - Dashboards
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    if role == 'admin':
        return render_template('dashboards/admin_dashboard.html')
    elif role == 'doctor':
        return render_template('dashboards/doctor_dashboard.html')
    elif role == 'patient':
        return render_template('dashboards/patient_dashboard.html')
    elif role == 'reception':
        return render_template('dashboards/reception_dashboard.html')
    elif role == 'pharmacy':
        return render_template('dashboards/pharmacy_dashboard.html')
    
    return redirect(url_for('login'))

# API Routes - Common
@app.route('/api/user/profile')
def get_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })

# API Routes - Admin
@app.route('/api/admin/stats')
def admin_stats():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'total_users': User.query.count(),
        'total_doctors': Doctor.query.count(),
        'total_patients': Patient.query.count(),
        'total_appointments': Appointment.query.count()
    })

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role,
        'created_at': u.created_at.isoformat()
    } for u in users])

# API Routes - Doctor
@app.route('/api/doctor/appointments')
def doctor_appointments():
    if session.get('role') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401
    
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    if not doctor:
        return jsonify({'appointments': []})
    
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return jsonify({
        'appointments': [{
            'id': a.id,
            'patient_name': a.patient.user.username,
            'date': a.appointment_date.isoformat(),
            'reason': a.reason,
            'status': a.status
        } for a in appointments]
    })

# API Routes - Patient
@app.route('/api/patient/appointments')
def patient_appointments():
    if session.get('role') != 'patient':
        return jsonify({'error': 'Unauthorized'}), 401
    
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    if not patient:
        return jsonify({'appointments': []})
    
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    return jsonify({
        'appointments': [{
            'id': a.id,
            'doctor_name': a.doctor.user.username,
            'date': a.appointment_date.isoformat(),
            'reason': a.reason,
            'status': a.status
        } for a in appointments]
    })

@app.route('/api/patient/prescriptions')
def patient_prescriptions():
    if session.get('role') != 'patient':
        return jsonify({'error': 'Unauthorized'}), 401
    
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    if not patient:
        return jsonify({'prescriptions': []})
    
    prescriptions = Prescription.query.filter_by(patient_id=patient.id).all()
    return jsonify({
        'prescriptions': [{
            'id': p.id,
            'medication': p.medication,
            'dosage': p.dosage,
            'duration': p.duration,
            'status': p.status,
            'created_at': p.created_at.isoformat()
        } for p in prescriptions]
    })

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get list of available doctors"""
    doctors = Doctor.query.filter_by(available=True).all()
    return jsonify({
        'doctors': [{
            'id': d.id,
            'name': d.user.username,
            'specialization': d.specialization,
            'phone': d.phone or 'N/A'
        } for d in doctors]
    })

@app.route('/api/patient/book-appointment', methods=['POST'])
def book_appointment():
    """Book an appointment for a patient"""
    if session.get('role') != 'patient':
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    
    if not patient:
        return jsonify({'error': 'Patient profile not found'}), 404
    
    try:
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=data.get('doctor_id'),
            appointment_date=datetime.fromisoformat(data.get('appointment_date')),
            reason=data.get('reason'),
            status='scheduled'
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Appointment booked successfully!', 'appointment_id': appointment.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# API Routes - Pharmacy
@app.route('/api/pharmacy/inventory')
def pharmacy_inventory():
    if session.get('role') != 'pharmacy':
        return jsonify({'error': 'Unauthorized'}), 401
    
    inventory = MedicineInventory.query.all()
    return jsonify({
        'medicines': [{
            'id': m.id,
            'name': m.name,
            'quantity': m.quantity,
            'unit_price': m.unit_price,
            'category': m.category,
            'expiry_date': m.expiry_date.isoformat() if m.expiry_date else None
        } for m in inventory]
    })

@app.route('/api/pharmacy/prescriptions')
def pharmacy_prescriptions():
    if session.get('role') != 'pharmacy':
        return jsonify({'error': 'Unauthorized'}), 401
    
    prescriptions = Prescription.query.filter_by(status='pending').all()
    return jsonify({
        'prescriptions': [{
            'id': p.id,
            'patient_name': p.patient.user.username,
            'medication': p.medication,
            'dosage': p.dosage,
            'created_at': p.created_at.isoformat()
        } for p in prescriptions]
    })

from main import app, db, User
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.set_password('mama1')
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create sample admin user if doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@hospital.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True, port=5000)
