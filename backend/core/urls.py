from django.urls import path
from .views import *
from .import views
from .views import add_patient
from .views import scan_prescription



urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('add-patient/', add_patient, name='add_patient'),
    path('patient/<int:id>/', patient_details, name='patient_details'),
    path('account/', my_account_view, name='my_account'),
    path('logout/', logout_view, name='logout'),
    path("scan/", scan_prescription, name="scan_prescription"),
    path('patient/<int:id>/', views.patient_details, name='patient_details'),
    path("scan/", views.scan_prescription, name="scan_prescription"),
    path(
    "medicine-details/<int:prescription_id>/",
    views.medicine_details,
    name="medicine_details"
),
   path(
    "generate-alarms/<int:prescription_id>/",
    views.generate_alarm_preview,
    name="generate_alarm_preview"
),

   path(
    "save-alarms/<int:prescription_id>/",
    views.save_alarms,
    name="save_alarms"
),
   path(
    "prescription/<int:prescription_id>/",
    views.prescription_detail,
    name="prescription_detail"
),

   path("patient/<int:id>/", views.patient_details, name="patient_details"),

   path(
    "delete-prescription/<int:id>/",
    views.delete_prescription,
    name="delete_prescription"
),

   path(
    "delete-patient/<int:id>/",
    views.delete_patient,
    name="delete_patient"
),
  
   path("check-alarm/", views.check_alarm, name="check_alarm"),
   path("mark-taken/<int:alarm_id>/", views.mark_taken, name="mark_taken"),
   path("snooze-alarm/<int:alarm_id>/", views.snooze_alarm, name="snooze_alarm"),



   
]
