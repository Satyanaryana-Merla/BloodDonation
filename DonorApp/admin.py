"""Creating List in admin"""
from django.contrib import admin
from DonorApp.models import BloodDonorDetailsmodel


class BloodDonorDetailsAdmin(admin.ModelAdmin):
    """Creating List in admin"""
    list_display = ('fullname', 'gender', 'mobilenumber', 'blood_group', 'last_time_blood_donated')
    list_filter = ['blood_group', 'fullname']
    search_fields = ['blood_group', 'fullname']


admin.site.register(BloodDonorDetailsmodel, BloodDonorDetailsAdmin)