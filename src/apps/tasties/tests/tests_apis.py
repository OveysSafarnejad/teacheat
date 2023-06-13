# import os.path
# import tempfile
# from django.core.files.base import ContentFile
# from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
import json

from django.urls import reverse
from model_bakery import baker
from rest_framework import status
# from PIL import Image
from apps.core.tests import BaseAPITestCase
from apps.user.models import User
from apps.general.models import FoodCategory
from apps.tasties.models import Like, Tasty


class TastyFoodsTestApi(BaseAPITestCase):

    def setUp(self) -> None:
        self.other_chef = baker.make(User)
        self.category = baker.make(FoodCategory)
        self.other_chef_tasty = baker.make(Tasty, chef=self.other_chef)
        self.chef = baker.make(User)
        self.chef_tasty = baker.make(Tasty, chef=self.chef)

        super().setUp()

    def test_create_tasty_unauthorized_401(self):
        url = reverse('tasties:tasty-list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tasty_invalid_data_400(self):
        url = reverse('tasties:tasty-list')
        self.client.force_authenticate(user=self.chef)
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tasty_201(self):
        url = reverse('tasties:tasty-list')
        self.client.force_authenticate(user=self.chef)

        # image = Image.new('RGB', (100, 100))
        # tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        # image.save(tmp_file)
        # tmp_file.seek(0)

        tasty = dict(
            ingredients=[
                dict(name="salt", volume=1, unit=0),
                dict(name="tomato", volume=2, unit=1)
            ],
            title="test-tasty",
            # img=tmp_file,
            recipe="cook it :)",
            duration=20,
            tags=['tag1', 'tag2'],
            category=self.category.id
        )

        response = self.client.post(
            url,
            data=tasty,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_request_update_tasty_401(self):
        url = reverse('tasties:tasty-detail', kwargs={
            'pk': str(self.other_chef_tasty.id)
        })
        response = self.client.put(
            url,
            data={},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_tasty_update_by_chef_404(self):
        url = reverse('tasties:tasty-detail', kwargs={
            'pk': str(self.other_chef_tasty.id)
        })

        put_data = {
            "title": "Macaroni",
            "recipe": "Mix mac with tomato sause and meet.",
            "duration": 20,
            "tags": [
                "Fastfood", "Italian"
            ],
            "category": self.category.id,
            "ingredients": [
                {
                    "name": "tomato",
                    "volume": 2,
                    "unit": 1
                }
            ]
        }

        self.client.force_authenticate(user=self.chef)
        response = self.client.put(
            url,
            data=put_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tasty_by_chef_200(self):
        url = reverse('tasties:tasty-detail', kwargs={
            'pk': str(self.other_chef_tasty.id)
        })

        put_data = {
            "title": "Macaroni",
            "recipe": "Mix mac with tomato sause and meet.",
            "duration": 20,
            "tags": [
                "Fastfood", "Italian"
            ],
            "category": self.category.id,
            "ingredients": [
                {
                    "name": "tomato",
                    "volume": 2,
                    "unit": 1
                }
            ]
        }

        self.client.force_authenticate(user=self.other_chef)
        response = self.client.put(
            url,
            data=put_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(response['title'], put_data['title'])
        self.assertEqual(
            len(response['ingredients']),
            len(put_data['ingredients'])
        )

    def test_timeline_unauthenticated_user(self):
        url = reverse("tasties:tasty-list")
        response = self.client.get(url)
        response = json.loads(response.content)
        self.assertEqual(len(response), 2)

    def test_exclude_chef_tasties_from_her_timeline(self):
        url = reverse("tasties:tasty-list")
        self.client.force_authenticate(user=self.chef)
        response = self.client.get(url)
        response = json.loads(response.content)
        self.assertEqual(len(response), 1)

    def test_timeline_include_liked_tags_in_timeline(self):
        url = reverse("tasties:tasty-list")
        user_3 = baker.make(User)
        liked_tasty = baker.make(Tasty, chef=user_3, tags=['a', 'b'])
        baker.make(Tasty, chef=user_3, tags=['a', 'c'])
        baker.make(Tasty, chef=user_3, tags=['d'])
        baker.make(Like, user=self.chef, tasty=liked_tasty)
        self.client.force_authenticate(user=self.chef)

        response = self.client.get(url)
        response = json.loads(response.content)

        self.assertEqual(len(response), 4)

    def test_timeline_include_liked_chef_other_tasties(self):
        url = reverse("tasties:tasty-list")
        user_3 = baker.make(User)
        liked_tasty = baker.make(Tasty, chef=user_3)
        baker.make(Tasty, chef=user_3)
        baker.make(Tasty, chef=user_3)
        baker.make(Like, user=self.chef, tasty=liked_tasty)
        self.client.force_authenticate(user=self.chef)

        response = self.client.get(url)
        response = json.loads(response.content)

        self.assertEqual(len(response), 4)

    # TODO: tasties filters should be tested
