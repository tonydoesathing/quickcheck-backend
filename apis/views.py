from django.shortcuts import render

from django.http import JsonResponse
from .models import Assessment, Student, Group, StudentClass
from .serializers import AssessmentSerializer, GetAssessmentSerializer, StudentSerializer, GroupSerializer, GetGroupSerializer, StudentScoreSerializer, GroupScoreSerializer, StudentClassSerializer, GetStudentClassSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import django.core.exceptions
from .custompermission import IsCurrentUserOwner
from rest_framework.permissions import IsAuthenticated

class OwnershipVerifier:

    def verify_object(self, user, object):
        if "student_set" in object:
            student_set = object["student_set"]
            for student in student_set:
                if not self.verify_student(student, user):
                    return False
        if "class_id" in object:
            class_id = object["class_id"]
            if not self.verify_class(class_id, user):
                return False
        if "groups" in object:
            groups = object["groups"]
            for group in groups:
                if not self.verify_group(group, user):
                    return False
        if "student_scores" in object:
            student_scores = object["student_scores"]
            for score in student_scores:
                student = score["student_id"]
                if not self.verify_student(student, user):
                    return False
        if "group_scores" in object:
            group_scores = object["group_scores"]
            for score in group_scores:
                group = score["group_id"]
                if not self.verify_group(group, user):
                    return False
        
        return True


    def verify_group(self, id, user):
        group = Group.objects.get(pk=id)
        owner = group.user
        return owner == user

    def verify_student(self, id, user):
        student = Student.objects.get(pk=id)
        owner = student.user
        return owner == user

    def verify_class(self, id, user):
        student_class = StudentClass.objects.get(pk=id)
        owner = student_class.user
        return owner == user

verifier = OwnershipVerifier()

def create_scores(scores, is_student, assessment_id):
    score_type = ["group", "student"][is_student] 
    for score in scores:
        score_object = {score_type: score[score_type+"_id"], "score": score["score"], "assessment": assessment_id}
        if is_student:
            serializer = StudentScoreSerializer(data=score_object)
        else:
            serializer = GroupScoreSerializer(data=score_object)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(django.core.exceptions.BadRequest)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def assessments(request):

    if request.method == 'GET':
        assessments = Assessment.objects.all().filter(user = request.user)
        class_id = request.query_params.get('class_id')
        if class_id is not None:
            assessments = assessments.filter(class_id=class_id)
        serializer = GetAssessmentSerializer(assessments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not verifier.verify_object(request.user, request.data):
            return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)
        student_scores = request.data.pop("student_scores")
        group_scores = request.data.pop("group_scores")
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            try:
                create_scores(student_scores, True, serializer.data["id"])
                create_scores(group_scores, False, serializer.data["id"])
            except:
                return Response(status.HTTP_400_BAD_REQUEST)
            
            # return data as if get assessment called
            assessment = Assessment.objects.get(pk=serializer.data["id"])
            assessment_serializer = GetAssessmentSerializer(assessment)
            return Response(assessment_serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsCurrentUserOwner])
def assessment(request, id):

    try:
        assessment = Assessment.objects.get(pk=id)
    except Assessment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not assessment.user == request.user:
        return Response(
            {'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = GetAssessmentSerializer(assessment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not verifier.verify_object(request.user, request.data):
            return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)
        serializer = AssessmentSerializer(assessment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return data as if get assessment called
            assessment = Assessment.objects.get(pk=serializer.data["id"])
            assessment_serializer = GetAssessmentSerializer(assessment)
            return Response(assessment_serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        assessment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def groups(request):

    if request.method == 'GET':
        groups = Group.objects.all().filter(user = request.user)
        class_id = request.query_params.get('class_id')
        if class_id is not None:
            groups = groups.filter(class_id=class_id)
        serializer = GetGroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not verifier.verify_object(request.user, request.data):
            return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # return data as if get group called
            group = Group.objects.get(pk=serializer.data["id"])
            group_serializer = GetGroupSerializer(group)
            return Response(group_serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsCurrentUserOwner])
def group(request, id):

    try:
        group = Group.objects.get(pk=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not group.user == request.user:
        return Response(
            {'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = GetGroupSerializer(group)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not verifier.verify_object(request.user, request.data):
            return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return data as if get group called
            group = Group.objects.get(pk=serializer.data["id"])
            group_serializer = GetGroupSerializer(group)
            return Response(group_serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def students(request):

    if request.method == 'GET':
        students = Student.objects.all().filter(user = request.user)
        class_id = request.query_params.get('class_id')
        if class_id is not None:
            students = students.filter(class_id=class_id)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not verifier.verify_object(request.user, request.data):
            return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsCurrentUserOwner])
def student(request, id):

    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not student.user == request.user:
        return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not verifier.verify_object(request.user, request.data):
            return Response({'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def student_classes(request):

    if request.method == 'GET':
        students = StudentClass.objects.all().filter(user = request.user)
        serializer = GetStudentClassSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsCurrentUserOwner])
def student_class(request, id):

    try:
        student = StudentClass.objects.get(pk=id)
    except StudentClass.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not student.user == request.user:
        return Response(
            {'message': 'You are not authorizated'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = GetStudentClassSerializer(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentClassSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

