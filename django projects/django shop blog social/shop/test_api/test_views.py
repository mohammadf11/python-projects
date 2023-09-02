from rest_framework.test import APITestCase
from django.urls import reverse
from blog.test.fake_objects import UserFactory, ArticleFactory, ArticleCategoryFactory, reset_sequence
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from blog.models import Article, ArticleCategory
import pdb


class BaseTest(APITestCase):
    _password = 'Ab12345!!'
    _path_image_test = 'media/image_blog/Screenshot_from_2022-08-15_22-05-09.png'
    _image_test_dir = 'test_image_dir/'

    def setUp(self) -> None:
        reset_sequence()
        self.normal_user = UserFactory()
        self.admin_user = UserFactory(is_superuser=True, is_admin=True)
        self.category = ArticleCategoryFactory()
        self.articles = [ArticleFactory(
            author=self.admin_user,
            category=self.category)
            for _ in range(20)]

    def info_admin_user_login(self):
        return {
            'username': self.admin_user.phone_number,
            'password': self._password
        }

    def info_normal_user_login(self):
        return {
            'username': self.normal_user.phone_number,
            'password': self._password
        }

    def get_data(self):
        return {
            'title': 'new article',
            'slug': 'new-article',
            'description': 'description',
            'category': self.category.id,
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='multipart/form-data')
        }


class TestPermission(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.list_url = reverse('blog:api_article-list')
        self.detail_url = reverse('blog:api_article-detail', args=[1])

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_IsAuthenticated(self):
        response = self.client.post(self.list_url, self.get_data())
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.list_url, self.get_data())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), 21)

    def test_IsStaffAccessMixins(self):
        # login with normal user
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.list_url, self.get_data())
        self.assertEqual(response.status_code, 403)

        # login with admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.list_url, self.get_data())
        self.assertEqual(response.status_code, 201)

    def test_IsSuperuserOrOwnerAccessPermissions(self):
        # noraml_user
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)

        # admin_user but not owner
        admin_user2 = UserFactory(is_admin=True)
        self.client.force_authenticate(user=admin_user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)

        # superuser
        superuser = UserFactory(is_superuser=True, is_admin=True)
        self.client.force_authenticate(user=superuser)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)

        # admin_user and owner
        self.detail_url = reverse('blog:api_article-detail', args=[5])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)

