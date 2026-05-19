from django.shortcuts import render, redirect
from .models import Patient
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile

import os
from django.conf import settings
from django.shortcuts import render

from vlm.service import extract_medicine_details
from vlm.parser import parse_vlm_response

from django.urls import reverse
from .models import Patient, Prescription, Medicine, Alarm





def my_account_view(request):

    # ✅ GUARANTEE PROFILE EXISTS (NO CRASH EVER)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # User field
        request.user.email = request.POST.get("email")
        request.user.save()

        # Profile fields
        profile.mobile = request.POST.get("mobile")
        profile.role = request.POST.get("role")
        profile.organization = request.POST.get("organization")
        profile.save()

        return redirect("my_account")

    edit_mode = request.GET.get("edit") == "true"

    return render(request, "my_account.html", {
        "profile": profile,
        "edit_mode": edit_mode,
    })




def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # 🔴 REDIRECT TO HOME
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        mobile = request.POST['mobile']
        role = request.POST['role']
        organization = request.POST['organization']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.get_or_create(
    user=user,
    defaults={
        "mobile": mobile,
        "role": role,
        "organization": organization
    }
)


        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')

def home_view(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'Home.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)
        Patient.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            health_issue=request.POST.get('health_issue'),
            photo=request.FILES.get('photo'),
            guardian_name=request.POST.get("guardian_name"),
            guardian_phone=request.POST.get("guardian_phone")
        )
        return redirect('home')
    return render(request, 'add_patient.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient

from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient

def patient_details(request, id):
    patient = get_object_or_404(Patient, id=id)
    prescriptions = patient.prescriptions.filter(status="FINALIZED").order_by("-created_at")


    # Handle patient update
    if request.method == "POST":
        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.health_issue = request.POST.get("health_issue")
        patient.guardian_name = request.POST.get("guardian_name")
        patient.guardian_phone = request.POST.get("guardian_phone")
        # Optional photo update
        if request.FILES.get("photo"):
            patient.photo = request.FILES.get("photo")

        patient.save()
        return redirect("patient_details", id=patient.id)

    # View or Edit mode toggle
    edit_mode = request.GET.get("edit") == "true"

    return render(request, "patient_details.html", {
        "patient": patient,
        "edit_mode": edit_mode,
        "prescriptions": prescriptions,
    })
  

def expand_intake(code):
    mapping = {
        "QD": "Once a day",
        "OD": "Once a day",
        "BID": "2x a day (Morning, Night)",
        "BD": "2x a day (Morning, Night)",
        "TID": "3x a day (Morning, Noon, Night)",
        "TDS": "3x a day (Morning, Noon, Night)",
        "QID": "4x a day",
    }

    if not code:
        return None

    return mapping.get(code.upper(), code)

from .models import Prescription, Medicine, Patient
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .models import Prescription, Medicine, Patient
from django.shortcuts import get_object_or_404, redirect

def scan_prescription(request):

    if request.method == "POST" and request.FILES.get("prescription"):

        patient_id = request.POST.get("patient_id")
        patient = get_object_or_404(Patient, id=patient_id)

        image = request.FILES["prescription"]

        # Create Prescription linked to Patient
        prescription = Prescription.objects.create(
            patient=patient,
            image=image,
            status="IN_PROGRESS"
        )

        # Run VLM
        raw_output = extract_medicine_details(prescription.image.path)
        medicine_data = parse_vlm_response(raw_output)

        prescription.raw_extracted_data = medicine_data
        prescription.save()

        names = medicine_data.get("medicine_name", [])
        dosages = medicine_data.get("dosage", [])
        foods = medicine_data.get("food_instruction", [])
        intakes = medicine_data.get("intake", [])
        days = medicine_data.get("duration_days", [])

        total = len(names)

        # ✅ Properly indented loop
        for i in range(total):

            raw_intake = intakes[i] if i < len(intakes) else None
            raw_days = days[i] if i < len(days) else None

            # Safe duration handling
            if raw_days is None or raw_days == "":
                safe_days = 1
            else:
                try:
                    safe_days = int(raw_days)
                except:
                    safe_days = 1

            Medicine.objects.create(
                prescription=prescription,
                name=names[i],
                dosage=dosages[i] if i < len(dosages) else None,
                food_instruction=foods[i] if i < len(foods) else None,
                intake_pattern=expand_intake(raw_intake),
                duration_days=safe_days,
            )

        return redirect("medicine_details", prescription_id=prescription.id)

    return redirect("home")


def expand_intake(code):
    mapping = {
        "QD": "Once a day",
        "OD": "Once a day",
        "BID": "2x a day (Morning, Night)",
        "BD": "2x a day (Morning, Night)",
        "TID": "3x a day (Morning, Noon, Night)",
        "TDS": "3x a day (Morning, Noon, Night)",
        "QID": "4x a day",
    }

    if not code:
        return None

    return mapping.get(code.upper(), code)

def medicine_details(request, prescription_id):

    prescription = get_object_or_404(Prescription, id=prescription_id)

    medicines = prescription.medicines.all()

    return render(
        request,
        "medicine_details.html",
        {
            "prescription": prescription,
            "medicines": medicines
        }
    )


from django.http import JsonResponse
from datetime import timedelta, time


def generate_alarm_preview(request, prescription_id):

    prescription = get_object_or_404(Prescription, id=prescription_id)
    medicines = prescription.medicines.all()

    alarms = []

    for med in medicines:

        intake = (med.intake_pattern or "").lower()

        if "once" in intake:
            times = [time(9, 0)]
        elif "2x" in intake or "twice" in intake:
            times = [time(9, 0), time(21, 0)]
        elif "3x" in intake or "3 times" in intake:
            times = [time(8, 0), time(14, 0), time(20, 0)]
        else:
            times = [time(9, 0)]

        duration = med.duration_days or 1
        start_date = prescription.created_at.date()

        for d in range(duration):
            alarm_date = start_date + timedelta(days=d)

            for t in times:
                alarms.append({
                    "medicine_id": med.id,   
                    "medicine": med.name,
                    "dosage": med.dosage,
                    "food": med.food_instruction,
                    "date": alarm_date.strftime("%Y-%m-%d"),
                    "time": t.strftime("%H:%M"),
                })

    return JsonResponse({"alarms": alarms})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime


def save_alarms(request, prescription_id):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    prescription = get_object_or_404(Prescription, id=prescription_id)

    if prescription.status == "FINALIZED":
        return JsonResponse({"error": "Already finalized"}, status=400)

    data = json.loads(request.body)
    alarms = data.get("alarms", [])

    for alarm in alarms:

        medicine_id = alarm.get("medicine_id")
        date_str = alarm.get("date")
        time_str = alarm.get("time")

        if not medicine_id or not date_str or not time_str:
            continue

        try:
            medicine = Medicine.objects.get(
                id=medicine_id,
                prescription=prescription
            )

            alarm_date = datetime.strptime(
                date_str, "%Y-%m-%d"
            ).date()

            alarm_time = datetime.strptime(
                time_str, "%H:%M"
            ).time()

        except Exception:
            continue

        Alarm.objects.create(
            prescription=prescription,
            medicine=medicine,
            alarm_date=alarm_date,
            alarm_time=alarm_time
        )

    prescription.status = "FINALIZED"
    prescription.save()

    return JsonResponse({
        "success": True,
        "redirect_url": reverse(
            "prescription_detail",
            args=[prescription.id]
        )
    })


def prescription_detail(request, prescription_id):

    prescription = get_object_or_404(
        Prescription,
        id=prescription_id
    )

    medicines = prescription.medicines.all()
    alarms = prescription.alarms.all()

    return render(
        request,
        "prescription_detail.html",
        {
            "prescription": prescription,
            "medicines": medicines,
             "alarms": alarms
        }
    )

@csrf_exempt
def update_medicines(request, prescription_id):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    prescription = get_object_or_404(Prescription, id=prescription_id)

    data = json.loads(request.body)
    medicines_data = data.get("medicines", [])

    medicines = prescription.medicines.all()

    for i, med in enumerate(medicines):
        try:
            new_days = medicines_data[i]["duration_days"]
            med.duration_days = int(new_days)
            med.save()
        except:
            continue

    return JsonResponse({"success": True})


#delete button on prescription cards
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Prescription, Patient


@require_POST
def delete_prescription(request, id):

    prescription = get_object_or_404(Prescription, id=id)

    prescription.delete()

    return JsonResponse({
        "success": True
    })


@require_POST
def delete_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    patient.delete()

    return JsonResponse({
        "success": True
    })


#alarm view
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime

def check_alarm(request):

    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    alarm = Alarm.objects.filter(
        alarm_date=today,
        alarm_time__lte=current_time,
        is_taken=False
    ).select_related(
        "medicine",
        "prescription",
        "prescription__patient"
    ).first()

    if alarm:
        return JsonResponse({
            "active": True,
            "alarm_id": alarm.id,
            "patient_name": alarm.prescription.patient.name,
            "medicine_name": alarm.medicine.name,
            "dosage": alarm.medicine.dosage,
        })

    return JsonResponse({"active": False})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mark_taken(request, alarm_id):

    if request.method == "POST":

        alarm = Alarm.objects.get(id=alarm_id)
        alarm.is_taken = True
        alarm.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)

from datetime import timedelta

@csrf_exempt
def snooze_alarm(request, alarm_id):

    if request.method == "POST":

        alarm = Alarm.objects.get(id=alarm_id)

        now = timezone.localtime()
        new_time = (now + timedelta(minutes=5)).time()

        alarm.alarm_time = new_time
        alarm.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)
