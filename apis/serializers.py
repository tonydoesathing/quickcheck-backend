from rest_framework import serializers
from .models import Assessment, Group, Student, StudentScore, GroupScore, StudentClass

def get_entity_objects(entities, entity_serializer):
        serialized_entities = []
        for entity in entities:
            serializer = entity_serializer(entity)
            serialized_entities.append(serializer.data)
        return serialized_entities

class GetGroupSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    student_set = serializers.SerializerMethodField()

    def get_student_set(self, obj):
        students = obj.student_set.all()
        serialized_students = get_entity_objects(students, StudentSerializer)
        return serialized_students

    class Meta:
        model = Group
        fields = ['id', 'name', 'date_edited', 'date_created', 'student_set', 'class_id', 'user']

class GroupSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Group
        fields = ['id', 'name', 'date_edited', 'date_created', 'student_set', 'class_id', 'user']

class StudentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Student
        fields = ['id', 'name', 'date_edited', 'date_created', 'groups', 'class_id', 'user']

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
        serializer = GetGroupSerializer(obj.group)
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

    user = serializers.ReadOnlyField(source='user.username')

    studentscore_set = serializers.SerializerMethodField()
    groupscore_set = serializers.SerializerMethodField()

    def get_studentscore_set(self, obj):
        student_scores = obj.studentscore_set.all()
        serialized_student_scores = get_entity_objects(student_scores, GetStudentScoreSerializer)
        return serialized_student_scores

    def get_groupscore_set(self, obj):
        group_scores = obj.groupscore_set.all()
        serialized_group_scores = get_entity_objects(group_scores, GetGroupScoreSerializer)
        return serialized_group_scores

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'date_edited', 'date_created', 'studentscore_set', 'groupscore_set', 'class_id', 'user']

class AssessmentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'date_edited', 'date_created', 'class_id', 'user']

class StudentClassSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = StudentClass
        fields = ['id', 'name', 'date_created', 'date_edited', 'user']

class GetStudentClassSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    student_set = serializers.SerializerMethodField()
    group_set = serializers.SerializerMethodField()
    assessment_set = serializers.SerializerMethodField()

    def get_student_set(self, obj):
        students = obj.student_set.all()
        serialized_students = get_entity_objects(students, StudentSerializer)
        return serialized_students

    def get_group_set(self, obj):
        groups = obj.group_set.all()
        serialized_groups = get_entity_objects(groups, GetGroupSerializer)
        return serialized_groups

    def get_assessment_set(self, obj):
        assessments = obj.assessment_set.all()
        serialized_assessments = get_entity_objects(assessments, GetAssessmentSerializer)
        return serialized_assessments
    
    class Meta:
        model = StudentClass
        fields = ['id', 'name', 'date_created', 'date_edited', 'student_set', 'group_set', 'assessment_set', 'user']