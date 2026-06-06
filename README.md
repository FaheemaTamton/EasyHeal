#  EasyHeal – Multimodal AI Prescription Understanding System

EasyHeal is an AI-powered healthcare web application designed to digitize and understand handwritten medical prescriptions using Vision Language Models (VLMs).

The system extracts medicine-related information directly from prescription images and converts them into structured, manageable healthcare data. It also generates medicine reminder alarms for patients based on dosage and intake schedules.

Built using Django, HTML, CSS, JavaScript, and locally hosted AI models through LM Studio.

---

#  Features

##  Patient Management
- Add and manage patient profiles
- Store patient medical details
- Upload patient photos
- Guardian information support


##  Prescription Understanding
- Upload handwritten prescription images
- AI-powered medicine extraction
- Detects:
  - Medicine names
  - Dosage
  - Intake frequency
  - Food instructions
  - Duration

##  Multimodal AI Integration
- Uses Vision Language Models (VLMs)
- Local AI inference using LM Studio
- Prescription understanding without traditional OCR pipelines

##  Medicine Alarm System
- Automatically generates medicine reminder schedules
- Smart intake timing generation
- Snooze functionality
- Mark medicines as taken

##  Authentication System
- User registration/login
- Session management
- Profile management

##  Structured Healthcare Data
- Prescriptions stored in database
- Medicines linked to patients
- Alarm tracking system
- Prescription history management

---

#  System Workflow

```text
User Uploads Prescription Image
                ↓
Image Preprocessing
                ↓
Vision Language Model (VLM)
                ↓
AI Extracts Medicine Information
                ↓
Structured Medicine Data Parsing
                ↓
Database Storage
                ↓
Automatic Alarm Generation
                ↓
Patient Medicine Tracking
```

---

#  AI Pipeline

Unlike traditional OCR-based systems, EasyHeal uses a multimodal Vision Language Model pipeline.

The uploaded prescription image is:
1. Preprocessed for clarity
2. Sent to a VLM through LM Studio
3. Parsed into structured JSON data
4. Stored into the healthcare management system

This allows the system to better understand:
- Handwritten prescriptions
- Medical abbreviations
- Dosage patterns
- Intake schedules

---

#  Tech Stack

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Django
- Python

## AI / ML
- Vision Language Models (VLM)
- LM Studio

## Database
- SQLite3

---

#  Project Structure

```bash
EasyHeal/
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   └── templates/
│
├── vlm/
│   ├── service.py
│   ├── parser.py
│   └── preprocess.py
│
├── static/
├── media/
├── templates/
├── manage.py
└── requirements.txt
```

---

# Core Functionalities

## 📌 Prescription Processing
- Upload prescription image
- AI extracts medicine details
- Structured medicine creation
- Prescription finalization workflow

## 📌 Medicine Management
- Dosage tracking
- Intake pattern management
- Duration scheduling
- Food instruction support

## 📌 Alarm Generation
Automatically creates alarms based on:
- Once daily medicines
- Twice daily medicines
- Three times daily medicines

---

#  Authentication Features

- User registration
- Login/logout system
- Persistent sessions
- User profile management

---


#  Project Goals

EasyHeal aims to reduce medication errors and simplify prescription understanding through AI-powered healthcare automation.

The project focuses on:
- Healthcare accessibility
- Prescription digitization
- Patient medication management
- AI-assisted healthcare systems

---

#  Developer

**Faheema Tamton**

AI & ML Engineer

Focused on AI-powered healthcare and intelligent systems.

🔗 Portfolio


---

# License

This project is developed for educational and portfolio purposes.
