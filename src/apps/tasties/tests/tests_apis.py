import tempfile
from django.urls import reverse
from rest_framework import status
from PIL import Image
from apps.core.tests import BaseAPITestCase
from apps.user.models import User
from apps.general.models import FoodCategory


class TastyFoodsTestApi(BaseAPITestCase):

    def setUp(self) -> None:
        user_data = {
            "email": "safarnejad@fakemail.com",
            "password": "supersecret",
        }
        self.user = User.objects.create_user(**user_data)
        self.category = FoodCategory.objects.create(name='test-category')
        super().setUp()

    def test_create_tasty_unauthorized_401(self):
        url = reverse('tasties:tasties-list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tasty_invalid_data_400(self):
        url = reverse('tasties:tasties-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tasty_201(self):
        url = reverse('tasties:tasties-list')
        self.client.force_authenticate(user=self.user)

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        tasty = {
            "title": "test-tasty",
            "img": tmp_file,
            "recepie": "cook it :)",
            "duration": 20,
            "tags": ['tag1', 'tag2'],
            "category": self.category.id
        }

        response = self.client.post(url, data=tasty, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
