from django.db import models
from datetime import datetime, date
from django import forms
from django.db import models
from phone_field import PhoneField
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Contact(models.Model):
    client = models.CharField(max_length=200, null=True, blank=True)
    # projects = models.ListField(null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.IntegerField(null=True,)
    phone = PhoneField(null=True, unique=True, blank=True)
    email = models.EmailField(null=False, unique=True, blank=True)

    def __str__(self):
        return self.client

# add default=0 so we dont get weird invalid literal for int() with base 10: error


class Project(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    contact_id = models.ForeignKey(
        Contact, null=True, on_delete=models.SET_NULL)
    number_of_signs = models.FloatField(null=True, blank=True, default=0)
    sign_details = models.TextField(null=True, blank=True)
    subtotal = models.FloatField(null=True, blank=True, default=0)
    sign_permit = models.FloatField(null=True, blank=True, default=0)
    engineering = models.FloatField(null=True, blank=True, default=0)
    other_fees = models.FloatField(null=True, blank=True, default=0)
    discount = models.FloatField(null=True, blank=True, default=0)
    cash_discount = models.FloatField(null=True, blank=True, default=0)
    discount_total = models.FloatField(null=True, blank=True, default=0)
    final_total = models.FloatField(null=True, blank=True, default=0)
    deposit_percentage = models.FloatField(null=True, blank=True, default=0, validators=[
        MaxValueValidator(100), MinValueValidator(0)])
    deposit_amount = models.FloatField(null=True, blank=True, default=0)
    completion_percentage = models.FloatField(
        null=True, blank=True, default=0, validators=[
            MaxValueValidator(100), MinValueValidator(0)])
    completion_amount = models.FloatField(null=True, blank=True, default=0, )
    intial_date = models.DateField(
        default=timezone.now, auto_now_add=False, auto_now=False, blank=True)
    survey_date = models.DateField(null=True,
                                   default=timezone.now, auto_now_add=False, auto_now=False, blank=True)
    approval_date = models.DateField(null=True,
                                     default=timezone.now, auto_now_add=False, auto_now=False, blank=True)
    sign_permit_details = models.TextField(null=True, blank=True)
    landlord_approval_details = models.TextField(null=True, blank=True)
    artwork_approved = models.BooleanField(
        default=False, null=True, blank=True)
    contract_approved = models.BooleanField(
        default=False, null=True, blank=True)
    legal_description = models.TextField(null=True, blank=True)
    general_contractor_name = models.CharField(
        max_length=200, null=True, blank=True)
    electrician_name = models.CharField(max_length=200, null=True, blank=True)
    turnaround_time = models.DateField(
        default=timezone.now, auto_now_add=False, auto_now=False, null=True, blank=True)
    actual_installation = models.DateField(
        default=timezone.now, auto_now_add=False, auto_now=False,  null=True, blank=True)
    production_notes = models.TextField(null=True, blank=True)
    installation_date = models.DateField(
        default=timezone.now, auto_now_add=False, auto_now=False, null=True, blank=True)
    date_of_completion = models.DateField(
        default=timezone.now, auto_now_add=False, auto_now=False, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    special_colors_materials = models.TextField(null=True, blank=True)
    external_links = models.TextField(
        null=True,
        blank=True,

    )

    def __str__(self):
        return self.name
