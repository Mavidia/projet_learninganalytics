from django.contrib import admin
from moodle.models import MoodleUser

@admin.register(MoodleUser)
class MoodleUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "last_login")
    #search_fields = ("username", "email")


