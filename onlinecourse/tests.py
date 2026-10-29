from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Course, Question, Choice, Submission

class ExamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='student', password='test-password')
        self.course = Course.objects.create(name='Test', description='Test course')
        self.q = Question.objects.create(course=self.course, question_text='Select both', grade=10)
        self.a = Choice.objects.create(question=self.q, choice_text='A', is_correct=True)
        self.b = Choice.objects.create(question=self.q, choice_text='B', is_correct=True)
        self.c = Choice.objects.create(question=self.q, choice_text='C')
        self.url = reverse('onlinecourse:submit', args=[self.course.pk])
        self.client.force_login(self.user)

    def test_exact_answers_pass_and_result_renders(self):
        response = self.client.post(self.url, {'choices': [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, 'Congratulations!')
        self.assertEqual(Submission.objects.get().score, 10)

    def test_partial_or_extra_answers_fail(self):
        for choices in ([self.a.pk], [self.a.pk, self.b.pk, self.c.pk], []):
            self.client.post(self.url, {'choices': choices})
        self.assertEqual(list(Submission.objects.values_list('score', flat=True)), [0, 0, 0])

    def test_foreign_and_invalid_choices_rejected(self):
        other = Course.objects.create(name='Other')
        q = Question.objects.create(course=other, question_text='Other')
        choice = Choice.objects.create(question=q, choice_text='Other')
        for choices in ([choice.pk], ['invalid']):
            self.assertEqual(self.client.post(self.url, {'choices': choices}).status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_result_private_and_snapshot_stable(self):
        response = self.client.post(self.url, {'choices': [self.a.pk, self.b.pk]})
        self.q.delete()
        self.assertContains(self.client.get(response.url), 'Congratulations!')
        other = get_user_model().objects.create_user(username='other')
        self.client.force_login(other)
        self.assertEqual(self.client.get(response.url).status_code, 404)

    def test_submission_requires_login_and_post(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_course_page(self):
        self.assertContains(self.client.get(reverse('onlinecourse:course_details', args=[self.course.pk])), 'Select both')
