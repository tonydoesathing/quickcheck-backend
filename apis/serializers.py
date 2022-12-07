from rest_framework import serializers
from .models import Assessment, Group, Student

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'name', 'date']

class GetGroupSerializer(serializers.ModelSerializer):

    student_set = serializers.SerializerMethodField()

    def get_student_set(self, obj):
        students = obj.student_set.all()
        serialized_students = []
        for student in students:
            serializer = StudentSerializer(student)
            serialized_students.append(serializer.data)
        return serialized_students

    class Meta:
        model = Group
        fields = ['id', 'name', 'date', 'student_set']

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name', 'date', 'student_set']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'date', 'group']