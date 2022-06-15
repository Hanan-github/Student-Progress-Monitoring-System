from calendar import week
from configparser import SectionProxy
from dataclasses import field
from datetime import date
import math
from tkinter import CASCADE
from unicodedata import name
from django.db import models
from account.models import Account

from home.models import Contact

# Create your models here.
class School(models.Model):
    name            = models.CharField(max_length=255, null=True)
    contact         = models.IntegerField(null=True)
    address         = models.CharField(max_length=255, null=True)

    #relations
    account         = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 


        

class Parent(models.Model):
    parent_name     = models.CharField(max_length=255, null=True)
    address         = models.CharField(max_length=255, null=True)
    contact         = models.IntegerField(null=True)
    cnic            = models.IntegerField(unique=True, null=True)
    email           = models.EmailField(max_length=60, null=True)

    #relations
    school          = models.ForeignKey(School, on_delete=models.CASCADE)
    account         = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.parent_name 



class Class(models.Model):
    class_no      = models.IntegerField(null=True)
    class_title     = models.CharField(max_length=50, null=True)
    
    #relations
    school          = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Classes"





class Upcoming_Test(models.Model):
    subject         = models.CharField(max_length=50, null=True)
    description     = models.CharField(max_length=50, null=True)
    date            = models.DateField(null=True)

    #relations
    for_class       = models.ForeignKey(Class, on_delete=models.CASCADE, default=None)





class Student(models.Model):
    name            = models.CharField(max_length=255, null=True)
    roll_number     = models.IntegerField(null=True)
    gender          = models.CharField(max_length=10, null=True)
    dob             = models.DateField(null=True)
    age             = models.IntegerField(null=True)
    father_cnic     = models.IntegerField(null=True)

    #relations
    school          = models.ForeignKey(School, on_delete=models.CASCADE)
    parent          = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    student_class   = models.ForeignKey(Class, on_delete=models.CASCADE)



class Attendence_Report(models.Model):
    Monday             = models.CharField(max_length=10, null=True)
    Tuesday            = models.CharField(max_length=10, null=True)
    Wednesday          = models.CharField(max_length=10, null=True)
    Thursday           = models.CharField(max_length=10, null=True)
    Friday             = models.CharField(max_length=10, null=True)
    Saturday           = models.CharField(max_length=10, null=True)
    Date               = models.DateField(auto_now_add=True, null=True)

    #relations
    student          = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)



class Result_Card(models.Model):
    urdu_obtained           = models.IntegerField(null=True)
    urdu_total              = models.IntegerField(null=True)
    
    english_obtained        = models.IntegerField(null=True)
    english_total           = models.IntegerField(null=True)

    maths_obtained          = models.IntegerField(null=True)
    maths_total             = models.IntegerField(null=True)

    physics_obtained        = models.IntegerField(null=True)
    physics_total           = models.IntegerField(null=True)

    chemistry_obtained      = models.IntegerField(null=True)
    chemistry_total         = models.IntegerField(null=True)

    bio_obtained            = models.IntegerField(null=True)
    bio_total               = models.IntegerField(null=True)

    computer_obtained       = models.IntegerField(null=True)
    computer_total          = models.IntegerField(null=True)

    pakstudies_obtained     = models.IntegerField(null=True)
    pakstudies_total        = models.IntegerField(null=True)

    islamiyat_obtained      = models.IntegerField(null=True)
    islamiyat_total         = models.IntegerField(null=True)

    science_obtained        = models.IntegerField(null=True)
    science_total           = models.IntegerField(null=True)

    arabic_obtained         = models.IntegerField(null=True)
    arabic_total            = models.IntegerField(null=True)

    total_obtained          = models.IntegerField(null=True)
    total_marks             = models.IntegerField(null=True)

    date                    = models.DateField(auto_now_add=True, null=True)

    #relations
    student          = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)




class Event(models.Model):
    title              = models.CharField(max_length=30, null=True)
    description        = models.TextField(null=True)
    date               = models.DateField(auto_now_add=True, null=True)

    #relations
    school             = models.ForeignKey(School, on_delete=models.CASCADE)