from main import app, db, User, Doctor, Patient
import os

# Remove old database
if os.path.exists('hospital.db'):
    os.remove('hospital.db')

with app.app_context():
    db.create_all()
    
    # Create admin
    admin = User(username='admin', email='admin@hospital.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    # Verify initial state
    print("=== DATABASE INITIALIZED ===")
    print(f"Total Users: {User.query.count()}")
    print(f"Total Doctors: {Doctor.query.count()}")
    print(f"Total Patients: {Patient.query.count()}")
    print("\n✓ Database ready for registration testing!")
