from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Education, Project
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import EducationSerializer, ProjectSerializer


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method == "GET":
        projects = Project.objects.prefetch_related("starred_by")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        return Response(ProjectSerializer(projects, many=True, context={"request": request}).data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related("starred_by"), pk=pk)
    if request.method == "GET":
        return Response(ProjectSerializer(project, context={"request": request}).data)
    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return Response(ProjectSerializer(project, context={"request": request}).data)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method == "GET":
        education = Education.objects.prefetch_related("starred_by")
        institution = request.query_params.get("institution", "").strip()
        if institution:
            education = education.filter(institution__icontains=institution)
        return Response(EducationSerializer(education, many=True, context={"request": request}).data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, pk):
    education = get_object_or_404(Education.objects.prefetch_related("starred_by"), pk=pk)
    if request.method == "GET":
        return Response(EducationSerializer(education, context={"request": request}).data)
    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)
    return Response(EducationSerializer(education, context={"request": request}).data)
