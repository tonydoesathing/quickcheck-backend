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

def class_authorized(user, class_id):
    classes = StudentClass.objects.all().filter(user = user)
    class_ids = [c.id for c in classes]
    return class_id in class_ids

def group_authorized(user, group):
    groups = Group.objects.all().filter(user = user)
    group_ids = [g.id for g in groups]
    for g in group:
        if not g in group_ids:
            return False
    return True

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
        if not class_authorized(request.user, request.data["class_id"]):
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
        if not class_authorized(request.user, request.data["class_id"]):
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
        if not class_authorized(request.user, request.data["class_id"]):
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
        if not class_authorized(request.user, request.data["class_id"]):
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
        if not class_authorized(request.user, request.data["class_id"]) or not group_authorized(request.user, request.data["groups"]):
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
        if not class_authorized(request.user, request.data["class_id"]) or not group_authorized(request.user, request.data["groups"]):
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