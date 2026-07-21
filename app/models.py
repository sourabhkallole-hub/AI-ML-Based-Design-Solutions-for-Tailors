from django.db import models
from django.utils import timezone
# Create your models here.


class AdminMaster(models.Model):
    ad_id = models.AutoField(primary_key=True, unique=True)
    ad_name = models.CharField(max_length=100)
    ad_mobile = models.CharField(max_length=100)
    ad_email = models.CharField(max_length=100)
    ad_password = models.CharField(max_length=100)
    ad_role = models.CharField(max_length=100)
    ad_status = models.CharField(max_length=100, default="0")
    ad_created_by = models.CharField(max_length=100)


class Register(models.Model):
    rg_id = models.AutoField(primary_key=True, unique=True)
    rg_name = models.CharField(max_length=100)
    rg_mobile = models.CharField(max_length=100)
    rg_email = models.CharField(max_length=100)
    rg_password = models.CharField(max_length=100)
    rg_address = models.CharField(max_length=100, default="")
    rg_secret_key = models.CharField(max_length=100, default="")
    rg_status = models.CharField(max_length=100, default="0")


class Contact(models.Model):
    co_id = models.AutoField(primary_key=True, unique=True)
    co_name = models.CharField(max_length=100)
    co_mobile = models.CharField(max_length=100)
    co_email = models.CharField(max_length=100)
    co_subject = models.CharField(max_length=100)
    co_message = models.CharField(max_length=100)
    co_status = models.CharField(max_length=100)

class PredictHistory(models.Model):
    ph_id = models.AutoField(primary_key=True, unique=True)
    
    ph_age = models.IntegerField()
    ph_gender = models.CharField(max_length=10)
    ph_height_cm = models.FloatField()
    ph_chest_cm = models.FloatField()
    ph_waist_cm = models.FloatField()
    ph_hips_cm = models.FloatField()
    ph_shoulder_cm = models.FloatField()
    ph_occasion = models.CharField(max_length=50)

    ph_predicted_outfit = models.CharField(max_length=100)
    
    ph_created_by = models.CharField(max_length=100, default="", blank=True)
    ph_status = models.CharField(max_length=10, default="0")
    ph_created_date = models.DateTimeField(auto_now_add=True)

class Design(models.Model):
    de_id = models.AutoField(primary_key=True, unique=True)
    de_name = models.CharField(max_length=100)
    de_status = models.CharField(max_length=100, default="0")
    de_image = models.FileField(upload_to="app/static/media/images")

class DesignSteps(models.Model):
    ar_id = models.AutoField(primary_key=True, unique=True)
    ar_de_id = models.CharField(max_length=100, default="")
    ar_name = models.CharField(max_length=100)
    ar_image = models.ImageField(upload_to="app/static/images/")
    ar_description = models.TextField(default="")
    ar_status = models.CharField(max_length=100, default="0")

class Bookings(models.Model):
    bk_id = models.AutoField(primary_key=True, unique=True)
    ph_id = models.IntegerField(default=0)
    de_id = models.IntegerField()
    de_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    booking_date = models.DateField(auto_now_add=True)
    booking_time = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default="Pending")