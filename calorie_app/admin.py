from django.contrib import admin
from calorie_app.models import *
# Register your models here.

admin.site.register([UserProfileModel, ConsumeCalorieModel])