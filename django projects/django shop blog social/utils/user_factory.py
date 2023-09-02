import factory
from django.contrib.auth import get_user_model
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    id = factory.Sequence(lambda n: n )
    phone_number = factory.Sequence(lambda n: f'{9000000000 + n}')
    email = factory.LazyAttribute(
        lambda obj: f'{obj.phone_number}@gmail.com')
    password = factory.PostGenerationMethodCall('set_password', 'Ab12345!!')
    # email = factory.Faker('email')