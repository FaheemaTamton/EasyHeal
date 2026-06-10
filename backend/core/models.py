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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50, blank=True)
    organization = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username
