from django.db import models

class Changelog(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    site = models.CharField(max_length=100, default='Default Site')  # Add this line

    
    def __str__(self):
        return self.title
