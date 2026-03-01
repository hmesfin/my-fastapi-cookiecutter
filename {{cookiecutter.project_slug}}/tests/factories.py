import factory

from {{ cookiecutter.project_slug }}.auth.models import User
from {{ cookiecutter.project_slug }}.auth.security import hash_password


class UserFactory(factory.Factory):
  class Meta:
    model = User

  email = factory.Sequence(lambda n: f"user{n}@example.com")
  hashed_password = factory.LazyFunction(lambda: hash_password("testpassword123"))
  full_name = factory.Faker("name")
  is_active = True
  is_superuser = False
