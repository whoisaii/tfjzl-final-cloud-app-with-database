from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Enrollment, Submission

def index(request):
    return render(request, 'onlinecourse/course_list.html', {'courses': Course.objects.all()})

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

@login_required
@require_POST
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = list(course.question_set.prefetch_related('choice_set'))
    if not questions:
        return HttpResponseBadRequest('This course has no exam yet.')
    raw = request.POST.getlist('choices')
    try:
        selected = {int(value) for value in raw}
    except ValueError:
        return HttpResponseBadRequest('Invalid choice.')
    valid = {c.pk for q in questions for c in q.choice_set.all()}
    if not selected <= valid:
        return HttpResponseBadRequest('Choice does not belong to this course.')
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    results, score, total = [], 0, 0
    for q in questions:
        choices = list(q.choice_set.all())
        correct = {c.pk for c in choices if c.is_correct}
        chosen = {c.pk for c in choices if c.pk in selected}
        passed = bool(correct) and chosen == correct
        score += q.grade if passed else 0
        total += q.grade
        results.append({'question': q.question_text, 'correct': passed, 'earned': q.grade if passed else 0, 'possible': q.grade, 'selected': [c.choice_text for c in choices if c.pk in chosen], 'answers': [c.choice_text for c in choices if c.is_correct]})
    submission = Submission.objects.create(enrollment=enrollment, score=score, total=total, results=results)
    submission.choices.set(selected)
    return redirect('onlinecourse:show_exam_result', course_id=course.pk, submission_id=submission.pk)

@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission.objects.select_related('enrollment__course'), pk=submission_id, enrollment__course_id=course_id, enrollment__user=request.user)
    # Use the saved question results so later course edits cannot change a grade.
    grade = sum(result['earned'] for result in submission.results)
    possible = sum(result['possible'] for result in submission.results)
    percentage = round(100 * grade / possible, 1) if possible else 0
    context = {
        'submission': submission,
        'course': submission.enrollment.course,
        'grade': grade,
        'possible': possible,
        'percentage': percentage,
        'passed': percentage >= 80,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
