from django.contrib import admin
from .models import doctor,patient

# Register your models here.
admin.site.register(doctor)
admin.site.register(patient)