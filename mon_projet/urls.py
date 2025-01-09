from moodle import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('moodle/', include('moodle.urls')),  # Inclure l'URL de l'app moodle
]



