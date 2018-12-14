import requests

# token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

# id = input('Введите имя пользователя или его id: ')


# id = '171691064' #  Шмаргунов

# id = '171691064'  # Азаров

id = 'another_nastyaf'

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

class User:
    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

    def __init__(self, user_id):
        self.user_id = user_id


if id.isdigit():
    id = id
    print('1')
else:
    params = {
        'access_token': token,
        'v': '5.92',
        'user_ids': id
    }
    id_json = requests.get('https://api.vk.com/method/users.get', params)
    id = id_json.json()['response'][0]['id']

user = User(id)

params = {
    'access_token': user.token,
    'v': '5.92',
    'user_id': user.user_id
}

friends = requests.get('https://api.vk.com/method/friends.get', params)  # Получил json друзей
params = {
    'access_token': user.token,
    'v': '5.92',
    'user_id': user.user_id,
    'count': '1000'
}

my_groups = requests.get('https://api.vk.com/method/groups.get', params)  # Получил json групп

# print(friends.json())

friends_list = friends.json()['response']['items']  # получил список друзей
# print(f'Cписок моих друзей {friends_list}')
# print(len(friends_list))

my_group_list = my_groups.json()['response']['items']  # получил список групп

print('Мои группы: ', my_group_list, '\n')

all_friends_group = []

try:
    for friend in friends_list:

        params = {
            'access_token': user.token,
            'v': '5.92',
            'user_id': friend
        }

        friend_group = requests.get('https://api.vk.com/method/groups.get', params)
        friend_group_list = friend_group.json()['response']['items']

        all_friends_group.extend(friend_group_list)
except KeyError:
        # print('Ошибка в группе', friend_group.json())
        pass
print(len(all_friends_group))

all_friends_group_set = set(all_friends_group)

print(len(all_friends_group_set))


result = set(my_group_list) - all_friends_group_set


print(f'Результат: {result}')

print(len(result))
