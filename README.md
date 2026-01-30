# 🏥 Hospital Management System

A comprehensive web-based Hospital Management System with role-based dashboards for different staff members and patients.

## Features

### 📊 Multi-Role Dashboards
- **Admin Dashboard**: System overview, user management, statistics, and reports
- **Doctor Dashboard**: Appointments, patient management, prescriptions, and scheduling
- **Patient Dashboard**: Appointment booking, prescription tracking, medical records, and profile management
- **Reception Dashboard**: Check-in management, appointment scheduling, and daily reports
- **Pharmacy Dashboard**: Inventory management, prescription fulfillment, orders, and sales reports

### 🔐 Authentication & Security
- User registration with role-based access
- Secure login system with password hashing
- Session management
- Role-based access control (RBAC)

### 💾 Database Features
- User accounts with different roles
- Doctor profiles and specializations
- Patient records and medical history
- Appointment scheduling system
- Prescription management
- Medicine inventory tracking

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Additional Libraries**: Flask-CORS, Werkzeug

## Installation & Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
uv sync
```

Or if using pip:

```bash
pip install flask flask-cors flask-sqlalchemy werkzeug
```

### Step 2: Run the Application

```bash
python main.py
```

The application will start on `http://localhost:5000`

### Step 3: Access the System

Open your browser and go to:
```
http://localhost:5000
```

## Default Admin Credentials

```
Username: admin
Password: admin123
```

**Note**: Change these credentials immediately after first login for security.

## User Roles & Access

### 1. **Admin (⚙️)**
   - View system statistics
   - Manage all users
   - View all doctors and patients
   - Monitor all appointments
   - Generate reports

### 2. **Doctor (👨‍⚕️)**
   - View scheduled appointments
   - Manage patient information
   - Create and manage prescriptions
   - Set availability schedule
   - Track patient history

### 3. **Patient (🩺)**
   - Book appointments
   - View medical records
   - Track prescriptions
   - Manage personal health information
   - View appointment history

### 4. **Reception (🎫)**
   - Manage daily appointments
   - Check-in patients
   - Register new patients
   - Generate daily reports
   - Handle patient inquiries

### 5. **Pharmacy (💊)**
   - Manage medicine inventory
   - Process prescriptions
   - Place medicine orders
   - Generate sales reports
   - Track stock levels

## Database Models

### User
- User authentication and role management
- Email and username

### Doctor
- Doctor specialization and contact info
- License information
- Availability status

### Patient
- Patient demographics
- Blood type and medical history
- Contact information

### Appointment
- Links doctor and patient
- Appointment date and time
- Status tracking (scheduled, completed, cancelled)

### Prescription
- Doctor-prescribed medications
- Dosage and duration
- Status tracking (pending, filled, completed)

### MedicineInventory
- Medicine details and quantity
- Unit price and expiry date
- Category classification

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - New user registration
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Dashboard based on user role

### User Profile
- `GET /api/user/profile` - Get current user profile

### Admin APIs
- `GET /api/admin/stats` - Get system statistics
- `GET /api/admin/users` - List all users

### Doctor APIs
- `GET /api/doctor/appointments` - Get doctor's appointments

### Patient APIs
- `GET /api/patient/appointments` - Get patient's appointments
- `GET /api/patient/prescriptions` - Get patient's prescriptions

### Pharmacy APIs
- `GET /api/pharmacy/inventory` - Get medicine inventory
- `GET /api/pharmacy/prescriptions` - Get pending prescriptions

## Project Structure

```
health/
├── main.py                          # Flask application entry point
├── pyproject.toml                   # Project configuration
├── README.md                        # This file
├── hospital.db                      # SQLite database (auto-created)
└── templates/
    ├── login.html                   # Login page
    ├── register.html                # Registration page
    ├── style.css                    # Global styles
    └── dashboards/
        ├── admin_dashboard.html     # Admin dashboard
        ├── doctor_dashboard.html    # Doctor dashboard
        ├── patient_dashboard.html   # Patient dashboard
        ├── reception_dashboard.html # Reception dashboard
        └── pharmacy_dashboard.html  # Pharmacy dashboard
```

## UI/UX Features

### Modern Design
- Gradient color schemes for each role
- Responsive layout (mobile, tablet, desktop)
- Smooth transitions and hover effects
- Intuitive navigation

### Interactive Elements
- Real-time data loading via AJAX
- Form validation
- Status badges and indicators
- Search and filter functionality
- Modal dialogs for additional information

### Dashboard Cards
- Key statistics overview
- Color-coded by role
- Visual hierarchy
- Quick action buttons

## Security Features

- Password hashing with Werkzeug
- Session management
- CSRF protection ready
- SQL injection prevention with ORM
- Role-based access control

## Future Enhancements

- Email notifications
- SMS alerts for appointments
- Payment integration
- Telemedicine support
- Advanced reporting and analytics
- Appointment reminders
- Patient feedback system
- Prescription refill requests
- Automated inventory management

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the `main.py` file:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

### Database Issues
To reset the database:
```python
# In Python shell
from main import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
```

### Missing Dependencies
Ensure all packages are installed:
```bash
pip install -r requirements.txt
```

## Support & Documentation

For additional help or to report issues, please check the code comments and inline documentation.

## License

This project is provided as-is for educational and healthcare management purposes.

---

**Happy managing!** 🏥✨
