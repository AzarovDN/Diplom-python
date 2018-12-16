import requests
import json
import time
import sys


class User:

    def __init__(self, user_id):
        self.user_id = user_id


def backspace():
    print('\r', end='')


def made_id(id):

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
    return id


def user_data():

    friends = '"friends": API.friends.get({' + '"user_id":' + f'{user.user_id}' + '})'
    my_groups = '"my_groups": API.groups.get({' + '"user_id":' + f'{user.user_id}' + '})'

    code = 'return {' + f'{friends}, {my_groups}' + '};'
    params = {
        'access_token': token,
        'v': '5.92',
        'code': code
    }

    response = requests.get('https://api.vk.com/method/execute?', params)

    friends_list = response.json()['response']['friends']['items']
    my_group_list = response.json()['response']['my_groups']['items']

    return friends_list, my_group_list


def find_secret_group(x, y):
    friends_list = x
    my_group_list = y

    all_friends_group = []
    counter = len(friends_list)

    for friend in friends_list:

        counter -= 1

        backspace()

        s = f'Осталось обработать {counter} друзей'
        sys.stdout.write(s)
        time.sleep(0.1)

        friend_group = '"friend_group": API.groups.get({' + '"user_id":' + f'{friend}' + '})'
        code = 'return {' + f'{friend_group}' + '};'
        params = {
            'access_token': token,
            'v': '5.92',
            'code': code
        }
        try:
            response = requests.get('https://api.vk.com/method/execute?', params)
            friend_group_list = response.json()['response']['friend_group']['items']
            all_friends_group.extend(friend_group_list)
        except KeyError:
            continue
        except TypeError:
            continue
    print('\n')

    results = set(my_group_list) - set(all_friends_group)

    return results

# Осталось прикрутить к последней функуции

def write_file(results):

    out_data =[]
    counter = len(results)

    for group_id in results:

        counter -= 1

        backspace()
        s = f'Осталось обработать {counter} групп'
        sys.stdout.write(s)
        time.sleep(0.1)

        group_info = '"group_info": API.groups.getById({' + '"group_id":' + f'{group_id}' + '})'
        group_members = '"group_members": API.groups.getMembers({' + '"group_id":' + f'{group_id}' + '})'

        code = 'return {' + f'{group_info}, {group_members}' + '};'

        params = {
            'access_token': token,
            'v': '5.92',
            'code': code
        }
        try:
            response = requests.get('https://api.vk.com/method/execute?', params)
            group_info_dict = {
                'name': response.json()['response']['group_info'][0]['name'],
                'gid': response.json()['response']['group_info'][0]['id'],
                'members_count': response.json()['response']['group_members']['count']
            }
            out_data.append(group_info_dict)
        except KeyError:
            print(f'Ошибка тут {response.json()}')
            continue

    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)
    print('\n')
    print('данные записаны в файл')


if __name__ == '__main__':

    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    # id = input('Введите имя пользователя или его id: ')
    # id = '171691064'  # Шмаргунов
    # id = '9897521'  # Азаров
    id = '230412273'

    user = User(made_id(id))
    friends_list, my_group_list = user_data()
    result = find_secret_group(friends_list, my_group_list)
    write_file(result)





