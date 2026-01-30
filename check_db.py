from main import app, db, User, Doctor, Patient

with app.app_context():
    print("=== CURRENT DATABASE STATE ===")
    print(f"Total Users: {User.query.count()}")
    print(f"Total Doctors: {Doctor.query.count()}")
    print(f"Total Patients: {Patient.query.count()}")
    print("\n=== USER BREAKDOWN ===")
    for u in User.query.all():
        print(f"{u.username:15} | Role: {u.role:10} | Has Doctor Profile: {u.doctor is not None} | Has Patient Profile: {u.patient is not None}")
