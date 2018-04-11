import json

from.base_test import BaseTestCase
from api.models import LoggedActivity


class LoggedActivitiesTestCase(BaseTestCase):
    """Test activity types endpoints."""

    def setUp(self):
        # inherit parent tests setUp
        super().setUp()

        # add test users and logged activity
        self.test_user.save()
        self.test_user_2.save()
        self.log_alibaba_challenge.save()

    def test_get_logged_activities_by_user_id(self):
        test_user_id = self.test_user.uuid
        response = self.client.get(
            f'/api/v1/users/{test_user_id}/logged-activities',
            headers=self.header
        )

        # test that request was successful
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.get_data(as_text=True))
        logged_activities = LoggedActivity.query.filter_by(
            user_id=test_user_id).all()

        # test that response data matches database query results
        self.assertEqual(len(logged_activities), len(response_content['data']))

    def test_get_logged_activities_message_when_user_has_none(self):
        # test that users with no logged activities have a message in the response
        response = self.client.get(
            f'/api/v1/users/{self.test_user_2.uuid}/logged-activities',
            headers=self.header
        )
        response_content = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(response_content['data']), 0)

        message = "There are no logged activities for that user."
        self.assertEqual(response_content['message'], message)

    def test_get_logged_activities_message_when_user_does_not_exist(self):
        # test that users with no logged activities have a message in the response
        response = self.client.get(
            '/api/v1/users/user_id/logged-activities',
            headers=self.header
        )
        response_content = json.loads(response.get_data(as_text=True))

        self.assertEqual(response_content['message'], "User not found")
        self.assertEqual(response.status_code, 404)
