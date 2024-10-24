from django.contrib.auth.models import User

from admin_pages.tests.helpers import save_all
from characters.models import Character

def make_unique_default_users_and_chars():
    for user in User.objects.all():
        print(user.username)
    users = [User(username=num+9999) for num in range(10)]
    save_all(users)

    chars = [

            Character(
                username=users[0],
                real_name='Adam',
                character_name='Apple',
                past_or_future='Past',
                occupation='Accountant',
                descriptor1='able',
                descriptor2='agile',
                descriptor3='alert',
                solo=True
                ),
            Character(
                username=users[1],
                real_name='Bob',
                character_name='Banana',
                past_or_future='Past',
                occupation='Bartender',
                descriptor1='buff',
                descriptor2='bunt',
                descriptor3='bright',
                solo=True
                ),
            Character(
                username=users[2],
                real_name='Charles',
                character_name='Coconut',
                past_or_future='Past',
                occupation='Cashier',
                descriptor1='callous',
                descriptor2='candid',
                descriptor3='charming',
                solo=True
                ),
            Character(
                username=users[3],
                real_name='Daren',
                character_name='Durian',
                past_or_future='Past',
                occupation='Data Scientist',
                descriptor1='deep',
                descriptor2='direct',
                descriptor3='dull',
                solo=True
                ),
            Character(
                username=users[4],
                real_name='Ed',
                character_name='Eggplant',
                past_or_future='Past',
                occupation='Electrician',
                descriptor1='eager',
                descriptor2='efficient',
                descriptor3='emotional',
                solo=True
                ),
            Character(
                username=users[5],
                real_name='Fred',
                character_name='Fig',
                past_or_future='Future',
                occupation='Fire Fighter',
                descriptor1='fabulous',
                descriptor2='funny',
                descriptor3='fussy',
                solo=True
                ),
            Character(
                username=users[6],
                real_name='George',
                character_name='Grape',
                past_or_future='Future',
                occupation='Guide',
                descriptor1='generous',
                descriptor2='gentle',
                descriptor3='gloomy',
                solo=True
                ),
            Character(
                username=users[7],
                real_name='Herald',
                character_name='Honeydew',
                past_or_future='Future',
                occupation='Hair Dresser',
                descriptor1='hateful',
                descriptor2='hearty',
                descriptor3='hesitant',
                solo=True
                ),
            Character(
                username=users[8],
                real_name='Ian',
                character_name='Ice Cream',
                past_or_future='Future',
                occupation='Interior Designer',
                descriptor1='idiotic',
                descriptor2='idle',
                descriptor3='inspiring',
                solo=True
                ),
            Character(
                username=users[9],
                real_name='Josh',
                character_name='Jackfruit',
                past_or_future='Future',
                occupation='Janitor',
                descriptor1='jokeful',
                descriptor2='joyous',
                descriptor3='jovial',
                solo=True
                ),
            ]

    save_all(chars)
