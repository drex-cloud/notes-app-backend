from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Unit)
admin.site.register(Subtopic)
admin.site.register(PDF)