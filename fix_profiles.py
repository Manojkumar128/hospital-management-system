from main import app, db, User, Doctor, Patient

with app.app_context():
    # Check if doctor/patient profiles exist
    venkatesh = User.query.filter_by(username='Venkatesh29').first()
    abhunav = User.query.filter_by(username='abhunav').first()
    
    print("=== FIXING MISSING PROFILES ===")
    
    if venkatesh and not venkatesh.doctor:
        print(f"Creating Doctor profile for {venkatesh.username}...")
        doctor_profile = Doctor(user_id=venkatesh.id, specialization='General Practice', phone='555-1234')
        db.session.add(doctor_profile)
    
    if abhunav and not abhunav.patient:
        print(f"Creating Patient profile for {abhunav.username}...")
        patient_profile = Patient(user_id=abhunav.id, age=25, gender='Male', blood_type='O+', phone='555-5678')
        db.session.add(patient_profile)
    
    db.session.commit()
    
    print("\n=== UPDATED DATABASE STATE ===")
    print(f"Total Users: {User.query.count()}")
    print(f"Total Doctors: {Doctor.query.count()}")
    print(f"Total Patients: {Patient.query.count()}")
    print("\n=== USER BREAKDOWN ===")
    for u in User.query.all():
        has_doctor = Doctor.query.filter_by(user_id=u.id).first() is not None
        has_patient = Patient.query.filter_by(user_id=u.id).first() is not None
        print(f"{u.username:15} | Role: {u.role:10} | Doctor: {has_doctor} | Patient: {has_patient}")
