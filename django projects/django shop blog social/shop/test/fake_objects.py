
import factory
import factory.fuzzy
from utils.user_factory import UserFactory


class ShapCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shop.ShopCategory'
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f'category {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shop.Product'
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f'name {n}')
    slug = factory.Sequence(lambda n: f'name-{n}')
    description = factory.Sequence(lambda n: f'description {n}')
    price = factory.Sequence(lambda n: 1000 + n)
    image = factory.Faker('image_url')
    is_available = factory.Sequence(lambda n: False if n % 2 == 0 else True)


def reset_sequence():
    ShapCategoryFactory.reset_sequence(1)
    ProductFactory.reset_sequence(1)
    UserFactory.reset_sequence(1)
