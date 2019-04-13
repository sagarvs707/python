from django.contrib import admin

# Register your models here.
from .models import Signup, Document

admin.site.register(Signup)

admin.site.register(Document)

