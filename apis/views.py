from django.shortcuts import render

from django.http import JsonResponse
from .models import Assessment, Student, Group
from .serializers import AssessmentSerializer, GetAssessmentSerializer, StudentSerializer, GroupSerializer, GetGroupSerializer, StudentScoreSerializer, GroupScoreSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import django.core.exceptions

#
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
def assessments(request):

    if request.method == 'GET':
        assessments = Assessment.objects.all()
        serializer = GetAssessmentSerializer(assessments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        student_scores = request.data.pop("student_scores")
        group_scores = request.data.pop("group_scores")
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                create_scores(student_scores, True, serializer.data["id"])
                create_scores(group_scores, False, serializer.data["id"])
            except:
                return Response(status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def assessment(request, id):

    try:
        assessment = Assessment.objects.get(pk=id)
    except Assessment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetAssessmentSerializer(assessment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AssessmentSerializer(assessment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        assessment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def groups(request):

    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GetGroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return data as if get group called
            group = Group.objects.get(pk=serializer.data["id"])
            group_serializer = GetGroupSerializer(group)
            return Response(group_serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def group(request, id):

    try:
        group = Group.objects.get(pk=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetGroupSerializer(group)
        return Response(serializer.data)

    elif request.method == 'PUT':
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
def students(request):

    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def student(request, id):

    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)