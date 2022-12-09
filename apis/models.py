from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.name

class Assessment(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StudentScore(models.Model):

    score = models.IntegerField()
    student = models.ForeignKey(Student, models.CASCADE)
    assessment = models.ForeignKey(Assessment, models.CASCADE)

class GroupScore(models.Model):

    score = models.IntegerField()
    group = models.ForeignKey(Group, models.CASCADE)
    assessment = models.ForeignKey(Assessment, models.CASCADE)