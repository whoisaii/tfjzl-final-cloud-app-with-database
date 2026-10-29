from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice
class Command(BaseCommand):
    help = 'Create a repeatable sample course (no user accounts or passwords).'
    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(name='Django Essentials', defaults={'description': 'Learn models, URL routing, and Django templates.'})
        lessons = [('Models and databases', 'Django models describe database tables. A ForeignKey creates a many-to-one relationship.'), ('Routing and templates', 'URL patterns map paths to views. Templates render context into HTML. CSRF tokens protect POST forms.')]
        for order, (title, content) in enumerate(lessons, 1):
            Lesson.objects.get_or_create(course=course, title=title, defaults={'content': content, 'order': order})
        data = [('Which field represents a many-to-one relationship?', [('ForeignKey', True), ('CharField', False), ('BooleanField', False)]), ('What does urls.py map URL paths to?', [('Views', True), ('Database columns', False), ('CSS classes', False)]), ('Which template tag protects a POST form against CSRF?', [('{% csrf_token %}', True), ('{% static %}', False), ('{% for %}', False)])]
        for title, choices in data:
            question, _ = Question.objects.get_or_create(course=course, question_text=title, defaults={'grade': 10})
            for text, correct in choices:
                Choice.objects.get_or_create(question=question, choice_text=text, defaults={'is_correct': correct})
        self.stdout.write(self.style.SUCCESS('Demo course is ready.'))
