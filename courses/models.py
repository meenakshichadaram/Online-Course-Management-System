from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = (
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced',     'Advanced'),
    )

    title        = models.CharField(max_length=200)
    description  = models.TextField()
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    level        = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    instructor   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True, null=True)
    updated_at   = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title  = models.CharField(max_length=200)
    order  = models.IntegerField(default=0)

    class Meta:
        unique_together = ('course', 'order')
        ordering        = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lecture(models.Model):
    module    = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lectures')
    title     = models.CharField(max_length=200)
    video_url = models.TextField(blank=True, null=True)
    notes     = models.TextField(blank=True, null=True)
    order     = models.IntegerField(default=0)
    duration  = models.IntegerField(default=0, help_text='Duration in seconds')

    class Meta:
        unique_together = ('module', 'order')
        ordering        = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"