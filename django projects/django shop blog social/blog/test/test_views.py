from django.test import TestCase
from django.urls import reverse
from .fake_objects import UserFactory, ArticleFactory, ArticleCategoryFactory, reset_sequence
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from blog.models import Article, ArticleCategory
import pdb


class BaseTest(TestCase):
    _password = 'Ab12345!!'
    _path_image_test = 'media/image_blog/Screenshot_from_2022-08-15_22-05-09.png'
    _image_test_dir = 'test_image_dir/'

    def setUp(self) -> None:
        reset_sequence()
        self.normal_user = UserFactory()
        self.admin_user = UserFactory(is_admin=True)
        self.category = ArticleCategoryFactory()
        self.articles = [ArticleFactory(
            author=self.admin_user,
            category=self.category)
            for _ in range(20)]

    def login_url(self, url):
        return reverse('account:login') + f'?next={url}'


class TestPermisson(BaseTest):
    def setUp(self):
        super().setUp()
        self.delete_url = reverse('blog:article_delete', args=[1])
        self.create_url = reverse('blog:article_create')

    def test_LoginRequiredMixin(self):
        # without login
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, self.login_url(self.delete_url), 302)

        # with login
        response = self.client.force_login(user =self.admin_user)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_IsStaffAccessMixins(self):
        # login with normal user
        response = self.client.force_login(user =self.normal_user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)

        # login with normal user
        response = self.client.force_login(user =self.admin_user)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_IsSuperuserOrOwnerAccessPermissions(self):
        # noraml_user
        response = self.client.force_login(user =self.normal_user)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)

        # admin_user but not owner
        admin_user2 = UserFactory(is_admin=True)
        response = self.client.force_login(user =admin_user2)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)

        # superuser
        superuser = UserFactory(is_superuser=True)
        response = self.client.force_login(user =superuser)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)

        # admin_user and owner
        self.delete_url = reverse('blog:article_delete', args=[2])
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)


class TestArticleListView(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:article_list')
        self.template_name = 'blog/article_lsit.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['articles']), 6)

    def test_get_page(self):
        response = self.client.get(self.url + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['articles']), 6)

        response = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response.context['articles']), 4)

        response = self.client.get(self.url + '?page=3')
        self.assertEqual(response.status_code, 404)


class TestArticleDetailView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('blog:article_detail', args=[1])
        self.template_name = 'blog/article_detail.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(Article.objects.last(), response.context['article'])

    def test_dont_show_draft_article(self):
        draft_article_url = reverse('blog:article_detail', args=[2])
        response = self.client.get(draft_article_url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response)


class TestArticleCreatelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('blog:article_create')
        self.template_name = 'blog/article_create.html'

    def test_post_invalid_data(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 4)

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_post_valid_data(self):
        response = self.client.force_login(user =self.admin_user)

        self.assertEqual(Article.objects.count(), 20)
        data = {
            'title': 'new article',
            'description': 'description',
            'category': self.category.id,
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='image/jpeg')
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('blog:manage_article'), 302)
        self.assertEqual(Article.objects.count(), 21)
        self.assertNotEqual(Article.objects.last().author, self.normal_user)
        self.assertEqual(Article.objects.first().title, 'new article')
        self.assertEqual(Article.objects.first().author, self.admin_user)


class TestArticleUpdatelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('blog:article_update', args=[1])
        self.template_name = 'blog/article_update.html'

    def test_update_invalid_data(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Article.objects.last().author, self.normal_user)
        self.assertEqual(Article.objects.last().title, 'title 1')
        self.assertEqual(Article.objects.last().author, self.admin_user)

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_update_valid_data(self):
        response = self.client.force_login(user =self.admin_user)

        response = self.client.post(self.url, {
            'title': 'update title-1',
            'description': 'update description-1',
            'category': self.category.id,
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='image/jpeg')
        })
        self.assertRedirects(response, reverse('blog:manage_article'), 302)
        self.assertNotEqual(Article.objects.last().author, self.normal_user)
        self.assertEqual(Article.objects.last().title, 'update title-1')
        self.assertEqual(Article.objects.last().author, self.admin_user)


class TestArticleDeletelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('blog:article_delete', args=[1])
        self.template_name = 'blog/article_delete.html'

    def test_get(self):
        response = self.client.force_login(user =self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_delete_view_post_with_login(self):
        self.assertTrue(Article.objects.filter(id=1).exists())
        response = self.client.force_login(user =self.admin_user)
        response = self.client.post(self.url)
        self.assertFalse(Article.objects.filter(id=1).exists())
        self.assertEqual(Article.objects.count(), 19)


class TestManageArticleView(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:manage_article')
        self.template_name = 'blog/manage_article.html'

    def test_get(self):
        superuser = UserFactory(is_superuser=True , is_admin= True)
        ArticleFactory(
            author=superuser,
            category=self.category
        )
        #admin 
        response = self.client.force_login(user =self.admin_user)

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['articles']), 20)

        #superuser
        response = self.client.force_login(user =superuser)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['articles']), 21)
    
