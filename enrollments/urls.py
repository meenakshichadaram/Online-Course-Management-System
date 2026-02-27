from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Enrollment
from .serializers import EnrollmentSerializer


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'STUDENT'


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset           = Enrollment.objects.all()
    serializer_class   = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['delete'], url_path='unenroll')
    def unenroll(self, request, pk=None):
        try:
            enrollment = Enrollment.objects.get(pk=pk, student=request.user)
            enrollment.delete()
            return Response(
                {'detail': 'Successfully unenrolled from the course.'},
                status=status.HTTP_200_OK
            )
        except Enrollment.DoesNotExist:
            return Response(
                {'detail': 'Enrollment not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet

router = DefaultRouter()
router.register(r'', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]