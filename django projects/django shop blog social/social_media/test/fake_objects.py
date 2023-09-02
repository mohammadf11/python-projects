import factory
from utils.user_factory import UserFactory



class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'social_media.Post'

    title = factory.Sequence(lambda n: f'title {n}')
    body =factory.Sequence(lambda n: f'body {n}')
    image = factory.Faker('image_url')
    

class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'social_media.Like'

class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'social_media.Follow'


def reset_sequence():
    FollowFactory.reset_sequence(1)
    LikeFactory.reset_sequence(1)
    PostFactory.reset_sequence(1)
    UserFactory.reset_sequence(1)
    