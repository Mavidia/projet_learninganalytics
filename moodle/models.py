from django.db import models

class MoodlePlatform(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    token = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class MoodleUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


