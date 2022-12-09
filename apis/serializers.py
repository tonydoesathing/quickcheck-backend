from rest_framework import serializers
from .models import Assessment, Group, Student, StudentScore, GroupScore

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
        fields = ['id', 'name', 'date', 'groups']

class GetStudentScoreSerializer(serializers.ModelSerializer):

    student = serializers.SerializerMethodField()

    def get_student(self, obj):
        serializer = StudentSerializer(obj.student)
        serialized_student = serializer.data
        return serialized_student

    class Meta:
        model = StudentScore
        fields = ['score', 'student', 'assessment']

class GetGroupScoreSerializer(serializers.ModelSerializer):

    group = serializers.SerializerMethodField()

    def get_group(self, obj):
        serializer = StudentSerializer(obj.group)
        serialized_group = serializer.data
        return serialized_group

    class Meta:
        model = GroupScore
        fields = ['score', 'group', 'assessment']

class StudentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScore
        fields = ['score', 'student', 'assessment']

class GroupScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupScore
        fields = ['score', 'group', 'assessment']

class GetAssessmentSerializer(serializers.ModelSerializer):

    studentscore_set = serializers.SerializerMethodField()
    groupscore_set = serializers.SerializerMethodField()

    def get_studentscore_set(self, obj):
        student_scores = obj.studentscore_set.all()
        serialized_student_scores = []
        for score in student_scores:
            serializer = GetStudentScoreSerializer(score)
            serialized_student_scores.append(serializer.data)
        return serialized_student_scores

    def get_groupscore_set(self, obj):
        group_scores = obj.groupscore_set.all()
        serialized_group_scores = []
        for score in group_scores:
            serializer = GetGroupScoreSerializer(score)
            serialized_group_scores.append(serializer.data)
        return serialized_group_scores

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'date', 'studentscore_set', 'groupscore_set']

class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'date']