"""
Test /cohort/user
"""
import re
from random import choice
from unittest.mock import patch
from django.urls.base import reverse_lazy
from rest_framework import status
from breathecode.tests.mocks import (
    GOOGLE_CLOUD_PATH,
    apply_google_cloud_client_mock,
    apply_google_cloud_bucket_mock,
    apply_google_cloud_blob_mock,
)
from ..mixins.new_admissions_test_case import AdmissionsTestCase

class CohortUserTestSuite(AdmissionsTestCase):
    """Test /cohort/user"""

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_without_auth(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, {
            'detail': 'Authentication credentials were not provided.',
            'status_code': status.HTTP_401_UNAUTHORIZED
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_without_data(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_cohort', role='potato')
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 0)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.get(url)
        json = response.json()
        expected = [{
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_bad_roles(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?roles=they-killed-kenny'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_roles(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?roles=' + model['cohort_user'].role
        response = self.client.get(url)
        json = response.json()
        expected = [{
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_roles_with_comma(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?roles=' + model['cohort_user'].role + ',they-killed-kenny'
        response = self.client.get(url)
        json = response.json()

        expected = [{
            # 'id': model['cohort_user'].id,
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_bad_finantial_status(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?finantial_status=they-killed-kenny'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_finantial_status(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'finantial_status': 'LATE'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?finantial_status=' + model['cohort_user'].finantial_status
        response = self.client.get(url)
        json = response.json()
        expected = [{
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_finantial_status_with_comma(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'finantial_status': 'LATE'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = (f'{base_url}?finantial_status=' + model['cohort_user'].finantial_status +
            ',they-killed-kenny')
        response = self.client.get(url)
        json = response.json()
        expected = [{
            # 'id': model['cohort_user'].id,
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_bad_educational_status(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?educational_status=they-killed-kenny'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_educational_status(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'educational_status': 'GRADUATED'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?educational_status=' + model['cohort_user'].educational_status
        response = self.client.get(url)
        json = response.json()
        expected = [{
            # 'id': model['cohort_user'].id,
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_educational_status_with_comma(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'educational_status': 'GRADUATED'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = (f'{base_url}?educational_status=' + model['cohort_user'].educational_status + ','
            'they-killed-kenny')
        response = self.client.get(url)
        json = response.json()
        expected = [{
            # 'id': model['cohort_user'].id,
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_academy(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'educational_status': 'GRADUATED'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?academy=' + model['cohort_user'].cohort.academy.slug
        response = self.client.get(url)
        json = response.json()
        expected = [{
            # 'id': model['cohort_user'].id,
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_academy_with_comma(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'educational_status': 'GRADUATED'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?academy=' + model['cohort_user'].cohort.academy.slug + ',they-killed-kenny'
        response = self.client.get(url)
        json = response.json()
        expected = [{
            # 'id': model['cohort_user'].id,
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_bad_cohorts(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?cohorts=they-killed-kenny'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_with_data_with_cohorts(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort_user=True,
            cohort_user_kwargs={'educational_status': 'GRADUATED'},
            profile_academy=True, capability='read_cohort', role='potato')
        model_dict = self.remove_dinamics_fields(model['cohort_user'].__dict__)
        base_url = reverse_lazy('admissions:academy_cohort_user')
        url = f'{base_url}?cohorts=' + model['cohort_user'].cohort.slug
        response = self.client.get(url)
        json = response.json()
        expected = [{
            # 'id': model['cohort_user'].id,
            'role': model['cohort_user'].role,
            'finantial_status': model['cohort_user'].finantial_status,
            'educational_status': model['cohort_user'].educational_status,
            'created_at': re.sub(r'\+00:00$', 'Z', model['cohort_user'].created_at.isoformat()),
            'user': {
                'id': model['cohort_user'].user.id,
                'first_name': model['cohort_user'].user.first_name,
                'last_name': model['cohort_user'].user.last_name,
                'email': model['cohort_user'].user.email,
            },
            'cohort': {
                'id': model['cohort_user'].cohort.id,
                'slug': model['cohort_user'].cohort.slug,
                'name': model['cohort_user'].cohort.name,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort_user'].cohort.kickoff_date.isoformat()
                ),
                'ending_date': model['cohort_user'].cohort.ending_date,
                'stage': model['cohort_user'].cohort.stage,
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.get_cohort_user_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_put_without_id(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_user')
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')
        data = {}
        response = self.client.put(url, data)
        json = response.json()

        self.assertEqual(json, {'status_code': 400, 'detail': 'Missing cohort_id or user_id'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_put_in_bulk_without_data(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_user')
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')
        data = []
        response = self.client.put(url, data, format='json')
        json = response.json()
        expected = []

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_put_in_bulk_without_data(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_user')
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')
        data = [{}]
        response = self.client.put(url, data, format='json')
        json = response.json()
        expected = {
            'detail': 'Cannot determine CohortUser in index 0',
            'status_code': 400
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_put_in_bulk_with_one_item(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_user')
        model = self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='crud_cohort', role='potato')
        data = [{
            'id': model['cohort_user'].id
        }]
        response = self.client.put(url, data, format='json')
        json = response.json()
        expected = [{
            'id': 1,
            'role': 'STUDENT',
            'educational_status': None,
            'finantial_status': None
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_cohort_user_dict(), [{
            'id': 1,
            'user_id': 1,
            'cohort_id': 1,
            'role': 'STUDENT',
            'finantial_status': None,
            'educational_status': None
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_user_put_in_bulk_with_two_items(self):
        """Test /cohort/user without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_user')
        model = [self.generate_models(authenticate=True, cohort_user=True,
            profile_academy=True, capability='crud_cohort', role='potato')]

        base = model[0].copy()
        del base['user']
        del base['cohort']
        del base['cohort_user']
        del base['profile_academy']

        model = model + [self.generate_models(cohort_user=True, profile_academy=True,
            models=base)]

        data = [{
            'id': 1,
            'finantial_status': 'LATE',
        }, {
            'user': '2',
            'cohort': '2',
            'educational_status': 'GRADUATED'
        }]
        response = self.client.put(url, data, format='json')
        json = response.json()
        expected = [{
            'id': 1,
            'role': 'STUDENT',
            'educational_status': None,
            'finantial_status': 'LATE',
        }, {
            'id': 2,
            'role': 'STUDENT',
            'educational_status': 'GRADUATED',
            'finantial_status': None
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_cohort_user_dict(), [{
            'id': 1,
            'user_id': 1,
            'cohort_id': 1,
            'role': 'STUDENT',
            'finantial_status': 'LATE',
            'educational_status': None
        }, {
            'id': 2,
            'user_id': 2,
            'cohort_id': 2,
            'role': 'STUDENT',
            'finantial_status': None,
            'educational_status': 'GRADUATED'
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_post_in_bulk_0_items(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True,
            profile_academy=True, capability='crud_cohort', role='potato')
        url = reverse_lazy('admissions:academy_cohort_user')
        data = []
        response = self.client.post(url, data, format='json')
        json = response.json()
        expected = []

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_post_in_bulk_1_items(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, user=True,
            profile_academy=True, capability='crud_cohort', role='potato')
        url = reverse_lazy('admissions:academy_cohort_user')
        data = [{
            'user':  model['user'].id,
            'cohort':  model['cohort'].id,
        }]
        response = self.client.post(url, data, format='json')
        json = response.json()
        expected = [{
            'id': 1,
            'role': 'STUDENT',
            'user': {
                'id': model['user'].id,
                'first_name': model['user'].first_name,
                'last_name': model['user'].last_name,
                'email': model['user'].email,
            },
            'cohort': {
                'id': model['cohort'].id,
                'slug': model['cohort'].slug,
                'name': model['cohort'].name,
                'never_ends': False,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort'].kickoff_date.isoformat()
                ),
                'current_day': model['cohort'].current_day,
                'academy': {
                    'id': model['cohort'].academy.id,
                    'name': model['cohort'].academy.name,
                    'slug': model['cohort'].academy.slug,
                    'country': model['cohort'].academy.country.code,
                    'city': model['cohort'].academy.city.id,
                    'street_address': model['cohort'].academy.street_address,
                },
                'syllabus': None,
                'ending_date': model['cohort'].ending_date,
                'stage': model['cohort'].stage,
                'language': model['cohort'].language,
                'created_at': re.sub(r'\+00:00$', 'Z', model['cohort'].created_at.isoformat()),
                'updated_at': re.sub(r'\+00:00$', 'Z', model['cohort'].updated_at.isoformat()),
            },
        }]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.all_cohort_user_dict(), [{
            'cohort_id': 1,
            'educational_status': None,
            'finantial_status': None,
            'id': 1,
            'role': 'STUDENT',
            'user_id': 1,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_post_in_bulk_2_items(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        base = self.generate_models(authenticate=True, cohort=True,
            profile_academy=True, capability='crud_cohort', role='potato')
        del base['user']

        models = [self.generate_models(user=True, models=base) for _ in range(0, 2)]
        url = reverse_lazy('admissions:academy_cohort_user')
        data = [{
            'user':  model['user'].id,
            'cohort':  models[0]['cohort'].id,
        } for model in models]
        response = self.client.post(url, data, format='json')
        json = response.json()
        expected = [{
            'id': model['user'].id - 1,
            'role': 'STUDENT',
            'user': {
                'id': model['user'].id,
                'first_name': model['user'].first_name,
                'last_name': model['user'].last_name,
                'email': model['user'].email,
            },
            'cohort': {
                'id': model['cohort'].id,
                'slug': model['cohort'].slug,
                'name': model['cohort'].name,
                'never_ends': False,
                'kickoff_date': re.sub(
                    r'\+00:00$', 'Z',
                    model['cohort'].kickoff_date.isoformat()
                ),
                'current_day': model['cohort'].current_day,
                'academy': {
                    'id': model['cohort'].academy.id,
                    'name': model['cohort'].academy.name,
                    'slug': model['cohort'].academy.slug,
                    'country': model['cohort'].academy.country.code,
                    'city': model['cohort'].academy.city.id,
                    'street_address': model['cohort'].academy.street_address,
                },
                'syllabus': None,
                'ending_date': model['cohort'].ending_date,
                'stage': model['cohort'].stage,
                'language': model['cohort'].language,
                'created_at': re.sub(r'\+00:00$', 'Z', model['cohort'].created_at.isoformat()),
                'updated_at': re.sub(r'\+00:00$', 'Z', model['cohort'].updated_at.isoformat()),
            },
        } for model in models]

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.all_cohort_user_dict(), [{
            'cohort_id': 1,
            'educational_status': None,
            'finantial_status': None,
            'id': 1,
            'role': 'STUDENT',
            'user_id': 2,
        }, {
            'cohort_id': 1,
            'educational_status': None,
            'finantial_status': None,
            'id': 2,
            'role': 'STUDENT',
            'user_id': 3,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_delete_without_auth(self):
        """Test /cohort/:id/user without auth"""
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.delete(url)
        json = response.json()
        expected = {
            'detail': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_delete_without_header(self):
        """Test /cohort/:id/user without auth"""
        model = self.generate_models(authenticate=True)
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.delete(url)
        json = response.json()
        expected = {
            'detail': 'Missing academy_id parameter expected for the endpoint url or \'Academy\' header',
            'status_code': 403
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_delete_without_capability(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True)
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.delete(url)
        json = response.json()
        expected = {
            'detail': "You (user: 1) don't have this capability: crud_cohort for academy 1",
            'status_code': 403
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_delete_without_args_in_url_or_bulk(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')
        url = reverse_lazy('admissions:academy_cohort_user')
        response = self.client.delete(url)
        json = response.json()
        expected = {
            'detail': "Missing user_id or cohort_id",
            'status_code': 400
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_delete_in_bulk_with_one(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        many_fields = ['id']

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')

        del base['user']
        del base['cohort']

        for field in many_fields:
            cohort_user_kwargs = {
                'role': choice(['STUDENT', 'ASSISTANT', 'TEACHER']),
                'finantial_status': choice(['FULLY_PAID', 'UP_TO_DATE', 'LATE']),
                'educational_status': choice(['ACTIVE', 'POSTPONED', 'SUSPENDED',
                    'GRADUATED', 'DROPPED']),
            }
            model = self.generate_models(cohort_user=True,
                cohort_user_kwargs=cohort_user_kwargs, models=base)
            url = (reverse_lazy('admissions:academy_cohort_user') + f'?{field}=' +
                str(getattr(model['cohort_user'], field)))
            response = self.client.delete(url)

            if response.status_code != 204:
                print(response.json())

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.all_cohort_user_dict(), [])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_user_delete_in_bulk_with_two(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        many_fields = ['id']

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')

        del base['user']
        del base['cohort']

        for field in many_fields:
            cohort_user_kwargs = {
                'role': choice(['STUDENT', 'ASSISTANT', 'TEACHER']),
                'finantial_status': choice(['FULLY_PAID', 'UP_TO_DATE', 'LATE']),
                'educational_status': choice(['ACTIVE', 'POSTPONED', 'SUSPENDED',
                    'GRADUATED', 'DROPPED']),
            }
            model1 = self.generate_models(cohort_user=True,
                cohort_user_kwargs=cohort_user_kwargs, models=base)

            cohort_user_kwargs = {
                'role': choice(['STUDENT', 'ASSISTANT', 'TEACHER']),
                'finantial_status': choice(['FULLY_PAID', 'UP_TO_DATE', 'LATE']),
                'educational_status': choice(['ACTIVE', 'POSTPONED', 'SUSPENDED',
                    'GRADUATED', 'DROPPED']),
            }
            model2 = self.generate_models(cohort_user=True,
                cohort_user_kwargs=cohort_user_kwargs, models=base)
            url = (reverse_lazy('admissions:academy_cohort_user') + f'?{field}=' +
                str(getattr(model1['cohort_user'], field)) + ',' +
                str(getattr(model2['cohort_user'], field)))
            response = self.client.delete(url)

            if response.status_code != 204:
                print(response.json())

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.all_cohort_user_dict(), [])
