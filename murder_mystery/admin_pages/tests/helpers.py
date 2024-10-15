from typing import Tuple, List

from characters.models import Character
from django.contrib.auth.models import User

def save_all(model_objects):
    for obj in model_objects:
        obj.save()

# --- Users --- #
def make_admin_user() -> User:
    '''Creates a admin user and returns it'''
    user = User.objects.create_superuser(
            username='admin',
            password='admin'
            )
    return user


# --- Characters --- #
def make_default_character(user):
    return Character(
        username=user,
        past_or_future='p',
        solo=False
    )

def make_n_users_and_characters(n: int) -> Tuple[List[User], List[Character]]:
    '''Creates n Users and associated Charactersr'''
    users = [User(username=num) for num in range(n)]
    chars = [make_default_character(user) for user in users]

    return  (users, chars)
