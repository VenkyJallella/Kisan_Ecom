from django.contrib import admin
from .models import contactForm

# Register your models here.

@admin.register(contactForm)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email")
