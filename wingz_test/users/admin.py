from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    fields = [
        "email",
        "password",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "date_joined",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
