from django.db import models

class Assessment(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
