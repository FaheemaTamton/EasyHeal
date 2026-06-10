from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    health_issue = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='patients/', null=True, blank=True)

    guardian_name = models.CharField(
        max_length=100,
        blank=True
    )
    guardian_phone = models.CharField(
        max_length=15,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




    image = models.ImageField(
        upload_to='prescriptions/',
        null=True,
        blank=True
    )

    raw_extracted_data = models.JSONField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IN_PROGRESS'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription #{self.id} - {self.patient.name}"


# ================= MEDICINE =================
class Medicine(models.Model):

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='medicines'
    )

    name = models.CharField(max_length=200)

    dosage = models.CharField(max_length=100)

    food_instruction = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    intake_pattern = models.CharField(
        max_length=100,
        help_text="Once daily, Twice daily, etc."
    )

    duration_days = models.IntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.name} ({self.prescription.id})"


# ================= ALARM =================
class Alarm(models.Model):

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='alarms'
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='alarms'
    )

    alarm_date = models.DateField()

    alarm_time = models.TimeField()

    is_taken = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.alarm_date} {self.alarm_time}"



# ✅ AUTO-CREATE PROFILE FOR EVERY NEW USER
@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
