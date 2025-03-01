"""
Collections of mixins used to login in authorize microservice
"""
from rest_framework.test import APITestCase
from breathecode.tests.mixins import GenerateModelsMixin, CacheMixin, GenerateQueriesMixin, DatetimeMixin, ICallMixin

class AdmissionsTestCase(APITestCase, GenerateModelsMixin, CacheMixin,
        GenerateQueriesMixin, DatetimeMixin, ICallMixin):
    """AdmissionsTestCase with auth methods"""
    def setUp(self):
        self.generate_queries()

    def tearDown(self):
        self.clear_cache()
