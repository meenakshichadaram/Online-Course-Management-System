from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register('', CourseViewSet)

urlpatterns = router.urls