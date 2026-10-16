from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile',null=True)
    name = models.CharField(max_length=100,null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(choices=[('Male','Male'),('Female','Female')], max_length=10, null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    image = models.ImageField(upload_to='media/user_image', null=True)
    bmr = models.FloatField(null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args,**kwargs):
        if self.gender == 'Male':
            self.bmr = 66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age)
        elif self.gender == 'Female':
            self.bmr = 655.1 + (9.563 * self.weight) + (1.850 * self.height) - (4.676 * self.age)

        return super().save(*args,**kwargs)

class ConsumeCalorieModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consumed_calorie', null=True)
    item_name = models.CharField(max_length=200,null=True)
    consumed_calorie = models.FloatField(null=True)

    def __str__(self):
        return f'{self.user.username}-{self.item_name}'