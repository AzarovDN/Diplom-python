import requests
import json
import time
import sys


# id = input('Введите имя пользователя или его id: ')

id = '171691064' #  Шмаргунов

# id = '9897521'  # Азаров

# id = '230412273'

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

class User:

    def __init__(self, user_id):
        self.user_id = user_id


def backspace():
    print('\r', end='')


if id.isdigit():
    id = id
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
    'access_token': token,
    'v': '5.92',
    'user_id': user.user_id
}

friends = requests.get('https://api.vk.com/method/friends.get', params)  # Получил json друзей
my_groups = requests.get('https://api.vk.com/method/groups.get', params)  # Получил json групп

friends_list = friends.json()['response']['items']  # получил список друзей
my_group_list = my_groups.json()['response']['items']  # получил список групп


all_friends_group = []

counter = len(friends_list)

for friend in friends_list:

    counter -= 1

    backspace()
    s = f'Осталось обработать {counter} друзей'  # string for output
    sys.stdout.write(s)
    # time.sleep(0.2)  # sleep for 200ms

    params = {
        'access_token': token,
        'v': '5.92',
        'user_id': friend
    }

    try:
        friend_group = requests.get('https://api.vk.com/method/groups.get', params)
        friend_group_list = friend_group.json()['response']['items']
        all_friends_group.extend(friend_group_list)
    except KeyError:
        continue

print('\n')

results = set(my_group_list) - set(all_friends_group)


out_data = []
counter = len(results)

for group_id in results:

    counter -= 1

    backspace()
    s = f'Осталось обработать {counter} групп'  # string for output
    sys.stdout.write(s)
    # time.sleep(0.2)  # sleep for 200ms

    params = {
        'access_token': token,
        'v': '5.92',
        'group_id': group_id
    }
    try:
        group_info = requests.get('https://api.vk.com/method/groups.getById', params)
        group_members = requests.get('https://api.vk.com/method/groups.getMembers', params)
        group_info_dict = {
            'name': group_info.json()['response'][0]['name'],
            'gid': group_info.json()['response'][0]['id'],
            'members_count': group_members.json()['response']['count']
        }
        out_data.append(group_info_dict)
    except KeyError:
        print(f'Ошибка тут {group_info.json()}')
        continue

with open('groups.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f, ensure_ascii=False)

print('\n')
print('данные записаны в файл')
