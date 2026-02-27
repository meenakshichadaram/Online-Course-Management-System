from django.contrib import admin
from .models import Category, Course, Module, Lecture

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['title', 'instructor', 'category', 'level', 'price', 'is_published']
    list_filter   = ['is_published', 'level', 'category']
    list_editable = ['is_published']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'duration']