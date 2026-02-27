# ocms/views.py
from django.shortcuts import render, get_object_or_404
from courses.models import Course, Category
from enrollments.models import Enrollment, LectureProgress
from reviews.models import Review
from accounts.models import User


def login_page(request):
    return render(request, 'login.html')


def student_dashboard(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course', 'course__category', 'course__instructor') if request.user.is_authenticated else []

    for enrollment in enrollments:
        total = LectureProgress.objects.filter(enrollment=enrollment).count()
        completed = LectureProgress.objects.filter(enrollment=enrollment, completed=True).count()
        enrollment.progress_percent = int((completed / total) * 100) if total > 0 else 0

    enrolled_count  = len(enrollments)
    completed_count = sum(1 for e in enrollments if e.status == 'COMPLETED')

    recent_progress = LectureProgress.objects.filter(
        enrollment__student=request.user,
        completed=True
    ).select_related('enrollment__course', 'lecture').order_by('-completed_at')[:10] if request.user.is_authenticated else []

    return render(request, 'student_dashboard.html', {
        'enrollments':     enrollments,
        'enrolled_count':  enrolled_count,
        'completed_count': completed_count,
        'hours_learned':   0,
        'reviews_count':   Review.objects.filter(student=request.user).count() if request.user.is_authenticated else 0,
        'recent_progress': recent_progress,
    })


def my_courses(request):
    return student_dashboard(request)


def course_list(request):
    courses_qs = Course.objects.filter(
        is_published=True
    ).select_related('category', 'instructor').prefetch_related('modules')

    for course in courses_qs:
        reviews = Review.objects.filter(course=course)
        course.review_count = reviews.count()
        course.avg_rating   = round(sum(r.rating for r in reviews) / reviews.count(), 1) if reviews.count() > 0 else None

    categories = Category.objects.all()

    return render(request, 'course_list.html', {
        'courses':    courses_qs,
        'categories': categories,
    })


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    reviews      = Review.objects.filter(course=course).select_related('student')
    review_count = reviews.count()
    avg_rating   = round(sum(r.rating for r in reviews) / review_count, 1) if review_count > 0 else None

    enrollment_count = Enrollment.objects.filter(course=course).count()
    total_lectures   = sum(m.lectures.count() for m in course.modules.all())

    is_enrolled           = False
    progress_percent      = 0
    completed_lectures    = 0
    completed_lecture_ids = []
    user_review           = None

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(
            student=request.user, course=course
        ).first()

        if enrollment:
            is_enrolled  = True
            completed_qs = LectureProgress.objects.filter(
                enrollment=enrollment, completed=True
            )
            completed_lectures    = completed_qs.count()
            completed_lecture_ids = list(completed_qs.values_list('lecture_id', flat=True))
            progress_percent      = int((completed_lectures / total_lectures) * 100) if total_lectures > 0 else 0

        user_review = Review.objects.filter(
            student=request.user, course=course
        ).first()

    course.avg_rating   = avg_rating
    course.review_count = review_count

    return render(request, 'course_detail.html', {
        'course':                course,
        'reviews':               reviews,
        'enrollment_count':      enrollment_count,
        'total_lectures':        total_lectures,
        'is_enrolled':           is_enrolled,
        'progress_percent':      progress_percent,
        'completed_lectures':    completed_lectures,
        'completed_lecture_ids': completed_lecture_ids,
        'user_review':           user_review,
    })


def instructor_dashboard(request):
    courses        = []
    total_students = 0
    total_reviews  = 0

    if request.user.is_authenticated:
        courses = Course.objects.filter(
            instructor=request.user
        ).select_related('category').prefetch_related('modules')

        for course in courses:
            reviews = Review.objects.filter(course=course)
            course.enrollment_count = Enrollment.objects.filter(course=course).count()
            course.review_count     = reviews.count()
            course.avg_rating       = round(sum(r.rating for r in reviews) / reviews.count(), 1) if reviews.count() > 0 else None
            total_students         += course.enrollment_count
            total_reviews          += course.review_count

    all_ratings = [c.avg_rating for c in courses if c.avg_rating]
    avg_rating  = round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else None
    categories  = Category.objects.all()

    return render(request, 'instructor_dashboard.html', {
        'courses':        courses,
        'total_courses':  len(courses),
        'total_students': total_students,
        'total_reviews':  total_reviews,
        'avg_rating':     avg_rating,
        'categories':     categories,
    })


def admin_dashboard(request):
    from django.db.models import Count

    total_users       = User.objects.count()
    student_count     = User.objects.filter(role='STUDENT').count()
    instructor_count  = User.objects.filter(role='INSTRUCTOR').count()
    admin_count       = User.objects.filter(role='ADMIN').count()
    total_courses     = Course.objects.count()
    published_courses = Course.objects.filter(is_published=True).count()
    total_enrollments = Enrollment.objects.count()
    total_reviews     = Review.objects.count()
    completed_count   = Enrollment.objects.filter(status='COMPLETED').count()
    completion_rate   = int((completed_count / total_enrollments) * 100) if total_enrollments > 0 else 0

    all_reviews = Review.objects.all()
    avg_rating  = round(sum(r.rating for r in all_reviews) / all_reviews.count(), 1) if all_reviews.count() > 0 else None

    top_courses  = Course.objects.annotate(
        enrollment_count=Count('enrollment')
    ).order_by('-enrollment_count')[:5]

    recent_users = User.objects.order_by('-created_at')[:10]

    redis_defaults = [
        {'key': 'admin:users:count'},
        {'key': 'admin:courses:count'},
        {'key': 'admin:top:courses'},
        {'key': 'admin:enrollments:count'},
    ]

    return render(request, 'admin_dashboard.html', {
        'stats': {
            'total_users':       total_users,
            'student_count':     student_count,
            'instructor_count':  instructor_count,
            'admin_count':       admin_count,
            'total_courses':     total_courses,
            'published_courses': published_courses,
            'total_enrollments': total_enrollments,
            'total_reviews':     total_reviews,
            'completion_rate':   completion_rate,
            'avg_rating':        avg_rating,
        },
        'top_courses':    top_courses,
        'recent_users':   recent_users,
        'redis_defaults': redis_defaults,
        'cache_keys':     [],
    })

def logout_page(request):
    # clear django session
    from django.contrib.auth import logout
    logout(request)
    # redirect to login
    from django.shortcuts import redirect
    return redirect('/auth/login/')