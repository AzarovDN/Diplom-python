import requests
import json
import time
import sys
from user_class import User


def backspace():
    print('\r', end='')


def default_params():

    default_params = {
        'access_token': token,
        'v': '5.92',
    }
    return default_params


def made_id(id):

    if id.isdigit():
        id = id
    else:

        params = default_params()
        params['user_ids'] = id
        id_json = requests.get('https://api.vk.com/method/users.get', params)
        id = id_json.json()['response'][0]['id']
    return id


def user_data():

    friends = '"friends": API.friends.get({' + '"user_id":' + f'{user.user_id}' + '})'
    my_groups = '"my_groups": API.groups.get({' + '"user_id":' + f'{user.user_id}' + '})'

    code = 'return {' + f'{friends}, {my_groups}' + '};'

    params = default_params()
    params['code'] = code


    response = requests.get('https://api.vk.com/method/execute?', params)

    friends_list = response.json()['response']['friends']['items']
    my_group_list = response.json()['response']['my_groups']['items']

    return friends_list, my_group_list


def find_secret_group(friends_list, my_group_list):

    all_friends_group = []
    counter = len(friends_list)

    for friend in friends_list:

        counter -= 1

        backspace()

        s = f'Осталось обработать {counter} друзей'
        sys.stdout.write(s)
        # time.sleep(0.1)

        friend_group = '"friend_group": API.groups.get({' + '"user_id":' + f'{friend}' + '})'
        code = 'return {' + f'{friend_group}' + '};'

        params = default_params()
        params['code'] = code

        try:
            response = requests.get('https://api.vk.com/method/execute?', params)
            friend_group_list = response.json()['response']['friend_group']['items']
            all_friends_group.extend(friend_group_list)
        except TypeError:
            print('TypeError в find_secret_group')
            continue
        except KeyError:
            print('KeyError в find_secret_group')
            continue

    print('\n')

    results = set(my_group_list) - set(all_friends_group)

    return results


def find_friend_in_group(n, groups, friend):

    all_mutural_group_list = []
    counter = len(groups)
    counter_group = 0

    for group in groups:

        counter -= 1
        backspace()
        s = f'Осталось обработать {counter} групп'
        sys.stdout.write(s)
        # time.sleep(0.1)
        mutural = '"mutural_list": API.groups.getMembers({' + '"group_id":' + f'{group}' + '})'
        code = 'return {' + f'{mutural},' + '};'

        params = default_params()
        params['code'] = code

        try:
            mutural_list = requests.get('https://api.vk.com/method/execute?', params).json()['response']['mutural_list']['items']
            if len(set(friend) & set(mutural_list)) > 0 & len(set(friend) & set(mutural_list)) <= n:
                counter_group += 1
                all_mutural_group_list.append(group)
        except KeyError:
            print('KeyError в find_friend_in_group')
            continue
        except TypeError:
            print('TypeError в find_friend_in_group')
            continue
        except AttributeError:
            print('AttributeError в find_friend_in_group')
            continue

    print(len(all_mutural_group_list))
    return all_mutural_group_list



def write_file(writes_file):

    out_data =[]
    counter = len(writes_file)

    for group_id in writes_file:

        counter -= 1

        backspace()
        s = f'Осталось записать {counter} групп'
        sys.stdout.write(s)
        # time.sleep(0.1)

        group_info = '"group_info": API.groups.getById({' + '"group_id":' + f'{group_id}' + '})'
        group_members = '"group_members": API.groups.getMembers({' + '"group_id":' + f'{group_id}' + '})'

        code = 'return {' + f'{group_info}, {group_members}' + '};'

        params = default_params()
        params['code'] = code
        
        try:
            response = requests.get('https://api.vk.com/method/execute?', params)
            group_info_dict = {
                'name': response.json()['response']['group_info'][0]['name'],
                'gid': response.json()['response']['group_info'][0]['id'],
                'members_count': response.json()['response']['group_members']['count']
            }
            out_data.append(group_info_dict)
        except KeyError:
            print(f'Ошибка тут {response.json()} в write_file')
            continue

    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)
    print('\n')
    print('данные записаны в файл')


if __name__ == '__main__':

    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

    id = input('Введите id пользователя или id: ')
    # id = input('Введите имя пользователя или его id: ')
    # id = '171691064'  # Шмаргунов
    # id = '9897521'  # Азаров
    # id = '230412273'  # В этом id всего 25 друзей

    user = User(made_id(id))

    print('Поиск секретных групп пользователя - 1')
    print('Поиск общих групп с друзьями - 2')
    what_find = input('Выберите режим поиска: ')

    if what_find == '1':
        friends_list, my_group_list = user_data()
        result = find_secret_group(friends_list, my_group_list)
        write_file(result)
    elif what_find == '2':
        n = int(input('N - максимальное количество друзей в группе. Введите N: '))
        friends_list, my_group_list = user_data()
        result = find_friend_in_group(n, my_group_list, friends_list)
        write_file(result)
    else:
        print('Вы ввели некорректные данные')

    # user = User(230412273)
    # friends_list, my_group_list = user_data()
    # result = find_friend_in_group(10, my_group_list, friends_list)
    # write_file(result)







