import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class RegressionTests(TestCase):
    def test_future_poll_voting_prevention(self):
        """
        Users should not be able to vote on polls published in the future.
        Expecting a 404 Not Found.
        """
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question.objects.create(
            question_text="Future question.",
            pub_date=future_time,
        )
        Choice.objects.create(question=future_question, choice_text="Choice 1", votes=0)
        
        url = reverse("polls:vote", args=(future_question.id,))
        response = self.client.post(url, {'choice': 1})
        
        # Should be 404 because get_object_or_404 filters by pub_date__lte=now
        self.assertEqual(response.status_code, 404)

    def test_duplicate_empty_choice_cleanup(self):
        """
        Submitting duplicate or empty choices should be cleaned up:
        - Empty strings removed
        - Duplicates removed (keeping one)
        """
        # This test assumes we are using the CreatePollView which processes the form
        # We need to log in first as CreatePollView is LoginRequired
        User = __import__('django.contrib.auth').contrib.auth.get_user_model()
        user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.client.force_login(user)
        
        url = reverse("polls:create")
        data = {
            'question_text': 'Clean up test',
            'choices': "Alpha\nBeta\nAlpha\n\nGamma\n "
        }
        
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("polls:detail", args=(1,))) # Assuming ID 1
        
        question = Question.objects.first()
        choices = list(question.choice_set.values_list('choice_text', flat=True))
        
        # Expecting: Alpha, Beta, Gamma (3 choices)
        self.assertEqual(len(choices), 3)
        self.assertIn('Alpha', choices)
        self.assertIn('Beta', choices)
        self.assertIn('Gamma', choices)
