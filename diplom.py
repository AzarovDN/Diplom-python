import requests

# token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

# id = input('Введите имя пользователя или его id: ')


# id = '171691064' #  Шмаргунов

id = '9897521'  # Азаров


class User:
    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

    def __init__(self, user_id):
        self.user_id = user_id


if id.isdigit():
    id = id
    print('1')
else:
    print('0')
    pass

user = User(id)

params = {
    'access_token': user.token,
    'v': '5.92',
    'user_id': user.user_id,
    'extended': '0',
    # 'filter': 'gid'
}

friends = requests.get('https://api.vk.com/method/users.getFollowers', params)  # Получил json друзей

my_groups = requests.get('https://api.vk.com/method/groups.get', params)  # Получил json групп

print(my_groups.json())

friends_list = friends.json()['response']['items']  # получил список друзей

my_group_list = my_groups.json()['response']['items'] # получил список групп

print(my_group_list)


