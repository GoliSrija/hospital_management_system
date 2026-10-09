
# hospital_management_system

AI Generated Project

## Frontend Design

===INDEX_HTML===
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Management System</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="logo">HMS</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="#login">Login</a></li>
                <li><a href="#register">Register</a></li>
            </ul>
        </nav>
    </header>

    <section id="hero">
        <div class="hero-content">
            <h1>Welcome to HMS</h1>
            <p>Efficiently manage your hospital operations.</p>
            <button class="cta-button">Get Started</button>
        </div>
    </section>

    <section id="statistics">
        <div class="stat-card">
            <h2>Patients Served</h2>
            <p>10,000+</p>
        </div>
        <div class="stat-card">
            <h2>Doctors on Board</h2>
            <p>500+</p>
        </div>
        <div class="stat-card">
            <h2>Appointments Booked</h2>
            <p>5,000+</p>
        </div>
    </section>

    <section id="features">
        <div class="feature-card">
            <i class="fas fa-user-md"></i>
            <h3>Doctor Management</h3>
            <p>Manage doctor schedules and availability.</p>
        </div>
        <div class="feature-card">
            <i class="fas fa-calendar-check"></i>
            <h3>Appointment Scheduling</h3>
            <p>Book appointments seamlessly.</p>
        </div>
        <div class="feature-card">
            <i class="

## Backend Design

Backend Technology:
- Flask
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- REST API

Backend Modules:
- Authentication Module
  - User Registration
  - User Login
- User Management
  - Patient Management
  - Doctor Management
- AI Project Generation
  - Generate AI Projects
- Project History
  - View Project History
- Download Module
  - Download Project Files
- Database Module
  - CRUD Operations for Patients
  - CRUD Operations for Appointments
  - CRUD Operations for MedicalRecords
  - CRUD Operations for Inventory

Folder Structure:
```
backend/
- app.py
- config.py
- models/
  - __init__.py
  - patient.py
  - appointment.py
  - medicalrecord.py
  - inventory.py
- routes/
  - auth_routes.py
  - user_routes.py
  - ai_routes.py
  - project_routes.py
  - download_routes.py
  - database_routes.py
- services/
  - auth_service.py
  - user_service.py
  - ai_service.py
  - project_service.py
- agents/
  - ai_agent.py
- orchestrator/
  - project_orchestrator.py
```

REST API Endpoints:
Authentication:
- POST /api/auth/register
- POST /api/auth/login

AI Services:
- POST /api/ai/generate

Project Services:
- GET /api/projects
- GET /api/projects/<id>
- DELETE /api/projects/<id>

User Management:
- GET /api/users/patients
- GET /api/users/patients/<id>
- PUT /api/users/patients/<id>
- DELETE /api/users/patients/<id>
- GET /api/users/doctors
- GET /api/users/doctors/<id>
- PUT /api/users/doctors/<id>
- DELETE /api/users/doctors/<id>

Database Operations:
- POST /api/database/patients
- GET /api/database/patients/<id>
- PUT /api/database/patients/<id>
- DELETE /api/database/patients/<id>
- POST /api/database/appointments
- GET /api/database/appointments/<id>
- PUT /api/database/appointments/<id>
- DELETE /api/database/appointments/<id>
- POST /api/database/medicalrecords
- GET /api/database/medicalrecords/<id>
- PUT /api

## Database Design

Database Name:
Hospital Management System

Database Type:
- PostgreSQL

Main Tables:
- Patients
- Appointments
- MedicalRecords
- Inventory

Table Details:

Patients Table:
- PatientID: SERIAL PRIMARY KEY
- FirstName: VARCHAR(50)
- LastName: VARCHAR(50)
- DateOfBirth: DATE
- Gender: CHAR(1)
- PhoneNumber: VARCHAR(20)
- Email: VARCHAR(100)
- Address: TEXT
- MedicalHistory: TEXT
- InsuranceDetails: TEXT

Appointments Table:
- AppointmentID: SERIAL PRIMARY KEY
- PatientID: INTEGER REFERENCES Patients(PatientID)
- DoctorID: INTEGER REFERENCES Doctors(DoctorID)
- AppointmentDate: DATE
- AppointmentTime: TIME
- Status: VARCHAR(20)

MedicalRecords Table:
- RecordID: SERIAL PRIMARY KEY
- PatientID: INTEGER REFERENCES Patients(PatientID)
- RecordDate: DATE
- Notes: TEXT
- Diagnosis: TEXT
- TreatmentPlan: TEXT

Inventory Table:
- ItemID: SERIAL PRIMARY KEY
- ItemName: VARCHAR(100)
- Category: VARCHAR(50)
- Quantity: INTEGER
- SupplierID: INTEGER REFERENCES Suppliers(SupplierID)
- PurchaseDate: DATE
- ExpiryDate: DATE

Primary Keys:
- PatientID in Patients table
- AppointmentID in Appointments table
- RecordID in MedicalRecords table
- ItemID in Inventory table

Foreign Keys:
- PatientID in Appointments table references Patients(PatientID)
- PatientID in MedicalRecords table references Patients(PatientID)
- ItemID in Inventory table references Suppliers(SupplierID)

Relationships:
- One-to-One: Each patient can have one medical record.
- One-to-Many: One doctor can have many appointments, and one appointment is for one patient.
- One-to-Many: One item can be part of many inventories, and one inventory entry is for one item.

Indexes:
- Index on PatientID in Appointments table
- Index on PatientID in MedicalRecords table
- Index on ItemID in Inventory table

Constraints:
- NOT NULL for columns that cannot be empty
- UNIQUE for PatientID to ensure each patient has a unique ID
- FOREIGN KEY constraints to maintain referential integrity

Normalization:
- First Normal Form (1NF): All tables are free from repeating groups.
- Second Normal Form (2NF): All non-key fields are fully function
