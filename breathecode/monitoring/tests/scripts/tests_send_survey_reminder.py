from datetime import timedelta
from django.utils import timezone
from unittest.mock import patch, MagicMock, call, mock_open
from breathecode.tests.mocks import (
    GOOGLE_CLOUD_PATH,
    apply_google_cloud_client_mock,
    apply_google_cloud_bucket_mock,
    apply_google_cloud_blob_mock,
    MAILGUN_PATH,
    MAILGUN_INSTANCES,
    apply_mailgun_requests_post_mock,
    SLACK_PATH,
    SLACK_INSTANCES,
    apply_slack_requests_request_mock,
    REQUESTS_PATH,
    REQUESTS_INSTANCES,
    apply_requests_get_mock,
    LOGGING_PATH,
    LOGGING_INSTANCES,
    apply_logging_logger_mock
)
from ..mixins import MonitoringTestCase
from breathecode.monitoring.actions import run_script
from breathecode.admissions.models import Cohort, Academy


class AcademyCohortTestSuite(MonitoringTestCase):
    """
    🔽🔽🔽 With bad entity 🔽🔽🔽
    """
    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def tests_send_survey_reminder_no_survey(self):

        monitor_script_kwargs = {"script_slug": "send_survey_reminder"}

        model = self.generate_models(academy=True, monitor_script=True,
                                     monitor_script_kwargs=monitor_script_kwargs
                                     )

        script = run_script(model.monitor_script)

        del script['slack_payload']
        del script['text']

        expected = {
            "severity_level": 5,
            "status": 'OPERATIONAL',
        }

        self.assertEqual(script, expected)

        self.assertEqual(self.all_monitor_script_dict(), [{
            **self.model_to_dict(model, 'monitor_script'),
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def tests_send_survey_ending_date_less_than_now(self):

        monitor_script_kwargs = {"script_slug": "send_survey_reminder"}
        ending_date = timezone.now() - timedelta(weeks=1)
        sent_at = timezone.now() - timedelta(weeks=5)
        model = self.generate_models(cohort=True, monitor_script=True,
                                     monitor_script_kwargs=monitor_script_kwargs,
                                     cohort_kwargs={
                                         'ending_date': ending_date},
                                     survey=True, survey_kwargs={'sent_at': sent_at})

        script = run_script(model.monitor_script)

        del script['slack_payload']
        del script['text']
        
        expected = {
            "severity_level": 5,
            "status": 'OPERATIONAL',
        }
        self.assertEqual(script, expected)

        self.assertEqual(self.all_monitor_script_dict(), [{
            **self.model_to_dict(model, 'monitor_script'),
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def tests_send_survey_kickoff_date_greater_than_now(self):

        monitor_script_kwargs = {"script_slug": "send_survey_reminder"}
        kickoff_date = timezone.now() + timedelta(weeks=1)
        sent_at = timezone.now() - timedelta(weeks=5)
        model = self.generate_models(cohort=True, monitor_script=True,
                                     monitor_script_kwargs=monitor_script_kwargs,
                                     cohort_kwargs={
                                         'kickoff_date': kickoff_date},
                                     survey=True, survey_kwargs={'sent_at': sent_at})

        script = run_script(model.monitor_script)

        del script['slack_payload']
        del script['text']

        expected = {
            "severity_level": 5,
            "status": 'OPERATIONAL'
        }
        self.assertEqual(script, expected)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def tests_send_survey_latest_survey_less_four_weeks(self):

        monitor_script_kwargs = {"script_slug": "send_survey_reminder"}
        ending_date = timezone.now() + timedelta(weeks=2)
        kickoff_date = timezone.now() - timedelta(weeks=12)

        base = self.generate_models(academy=True, cohort=True, monitor_script=True,
                                    monitor_script_kwargs=monitor_script_kwargs,
                                    cohort_kwargs={'ending_date': ending_date,
                                                   "kickoff_date": kickoff_date})
        sent_at = timezone.now() - timedelta(weeks=2)
        models = [self.generate_models(survey=True, survey_kwargs={'sent_at': sent_at},
                                       models=base)
                  for _ in range(0, 2)]

        script = run_script(models[1].monitor_script)

        del script['slack_payload']
        del script['text']

        expected = {
            "severity_level": 5,
            "status": 'OPERATIONAL',
        }
        self.assertEqual(script, expected)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def tests_send_survey_latest_survey_greater_four_weeks(self):

        monitor_script_kwargs = {"script_slug": "send_survey_reminder"}
        ending_date = timezone.now() + timedelta(days=2)
        kickoff_date = timezone.now() - timedelta(days=2)

        base = self.generate_models(academy=True, cohort=True, monitor_script=True,
                                    monitor_script_kwargs=monitor_script_kwargs,
                                    cohort_kwargs={'ending_date': ending_date,
                                                   "kickoff_date": kickoff_date})

        sent_at = timezone.now() - timedelta(weeks=6)

        models = [self.generate_models(survey=True, survey_kwargs={'sent_at': sent_at},
                                       models=base)
                  for _ in range(0, 2)]

        script = run_script(models[1].monitor_script)

        del script['slack_payload']
        del script['text']


        expected = {
                    'severity_level': 5,
                    'error_slug': None,
                    'status': 'MINOR',
                    }

        self.assertEqual(script, expected)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def tests_send_survey_latest_survey_greater_four_weeks_two_cohorts_two_survey(self):

        monitor_script_kwargs = {"script_slug": "send_survey_reminder"}
        ending_date = timezone.now() + timedelta(days=2)
        kickoff_date = timezone.now() - timedelta(days=2)

        base = self.generate_models(academy=True,  monitor_script=True,
                                    monitor_script_kwargs=monitor_script_kwargs,
                                    )

        sent_at = timezone.now() - timedelta(weeks=6)

        models = [self.generate_models(survey=True, cohort=True, survey_kwargs={'sent_at': sent_at},
                                       models=base, cohort_kwargs={'ending_date': ending_date,
                                                                   "kickoff_date": kickoff_date})
                  for _ in range(0, 2)]

        script = run_script(models[1].monitor_script)
        del script['slack_payload']
        del script['text']

        expected = {
                    'severity_level': 5,
                    'status': 'MINOR',
                    'error_slug': None,
                    }

        self.assertEqual(script, expected)
