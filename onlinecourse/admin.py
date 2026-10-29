from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['name']

admin.site.register([Instructor, Learner, Choice, Submission])
