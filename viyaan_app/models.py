from django.core.validators import RegexValidator
from django.db import models

import os

class Signup(models.Model):

    full_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number entered in the format:'+919999999999'. Up to 14 digits number")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    password = models.CharField(max_length=20, null=False, blank=False)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    community = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email + "|" + str(self.id)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.profile_picture.path):
            os.remove(self.profile_picture.path)

        super(Signup, self).delete(*args, **kwargs)

class send_notification(models.Model):
    title = models.CharField(max_length=1024, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title + "|" + str(self.id)