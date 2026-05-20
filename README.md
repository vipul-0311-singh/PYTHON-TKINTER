# Hospital Management System (Tkinter + SQLite)

A simple desktop-based Hospital Management System developed using Python’s Tkinter for the graphical user interface and SQLite for local database storage.

The system allows users to manage:

- Patients
- Staff
- Appointments
- Emergency cases

It also provides a live statistics dashboard powered directly from the database.

---

# Features

## Home Dashboard
- Simple and user-friendly interface
- Branding/logo support
- Navigation menu for all sections

## Statistics Overview
Displays real-time counts for:
- Total Patients
- Total Staff
- Total Appointments
- Total Emergency Cases

## Patient Management
- Add patients
- Edit patient records
- Delete patients
- Automatic admission date stamping (`YYYY-MM-DD`)

## Staff Management
- Add staff members
- Store staff roles/designations

## Appointment Management
- Add appointments
- Basic date validation (`YYYY-MM-DD`)
- Store patient and doctor information

## Emergency Case Management
- Add emergency entries
- Store issue description and date
- Basic date validation support

## Database Support
- SQLite-based persistent storage
- Automatically creates database and required tables on first launch

## Image Support
Optional support for:
- `logo.png`
- `image.png`

The application continues running even if images are missing.

---

# Tech Stack

- Python 3.x
- Tkinter (GUI)
- SQLite3 (Database)
- Pillow / PIL (Image handling)

---

# Project Structure

```bash
project-folder/
│
├── main.py
├── hospital.db
├── logo.png
├── image.png
└── README.md
```

### Files Description

| File | Description |
|------|-------------|
| `main.py` | Main application script |
| `hospital.db` | SQLite database (auto-created) |
| `logo.png` | Optional header logo |
| `image.png` | Optional home screen illustration |

---

# Getting Started

## Prerequisites

- Python 3.8+
- pip package manager

---

# Installation

## Clone Repository

```bash
git clone <your-repository-url>
cd your-repository-name
```

## Install Dependencies

```bash
pip install pillow
```

> `tkinter` and `sqlite3` are included with most Python installations.

If Tkinter is missing on Linux:

```bash
sudo apt-get install python3-tk
```

---

# Running the Application

```bash
python main.py
```

On first launch, the system automatically:

- Creates `hospital.db`
- Creates tables:
  - `patients`
  - `staff`
  - `appointments`
  - `emergency`

---

# Optional Assets

Place the following files in the project directory:

| File | Purpose |
|------|---------|
| `logo.png` | Header logo (60×60 recommended) |
| `image.png` | Home screen image (~320×320 recommended) |

If not available, the application skips image loading gracefully.

---

# How to Use

## Patients
1. Enter patient name
2. Click **Add Patient**
3. Select records to edit or delete

## Staff
1. Enter staff name and role
2. Click **Add Staff**

## Appointments
1. Enter:
   - Patient Name
   - Doctor Name
   - Date (`YYYY-MM-DD`)
2. Click **Add Appointment**

## Emergency Cases
1. Enter:
   - Patient Name
   - Issue
   - Date (`YYYY-MM-DD`)
2. Click **Add**

---

# Database Schema

## Patients Table

```sql
patients(
    id INTEGER PRIMARY KEY,
    name TEXT,
    admission_date TEXT
)
```

## Staff Table

```sql
staff(
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT
)
```

## Appointments Table

```sql
appointments(
    id INTEGER PRIMARY KEY,
    patient_name TEXT,
    doctor_name TEXT,
    appointment_date TEXT
)
```

## Emergency Table

```sql
emergency(
    id INTEGER PRIMARY KEY,
    patient_name TEXT,
    issue TEXT,
    date TEXT
)
```

---

# Future Improvements

- Search functionality
- Authentication/Login system
- Billing module
- Prescription management
- Export reports to PDF/Excel
- Improved UI styling
- Appointment reminders

---

# License

This project is open-source and available under the MIT License.

---

# Author
vipul kumar singh

Developed using Python, Tkinter, and SQLite.

