"""
Test /answer
"""
import re, urllib
from unittest.mock import patch
from django.urls.base import reverse_lazy
from rest_framework import status
from breathecode.tests.mocks import (
    GOOGLE_CLOUD_PATH,
    apply_google_cloud_client_mock,
    apply_google_cloud_bucket_mock,
    apply_google_cloud_blob_mock,
)
from ..mixins import MediaTestCase

class MediaTestSuite(MediaTestCase):
    """Test /answer"""

    """
    🔽🔽🔽 Auth
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__without_auth(self):
        """Test /answer without auth"""
        url = reverse_lazy('media:root')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__wrong_academy(self):
        """Test /answer without auth"""
        url = reverse_lazy('media:root')
        response = self.client.get(url, **{'HTTP_Academy': 1 })
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__without_capability(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        url = reverse_lazy('media:root')
        self.generate_models(authenticate=True)
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, {
            'detail': "You (user: 1) don't have this capability: read_media for academy 1",
            'status_code': 403
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    🔽🔽🔽 Without data
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__without_data(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        models = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')
        url = reverse_lazy('media:root')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [])

    """
    🔽🔽🔽 With data
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True)
        url = reverse_lazy('media:root')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    """
    🔽🔽🔽 Academy in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_academy_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?academy=0'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_academy_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?academy=1'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_two_academy_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')

        del base['academy']

        models = [self.generate_models(academy=True, media=True, category=True, models=base)
            for _ in range(0, 2)]

        url = (reverse_lazy('media:root') + '?academy=' +
            str(models[0]['media'].academy.id) + ',' + str(models[1]['media'].academy.id))
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(json, [{
            'categories': [{
                'id': model['category'].id,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    """
    🔽🔽🔽 Mime in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_mime_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?mime=application/hitman'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_mime_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?mime=' + model['media'].mime
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_two_mime_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')

        models = [self.generate_models(media=True, category=True, models=base)
            for _ in range(0, 2)]

        url = reverse_lazy('media:root') + '?mime=' + models[0]['media'].mime + ',' + models[1]['media'].mime
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(json, [{
            'categories': [{
                'id': model['category'].id,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    """
    🔽🔽🔽 Name in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_name_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?name=hitman'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_name_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?name=' + model['media'].name
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_two_name_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')

        models = [self.generate_models(media=True, category=True, models=base)
            for _ in range(0, 2)]

        url = (reverse_lazy('media:root') + '?name=' + models[0]['media'].name +
            ',' + models[1]['media'].name)
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(json, [{
            'categories': [{
                'id': model['category'].id,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    """
    🔽🔽🔽 Slug in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_slug_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?slug=hitman'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_slug_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?slug=' + model['media'].slug
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_two_slug_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')

        models = [self.generate_models(media=True, category=True, models=base)
            for _ in range(0, 2)]

        url = (reverse_lazy('media:root') + '?slug=' + models[0]['media'].slug +
            ',' + models[1]['media'].slug)
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(json, [{
            'categories': [{
                'id': model['category'].id,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    """
    🔽🔽🔽 Id in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_id_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?id=0'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_id_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?id=' + str(model['media'].id)
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_two_id_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')

        models = [self.generate_models(media=True, category=True, models=base)
            for _ in range(0, 2)]

        url = (reverse_lazy('media:root') + '?id=' + str(models[0]['media'].id) +
            ',' + str(models[1]['media'].id))
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(json, [{
            'categories': [{
                'id': model['category'].id,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    """
    🔽🔽🔽 Categories in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_categories_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?categories=0'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_categories_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?categories=1'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_two_categories_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)

        base = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato')

        models = [self.generate_models(media=True, category=True, models=base)
            for _ in range(0, 2)]

        url = (reverse_lazy('media:root') + '?categories=1,2')
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(json, [{
            'categories': [{
                'id': model['category'].id,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    """
    🔽🔽🔽 Type in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_type_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?type=freyja'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_type_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        media_kwargs = {'mime': 'application/pdf'}
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True,
            media_kwargs=media_kwargs)
        url = reverse_lazy('media:root') + '?type=pdf'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    """
    🔽🔽🔽 Like in querystring
    """

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_bad_like_in_querystring(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True)
        url = reverse_lazy('media:root') + '?like=freyja'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_like_in_querystring__like_match_name(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        media_kwargs = {'name': 'Freyja'}
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True,
            media_kwargs=media_kwargs)
        url = reverse_lazy('media:root') + '?like=fre'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_root__with_category__with_like_in_querystring__like_match_slug(self):
        """Test /answer without auth"""
        self.headers(academy=1)
        media_kwargs = {'slug': 'freyja'}
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='read_media', role='potato', media=True, category=True,
            media_kwargs=media_kwargs)
        url = reverse_lazy('media:root') + '?like=Fre'
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'categories': [{
                'id': 1,
                'medias': 1,
                'name': model['category'].name,
                'slug': model['category'].slug,
            }],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        }])

    """
    🔽🔽🔽 Pagination tests
    """

    def test_root__pagination__with_105(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        base = self.generate_models(authenticate=True, role=role,
            capability='read_media', profile_academy=True)

        models = [self.generate_models(media=True, models=base)
            for _ in range(0, 105)]
        url = reverse_lazy('media:root')
        response = self.client.get(url)
        json = response.json()
        expected = [{
            'categories': [],
            'hash': model['media'].hash,
            'hits': model['media'].hits,
            'id': model['media'].id,
            'mime': model['media'].mime,
            'name': model['media'].name,
            'slug': model['media'].slug,
            'url': model['media'].url
        } for model in models if model['media'].id < 101]

        self.assertEqual(json, expected)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    def test_root__pagination__first_five(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        base = self.generate_models(authenticate=True, role=role,
            capability='read_media', profile_academy=True)

        models = [self.generate_models(media=True, models=base)
            for _ in range(0, 10)]
        url = reverse_lazy('media:root') + '?limit=5&offset=0'
        response = self.client.get(url)
        json = response.json()
        expected = {
            'count': 10,
            'first': None,
            'last': 'http://testserver/v1/media/?limit=5&offset=5',
            'next': 'http://testserver/v1/media/?limit=5&offset=5',
            'previous': None,
            'results': [{
                'categories': [],
                'hash': model['media'].hash,
                'hits': model['media'].hits,
                'id': model['media'].id,
                'mime': model['media'].mime,
                'name': model['media'].name,
                'slug': model['media'].slug,
                'url': model['media'].url
            } for model in models if model['media'].id < 6]
        }

        self.assertEqual(json, expected)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    def test_root__pagination__last_five(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        base = self.generate_models(authenticate=True, role=role,
            capability='read_media', profile_academy=True)

        models = [self.generate_models(media=True, models=base)
            for _ in range(0, 10)]
        url = reverse_lazy('media:root') + '?limit=5&offset=5'
        response = self.client.get(url)
        json = response.json()
        expected = {
            'count': 10,
            'first': 'http://testserver/v1/media/?limit=5',
            'last': None,
            'next': None,
            'previous': 'http://testserver/v1/media/?limit=5',
            'results': [{
                'categories': [],
                'hash': model['media'].hash,
                'hits': model['media'].hits,
                'id': model['media'].id,
                'mime': model['media'].mime,
                'name': model['media'].name,
                'slug': model['media'].slug,
                'url': model['media'].url
            } for model in models if model['media'].id > 5]
        }

        self.assertEqual(json, expected)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])

    def test_root__pagination__after_last_five(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        base = self.generate_models(authenticate=True, role=role,
            capability='read_media', profile_academy=True)

        models = [self.generate_models(media=True, models=base)
            for _ in range(0, 10)]
        url = reverse_lazy('media:root') + '?limit=5&offset=10'
        response = self.client.get(url)
        json = response.json()
        expected = {
            'count': 10,
            'first': 'http://testserver/v1/media/?limit=5',
            'last': None,
            'next': None,
            'previous': 'http://testserver/v1/media/?limit=5&offset=5',
            'results': []
        }

        self.assertEqual(json, expected)
        self.assertEqual(self.all_media_dict(), [{
            **self.model_to_dict(model, 'media')
        } for model in models])
