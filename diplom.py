import requests


# id = input('Введите имя пользователя или его id: ')

# id = '171691064' #  Шмаргунов

# id = '171691064'  # Азаров

id = 'another_nastyaf'

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

class User:

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
    'access_token': token,
    'v': '5.92',
    'user_id': user.user_id
}

friends = requests.get('https://api.vk.com/method/friends.get', params)  # Получил json друзей
my_groups = requests.get('https://api.vk.com/method/groups.get', params)  # Получил json групп

friends_list = friends.json()['response']['items']  # получил список друзей
my_group_list = my_groups.json()['response']['items']  # получил список групп

print('Не забудь удалить! Мои группы: ', my_group_list, '\n')

all_friends_group = []

n = 0

for friend in friends_list:
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


print(len(all_friends_group))

all_friends_group_set = set(all_friends_group)

print(len(all_friends_group_set))


results = set(my_group_list) - all_friends_group_set

out_data = []
for group_id in results:
    params = {
        'access_token': token,
        'v': '5.92',
        'group_id': group_id
    }
    group_info = requests.get('https://api.vk.com/method/groups.getById', params)
    # print(group_info.json())
    group_mem = requests.get('https://api.vk.com/method/groups.getMembers', params)
    # print(group_mem.json()['response']['count'])
    group_info_dict = {
        'name': group_info.json()['response'][0]['name'],
        'gid': group_info.json()['response'][0]['id'],
        'members_count': group_mem.json()['response']['count']
    }
    out_data.append(group_info_dict)


