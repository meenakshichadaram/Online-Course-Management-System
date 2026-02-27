from django.db import models
from django.conf import settings
from courses.models import Course, Lecture


class Enrollment(models.Model):
    STATUS = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    )

    student     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course      = models.ForeignKey(Course, on_delete=models.CASCADE)
    status      = models.CharField(max_length=20, choices=STATUS, default='ACTIVE')
    enrolled_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.full_name} → {self.course.title}"


class LectureProgress(models.Model):
    enrollment   = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    lecture      = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    completed    = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'lecture')

    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.lecture.title} - {'Done' if self.completed else 'Pending'}"