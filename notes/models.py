from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    user = models.ForeignKey(User, related_name="units", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subtopic(models.Model):
    unit = models.ForeignKey(Unit, related_name="subtopics", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)  # will store the HTML from Quill

    def __str__(self):
        return f"{self.unit.name} - {self.title}"


class PDF(models.Model):
    subtopic = models.ForeignKey(Subtopic, related_name="pdfs", on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True)
    file = models.FileField(upload_to='course_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"PDF for {self.subtopic.title}"
