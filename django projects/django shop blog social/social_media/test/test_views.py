from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from utils.user_factory import UserFactory
from social_media.models import Like , Post
from .fake_objects import PostFactory, LikeFactory, FollowFactory, reset_sequence


class BaseTest(TestCase):
    _password = 'Ab12345!!'
    _path_image_test = 'media/image_blog/Screenshot_from_2022-08-15_22-05-09.png'
    _image_test_dir = 'test_image_dir/'

    def setUp(self) -> None:
        reset_sequence()
        self.normal_user = UserFactory()
        self.admin_user = UserFactory(is_admin=True)
        self.posts = [PostFactory(user=self.normal_user) for _ in range(20)]

    def login_url(self, url):
        return reverse('account:login') + f'?next={url}'


class TestPermisson(BaseTest):
    def setUp(self):
        super().setUp()

    def get_url(self, id):
        return reverse('social_media:post_update', args=[1])

    def test_LoginRequiredMixin(self):
        # without login
        response = self.client.get(self.get_url(1))
        self.assertRedirects(response, self.login_url(self.get_url(1)), 302)

        # with login
        response = self.client.force_login(user =self.admin_user)
        response = self.client.get(self.get_url(1))
        self.assertEqual(response.status_code, 200)

    def test_IsStaffOrOwnerModifiedPostMixin(self):

        #login with normal user but not owner
        normal_user2 = UserFactory()
        response = self.client.force_login(user =normal_user2)
        response = self.client.get(self.get_url(1))
        self.assertRedirects(response , reverse("social_media:post_list") , 302) 

        # login with normal user and owner
        response = self.client.force_login(user =self.normal_user)
        response = self.client.get(self.get_url(1))
        self.assertEqual(response.status_code, 200)

        # login with normal user
        response = self.client.force_login(user =self.admin_user)
        response = self.client.get(self.get_url(2))
        self.assertEqual(response.status_code, 200)

    def test_OneLikeMixin(self):
        self.assertEqual(Like.objects.count() , 0)

        response = self.client.force_login(user =self.normal_user)
        url = reverse('social_media:like_post',args=[1])
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)

        self.assertEqual(Like.objects.count() , 1)



class TestPostListView(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('social_media:post_list')
        self.template_name = 'social_media/post_list.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['posts']), 9)

    def test_get_page(self):
        response = self.client.get(self.url + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['posts']), 9)

        response = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response.context['posts']), 9)

        response = self.client.get(self.url + '?page=4')
        self.assertEqual(response.status_code, 404)



class TestPostCreatelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('social_media:post_create')
        self.template_name = 'social_media/post_create.html'

    def test_post_invalid_data(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 3)

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_post_valid_data(self):
        response = self.client.force_login(user =self.normal_user)

        self.assertEqual(Post.objects.count(), 20)
        data = {
            'title': 'new post',
            'body': 'body',
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='image/jpeg')
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('social_media:post_list'), 302)
        self.assertEqual(Post.objects.count(), 21)
        self.assertNotEqual(Post.objects.last().user, self.admin_user)
        self.assertEqual(Post.objects.first().title, 'new post')
        self.assertEqual(Post.objects.first().user, self.normal_user)


class TestPostUpdatelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('social_media:post_update', args=[1])
        self.template_name = 'social_media/post_update.html'

    def test_update_invalid_data(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.last().title, 'title 1')
        self.assertNotEqual(Post.objects.last().user, self.admin_user)
        self.assertEqual(Post.objects.last().user, self.normal_user)

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_update_valid_data(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url, {
            'title': 'update title-1',
            'body': 'body',
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='image/jpeg')
        })
        self.assertRedirects(response, reverse('social_media:post_list'), 302)
        self.assertEqual(Post.objects.last().title, 'update title-1')
        self.assertNotEqual(Post.objects.last().user, self.admin_user)
        self.assertEqual(Post.objects.last().user, self.normal_user)


class TestArticleDeletelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('social_media:post_delete', args=[1])
        self.template_name = 'social_media/post_delete.html'

    def test_get(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_delete_view_post_with_login(self):
        self.assertTrue(Post.objects.filter(id=1).exists())
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url)
        self.assertFalse(Post.objects.filter(id=1).exists())
        self.assertEqual(Post.objects.count(), 19)


class TesLikeView(BaseTest):
    def setUp(self) -> None:
        super().setUp()

    def test_like(self):
        url = reverse('social_media:like_post', args=[1])
        self.assertEqual(Like.objects.count() , 0)
        response = self.client.force_login(user =self.normal_user)
        self.client.get(url)
        self.assertEqual(Like.objects.count() , 1)

    def test_dislike(self):
        url = reverse('social_media:dislike_post', args=[1])
        self.test_like()
        self.assertEqual(Like.objects.count() , 1)
        response = self.client.force_login(user =self.normal_user)
        self.client.get(url)
        self.assertEqual(Like.objects.count() , 0)



