from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    def __str__(self): return self.user.get_username()

class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)
    def __str__(self): return self.user.get_username()

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ManyToManyField(Instructor, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    def __str__(self): return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']
    def __str__(self): return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'course'], name='unique_enrollment')]
    def __str__(self): return f'{self.user} — {self.course}'

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    def is_get_score(self, selected_ids):
        correct = set(self.choice_set.filter(is_correct=True).values_list('pk', flat=True))
        selected = set(self.choice_set.filter(pk__in=selected_ids).values_list('pk', flat=True))
        return bool(correct) and selected == correct
    def __str__(self): return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    def __str__(self): return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    results = models.JSONField(default=list)
    @property
    def percentage(self): return round(100 * self.score / self.total, 1) if self.total else 0
