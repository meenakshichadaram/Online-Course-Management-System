from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        cached_data = cache.get("course_list")

        if cached_data:
            return Response(cached_data)

        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        cache.set("course_list", serializer.data, timeout=600)  # 10 minutes

        return Response(serializer.data)

from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "INSTRUCTOR"
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsInstructor()]
        return []