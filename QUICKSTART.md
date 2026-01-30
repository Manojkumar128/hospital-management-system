## Quick Start Guide

### Installation

1. **Install Python dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Open in browser**:
   ```
   http://localhost:5000
   ```

### Login Credentials

**Demo Admin Account:**
- Username: `admin`
- Password: `admin123`

### Testing Different Roles

1. **Login with admin account** (demo credentials above)
2. **Create new accounts** by registering with different roles:
   - Patient
   - Doctor
   - Reception
   - Pharmacy

### Features to Try

#### Admin Dashboard
- View system statistics
- Manage users
- Browse all doctors and patients
- Monitor appointments

#### Doctor Dashboard
- View scheduled appointments
- Add prescriptions
- Manage patient information
- Set availability schedule

#### Patient Dashboard
- Book new appointments
- View prescriptions
- Update medical profile
- Check appointment history

#### Reception Dashboard
- Check-in patients
- Manage appointments
- View daily reports
- Search patients

#### Pharmacy Dashboard
- Manage medicine inventory
- Process prescriptions
- Create orders
- View sales reports

### Database

- The app automatically creates `hospital.db` on first run
- Database is SQLite and stored in the project root
- All tables are auto-generated from models

### Customization

#### Change Port
Edit `main.py` line at the bottom:
```python
app.run(debug=True, port=5001)  # Change 5000 to your desired port
```

#### Modify Admin Password
In the Flask shell:
```python
from main import app, db, User
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.set_password('newpassword')
    db.session.commit()
```

### Troubleshooting

**Port 5000 already in use?**
- Change to a different port (e.g., 5001, 8000, 8080)

**Database locked error?**
- Make sure only one instance of the app is running
- Delete `hospital.db` and restart to reset

**Static files not loading?**
- Ensure you're running the app from the project root directory

### Next Steps

1. Customize the theme colors in dashboard HTML files
2. Add more database fields as needed
3. Implement email notifications
4. Add more API endpoints
5. Deploy to a production server

For detailed information, see `README.md`
