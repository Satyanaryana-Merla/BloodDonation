"""Importing modules"""
from django.db import models
from django.contrib.auth.models import Group

# from django.contrib.auth.models import User

GENDER = (("Male", "Male"),
          ("Female", "Female"),
          ("Others", "Others"))


CHOICYESNO = (("YES", "YES"),
              ("NO", "NO"))

BLOODBEFORE = (("YES", "YES"),
               ("NO", "NO"))


class BloodDonorDetailsmodel(models.Model):
    """BloodDonorDetails"""
    fullname = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER, max_length=50)
    email = models.EmailField()
    mobilenumber = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    Home_address = models.CharField(max_length=250)
    office_address = models.CharField(max_length=250)
    occupation = models.CharField(max_length=50)
    last_time_blood_donated = models.CharField(max_length=100)
    did_you_ever_donate_blood_before = models.CharField(max_length=20,
                                                        choices=BLOODBEFORE)
    Are_you_currently_taking_any_medications = models.TextField()
    Do_you_have_any_disease = models.TextField()


DONOR_GROUP_NAME = 'Donor'
HOSPITAL_GROUP_NAME = 'Hospital'
COMPANY_GROUP_NAME = 'Company'


def create_groups():
    donor_group, created = Group.objects.get_or_create(name=DONOR_GROUP_NAME)
    hospital_group, created = Group.objects.get_or_create(name=HOSPITAL_GROUP_NAME)
    company_group, created = Group.objects.get_or_create(name=COMPANY_GROUP_NAME)

