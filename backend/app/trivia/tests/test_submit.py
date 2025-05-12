from django.utils import timezone
from rest_framework import status
from trivia.models import Test, TestQuestion, TestParticipation, ParticipationResponse, AnswerOption
from trivia.tests.tests_create import BaseAPITest

class QuestionRetrieveAndAccessTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        t = Test.objects.create(title="Sample Test", multiplayer=False, time_limit_minutes=5)
        self.tq1 = TestQuestion.objects.create(test=t, question=self.question1, question_number=1)
        self.tq2 = TestQuestion.objects.create(test=t, question=self.question2, question_number=2)
        self.part = TestParticipation.objects.create(user=self.normal_user, test=t, score=0)
        self.participation_id = self.part.id
        self.start_url    = f"/trivia/tests/{self.participation_id}/question/1/start/"
        self.retrieve_url = f"/trivia/tests/{self.participation_id}/question/1/"

    def test_start_creates_participation_response_and_returns_statement(self):
        resp = self.client_user.get(self.start_url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        pr = ParticipationResponse.objects.filter(
            test_participation=self.part,
            test_question=self.tq1
        ).first()
        self.assertIsNotNone(pr)
        self.assertIsNone(pr.responded_at)
        self.assertIn("text", resp.data)
        self.assertIn("answer_options", resp.data)
        self.assertNotIn("explanation", resp.data)

    def test_standard_retrieve_does_not_create_participation_response(self):
        resp = self.client_user.get(self.retrieve_url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        exists = ParticipationResponse.objects.filter(
            test_participation=self.part,
            test_question=self.tq1
        ).exists()
        self.assertFalse(exists)


class AnswerSubmissionTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        t = Test.objects.create(title="Sample Test", multiplayer=False, time_limit_minutes=2)
        self.tq1 = TestQuestion.objects.create(test=t, question=self.question1, question_number=1)
        self.tq2 = TestQuestion.objects.create(test=t, question=self.question2, question_number=2)
        self.part = TestParticipation.objects.create(user=self.normal_user, test=t, score=0)
        self.participation_id = self.part.id
        self.start_url1  = f"/trivia/tests/{self.participation_id}/question/1/start/"
        self.answer_url1 = f"/trivia/tests/{self.participation_id}/question/1/answer/"
        self.start_url2  = f"/trivia/tests/{self.participation_id}/question/2/start/"
        self.answer_url2 = f"/trivia/tests/{self.participation_id}/question/2/answer/"

    def test_cannot_submit_before_start(self):
        option = AnswerOption.objects.filter(question=self.question1).first()
        resp = self.client_user.post(self.answer_url1, {"answer_option": option.id}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

    def test_submit_correct_answer_records_and_scores(self):
        self.client_user.get(self.start_url1, format="json")
        pr = ParticipationResponse.objects.get(test_participation=self.part, test_question=self.tq1)
        correct = AnswerOption.objects.get(question=self.question1, correct=True)
        before = timezone.now()
        resp = self.client_user.post(self.answer_url1, {"answer_option": correct.id}, format="json")
        after = timezone.now()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data
        self.assertTrue(data["is_correct"])
        self.assertIn("earned_score", data)
        earned = data["earned_score"]

        pr.refresh_from_db()
        self.assertIsNotNone(pr.responded_at)
        self.assertTrue(before <= pr.responded_at <= after)
        self.assertAlmostEqual(pr.score, earned, places=5)

        self.part.refresh_from_db()
        self.assertAlmostEqual(self.part.score, earned, places=5)

    def test_submit_incorrect_answer_scores_zero(self):
        self.client_user.get(self.start_url1, format="json")
        wrong = AnswerOption.objects.get(question=self.question1, correct=False)
        resp = self.client_user.post(self.answer_url1, {"answer_option": wrong.id}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data["is_correct"])
        self.assertEqual(resp.data["earned_score"], 0.0)

        pr = ParticipationResponse.objects.get(test_participation=self.part, test_question=self.tq1)
        self.assertEqual(pr.score, 0.0)
        self.part.refresh_from_db()
        self.assertEqual(self.part.score, 0.0)

    def test_double_submission_returns_error(self):
        self.client_user.get(self.start_url1, format="json")
        option = AnswerOption.objects.filter(question=self.question1).first()
        self.client_user.post(self.answer_url1, {"answer_option": option.id}, format="json")
        dup = self.client_user.post(self.answer_url1, {"answer_option": option.id}, format="json")
        self.assertEqual(dup.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", dup.data)

    def test_test_time_limit_expired(self):
        self.client_user.get(self.start_url1, format="json")
        # expire the test
        self.part.started_at = timezone.now() - timezone.timedelta(minutes=3)
        self.part.save(update_fields=["started_at"])
        correct = AnswerOption.objects.get(question=self.question1, correct=True)
        resp = self.client_user.post(self.answer_url1, {"answer_option": correct.id}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", resp.data)

    def test_per_question_time_limit_expired_scores_zero(self):
        self.client_user.get(self.start_url1, format="json")
        pr = ParticipationResponse.objects.get(test_participation=self.part, test_question=self.tq1)
        # total 2 minutes -> 120s, 2 questions -> 60s per question
        pr.accessed_at = timezone.now() - timezone.timedelta(seconds=61)
        pr.save(update_fields=["accessed_at"])

        correct = AnswerOption.objects.get(question=self.question1, correct=True)
        resp = self.client_user.post(self.answer_url1, {"answer_option": correct.id}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["earned_score"], 0.0)

        pr.refresh_from_db()
        self.assertEqual(pr.score, 0.0)
        self.part.refresh_from_db()
        self.assertEqual(self.part.score, 0.0)

    def test_final_result_included_on_last_question(self):
        # answer first question
        self.client_user.get(self.start_url1, format="json")
        correct1 = AnswerOption.objects.get(question=self.question1, correct=True)
        self.client_user.post(self.answer_url1, {"answer_option": correct1.id}, format="json")

        # answer second question
        self.client_user.get(self.start_url2, format="json")
        correct2 = AnswerOption.objects.get(question=self.question2, correct=True)
        resp = self.client_user.post(self.answer_url2, {"answer_option": correct2.id}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("final_result", resp.data)
        fr = resp.data["final_result"]
        self.assertEqual(fr["total_questions"], 2)
        self.assertEqual(fr["correct_answers"], 2)
        self.assertAlmostEqual(fr["total_score"], self.part.score, places=5)
