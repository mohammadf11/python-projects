
import factory
import factory.fuzzy
from utils.user_factory import UserFactory

class ArticleCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.ArticleCategory'
    id = factory.Sequence(lambda n: n )
    name = factory.Sequence(lambda n: f'category {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')
    is_active = True


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Article'
    id = factory.Sequence(lambda n: n )
    title = factory.Sequence(lambda n: f'title {n}')
    slug = factory.Sequence(lambda n: f'title-{n}')
    description =factory.Sequence(lambda n: f'description {n}')
    image = factory.Faker('image_url')
    is_publish = factory.Sequence(lambda n: False if n % 2 == 0 else True)

def reset_sequence():
    ArticleFactory.reset_sequence(1)
    ArticleCategoryFactory.reset_sequence(1)
    UserFactory.reset_sequence(1)