from django.test import TestCase
from django.urls import reverse
from .fake_objects import UserFactory, ShapCategoryFactory, ProductFactory, reset_sequence
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from shop.models import ShopCategory, Product
from shop.cart import Cart
import pdb


class BaseTest(TestCase):
    _password = 'Ab12345!!'
    _path_image_test = 'media/image_blog/Screenshot_from_2022-08-15_22-05-09.png'
    _image_test_dir = 'test_image_dir/'

    def setUp(self) -> None:
        reset_sequence()
        self.normal_user = UserFactory(password=self._password)
        self.admin_user = UserFactory(is_admin=True)
        self.category = ShapCategoryFactory()
        self.products = [ProductFactory(
            category=self.category) for _ in range(20)]

    def login_url(self, url):
        return reverse('account:login') + f'?next={url}'


class TestPermisson(BaseTest):
    def setUp(self):
        super().setUp()
        self.delete_url = reverse('shop:product_delete', args=[1])

    def test_LoginRequiredMixin(self):
        # without login
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, self.login_url(self.delete_url), 302)

        # with login
        response = self.client.force_login(user = self.admin_user)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_IsStaffAccessMixins(self):
        # login with normal user
        response = self.client.force_login(user = self.normal_user)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)

        # login with normal user
        response = self.client.force_login(user = self.admin_user)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)


class TestProductLsitView(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('shop:product_list')
        self.template_name = 'shop/product_list.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['products']), 8)

    def test_get_page(self):
        response = self.client.get(self.url + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['products']), 8)

        response = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response.context['products']), 2)

        response = self.client.get(self.url + '?page=3')
        self.assertEqual(response.status_code, 404)


class TestProductDetailView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('shop:product_detail', args=[1])
        self.template_name = 'shop/product_detail.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(Product.objects.last(), response.context['product'])

    def test_dont_show_not_availabe_product(self):
        url = reverse('shop:product_detail', args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response)


class TestProductCreateView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('shop:product_create')
        self.template_name = 'shop/product_create.html'

    def test_post_invalid_data(self):
        response = self.client.force_login(user = self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 5)

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_post_valid_data(self):
        response = self.client.force_login(user = self.admin_user)

        self.assertEqual(Product.objects.count(), 20)
        data = {
            'name': 'new product',
            'description': 'description',
            'category': self.category.id,
            'price': 100,
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='image/jpeg')
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('shop:manage_product'), 302)
        self.assertEqual(Product.objects.count(), 21)
        self.assertEqual(Product.objects.first().name, 'new product')


class TestProductUpdateView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('shop:product_update', args=[1])
        self.template_name = 'shop/product_update.html'

    def test_update_invalid_data(self):
        response = self.client.force_login(user = self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.last().name, 'name 1')

    @override_settings(MEDIA_ROOT=BaseTest._image_test_dir)
    def test_update_valid_data(self):
        response = self.client.force_login(user = self.admin_user)
        response = self.client.post(self.url, {
            'name': 'update name-1',
            'description': 'update description-1',
            'category': self.category.id,
            'price': 200,
            'image': SimpleUploadedFile(name='test.jpg', content=open(self._path_image_test, 'rb').read(), content_type='image/jpeg')
        })
        self.assertRedirects(response, reverse('shop:manage_product'), 302)
        self.assertEqual(Product.objects.last().name, 'update name-1')


class TestProductDeletelView(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('shop:product_delete', args=[1])
        self.template_name = 'shop/product_delete.html'

    def test_get(self):
        response = self.client.force_login(user = self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_delete(self):
        self.assertTrue(Product.objects.filter(id=1).exists())
        response = self.client.force_login(user = self.admin_user)
        response = self.client.post(self.url)
        self.assertFalse(Product.objects.filter(id=1).exists())
        self.assertEqual(Product.objects.count(), 19)


class TestManageArticleView(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('shop:manage_product')
        self.template_name = 'shop/manage_product.html'

    def test_get(self):
        response = self.client.force_login(user = self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['products']), 20)


class TestCartView(BaseTest):
    def setUp(self):
        super().setUp()

        response = self.client.force_login(user = self.admin_user)

    def get_cart(self):
        response = self.client.get('/')
        request = response.context['request']
        cart = Cart(request)
        return cart

    def test_add_cart(self):
        url = reverse('shop:add_product_cart', args=[1])
        url2 = reverse('shop:add_product_cart', args=[3])
        self.client.post(url, {'quantity': 2})
        self.client.post(url2, {'quantity': 4})
        session_cart = self.client.session['cart']
        self.assertEqual(session_cart['1']['quantity'], 2)
        self.assertEqual(session_cart['1']['price'], 1001)
        self.assertEqual(session_cart['3']['quantity'], 4)
        self.assertEqual(session_cart['3']['price'], 1003)
        cart = self.get_cart()
        self.assertEqual(cart.get_total_price(), 6014)
        self.assertEqual(len(cart), 2)

    def test_remove_cart(self):
        self.test_add_cart()
        url = reverse('shop:remove_product_cart', args=[1])
        self.client.get(url)
        cart = self.get_cart()
        self.assertEqual(cart.get_total_price(), 4012)
        self.assertEqual(len(cart), 1)

    def test_cart(self):
        self.test_add_cart()
        url = reverse('shop:cart')
        response = self.client.get(url)
        cart = self.get_cart()

        self.assertEqual(response.context['cart'].get_total_price (), 6014)
        self.assertEqual(response.context['cart_count'] ,2)


