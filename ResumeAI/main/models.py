from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    document = models.FileField(upload_to='pdfs/', null=False, blank=False)
    comment = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name