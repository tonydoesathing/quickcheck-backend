from django.db import models

class Assessment(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, models.SET_NULL, null=True)

    def __str__(self):
        return self.name