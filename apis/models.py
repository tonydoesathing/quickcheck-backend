from django.db import models

class StudentClass(models.Model):
    name = models.CharField(max_length=300)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=300)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    class_id = models.ForeignKey(StudentClass, models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, blank=True)
    class_id = models.ForeignKey(StudentClass, models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Assessment(models.Model):
    name = models.CharField(max_length=300)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    class_id = models.ForeignKey(StudentClass, models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

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