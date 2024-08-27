from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Milan(models.Model):
    milan_name = models.CharField(max_length=100)
    valaya = models.CharField(max_length=100)
    khand = models.CharField(max_length=100)
    prakhand = models.CharField(max_length=100)
    nagar = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Responsibility(models.Model):
    role_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    milan = models.ForeignKey(Milan, on_delete=models.CASCADE)
    role = models.ForeignKey(Responsibility, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    address_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reports(models.Model):
    milan = models.ForeignKey('Milan', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='user_reports', on_delete=models.CASCADE, null=True, blank=True)
    common_user = models.ForeignKey('CommonUser', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey('Responsibility', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('milan', 'user', 'created_at','common_user')
        constraints = [
            models.UniqueConstraint(
                fields=['milan', 'user', 'common_user', 'created_at'],
                name='unique_report'
            )
        ]
@receiver(pre_save, sender=Reports)
def set_user_role(sender, instance, **kwargs):
    if instance.user and not instance.role:
        instance.role = instance.user.role

class CommonUser(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    milan = models.ForeignKey(Milan, on_delete=models.CASCADE)
    address = models.TextField()
    role = models.ForeignKey(Responsibility, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)