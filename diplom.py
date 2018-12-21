import requests
import json
import time
import sys


class User:

    def __init__(self, user_id):
        self.user_id = user_id


def backspace():

    print('\r', end='')


def take_params():

    with open('params.json', encoding='utf-8') as f:  # заменить имя файла на params_export, поменять token в файле
        default_params = json.load(f)[0]
        return default_params


def made_id(id, default_params):

    if id.isdigit():
        id = id
    else:
        params = default_params
        params['user_ids'] = id

        try:
            id_json = requests.get('https://api.vk.com/method/users.get', params)
            id = id_json.json()['response'][0]['id']

        except KeyError:
            if id_json.json()['error']['error_code'] == 5:
                print(f"В работе программы возникла ошибка {id_json.json()['error']['error_msg']}")
                print('Программа перезапущенна!!!')
                work_program()
            elif id_json.json()['error']['error_code'] == 113:
                print('Введите корректное имя пользователя')
                print('Программа перезапущена!!!')
                work_program()
            else:
                print('Ошибка', id_json.json()['error']['error_msg'])
                print('Программа перезапущена!!!')
                work_program()

        except NameError:
            if id_json.json()['error']['error_code'] == 5:
                print(f"В работе программы возникла ошибка {id_json.json()['error']['error_msg']}")
                print('Введите корректное имя пользователья. Программа перезапущена')
                work_program()
            else:
                print('Ошибка', id_json.json()['error']['error_msg'])
                print('Программа перезапущена!!!')
                work_program()

    return id


def user_data(default_params, user):

    friends = '"friends": API.friends.get({' + '"user_id":' + f'{user.user_id}' + '})'
    my_groups = '"my_groups": API.groups.get({' + '"user_id":' + f'{user.user_id}' + '})'

    code = 'return {' + f'{friends}, {my_groups}' + '};'

    params = default_params
    params['code'] = code
    try:
        response = requests.get('https://api.vk.com/method/execute?', params)
        friends_list = response.json()['response']['friends']['items']
        my_group_list = response.json()['response']['my_groups']['items']

    except KeyError:
        if response.json()['error']['error_code'] == 5:
            print(f"В работе программы возникла ошибка {response.json()['error']['error_msg']}")
            print('Программа перезапущенна!!!')
            work_program()
        else:
            print('Ошибка', response.json()['error']['error_msg'])
            print('Программа перезапущена!!!')
            work_program()

    return friends_list, my_group_list


def find_secret_group(friends_list, my_group_list,default_params):

    all_friends_group = []
    counter = len(friends_list)

    for friend in friends_list:

        counter -= 1
        backspace()

        s = f'Осталось обработать {counter} друзей'
        sys.stdout.write(s)

        friend_group = '"friend_group": API.groups.get({' + '"user_id":' + f'{friend}' + '})'
        code = 'return {' + f'{friend_group}' + '};'

        params = default_params
        params['code'] = code

        try:
            response = requests.get('https://api.vk.com/method/execute?', params)
            friend_group_list = response.json()['response']['friend_group']['items']
            all_friends_group.extend(friend_group_list)
        except TypeError:
            if response.json()['execute_errors'][0]['error_code'] == 30:
                print('\n', f'Закрытый доступ в профиль {friend}')
            continue
        except KeyError:
            if response.json()['error']['error_code'] == 6:
                time.sleep(0.5)
                response = requests.get('https://api.vk.com/method/execute?', params)
                friend_group_list = response.json()['response']['friend_group']['items']
                all_friends_group.extend(friend_group_list)
                continue
            else:
                print('Ошибка', response.json()['error']['error_msg'])

    print('\n')
    results = set(my_group_list) - set(all_friends_group)

    return results


def find_friend_in_group(n, groups, friend, default_params):

    all_mutural_group_list = []
    counter = len(groups)
    counter_group = 0

    for group in groups:

        counter -= 1
        backspace()
        s = f'Осталось обработать {counter} групп'
        sys.stdout.write(s)
        mutural = '"mutural_list": API.groups.getMembers({' + '"group_id":' + f'{group}' + '})'
        code = 'return {' + f'{mutural},' + '};'

        params = default_params
        params['code'] = code

        try:
            mutural_list = requests.get('https://api.vk.com/method/execute?', params).json()['response']['mutural_list']['items']
            if len(set(friend) & set(mutural_list)) > 0 & len(set(friend) & set(mutural_list)) <= n:
                counter_group += 1
                all_mutural_group_list.append(group)
        except KeyError:
            if mutural_list.json()['error']['error_code'] == 6:
                time.sleep(0.5)
                mutural_list = requests.get('https://api.vk.com/method/execute?', params).json()['response']['mutural_list']['items']
                if len(set(friend) & set(mutural_list)) > 0 & len(set(friend) & set(mutural_list)) <= n:
                    counter_group += 1
                    all_mutural_group_list.append(group)
                continue
        except TypeError:
            if mutural_list.json()['execute_errors'][0]['error_code'] == 30:
                print('\n', f'Закрытый доступ в профиль {friend}')
            continue
        except AttributeError:
            print('AttributeError в find_friend_in_group')
            continue

    print(len(all_mutural_group_list))
    return all_mutural_group_list


def write_file(writes_file, default_params):

    out_data =[]
    counter = len(writes_file)

    for group_id in writes_file:

        counter -= 1


        backspace()
        s = f'Осталось записать {counter} групп'
        sys.stdout.write(s)

        group_info = '"group_info": API.groups.getById({' + '"group_id":' + f'{group_id}' + '})'
        group_members = '"group_members": API.groups.getMembers({' + '"group_id":' + f'{group_id}' + '})'

        code = 'return {' + f'{group_info}, {group_members}' + '};'

        params = default_params
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
            if response.json()['error']['error_code'] == 6:
                time.sleep(0.5)
                response = requests.get('https://api.vk.com/method/execute?', params)
                group_info_dict = {
                    'name': response.json()['response']['group_info'][0]['name'],
                    'gid': response.json()['response']['group_info'][0]['id'],
                    'members_count': response.json()['response']['group_members']['count']
                }
            continue

    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)
    print('\n')
    print('данные записаны в файл')


def search_for_secret_groups(default_params, user):
    friends_list, my_group_list = user_data(default_params, user)
    result = find_secret_group(friends_list, my_group_list, default_params)
    write_file(result, default_params)


def search_for_common_groups(default_params,user):
    n = int(input('N - максимальное количество друзей в группе. Введите N: '))
    friends_list, my_group_list = user_data(default_params,user)
    result = find_friend_in_group(n, my_group_list, friends_list, default_params)
    write_file(result, default_params)


def work_program():
    default_params = take_params()
    id = input('Введите id пользователя или id: ')
    user = User(made_id(id, default_params))
    print('Поиск секретных групп пользователя - 1')
    print('Поиск общих групп с друзьями - 2')
    what_find = input('Выберите режим поиска: ')

    if what_find == '1':
        search_for_secret_groups(default_params, user)
    elif what_find == '2':
        search_for_common_groups(default_params, user)
    else:
        print('Вы ввели некорректные данные')


if __name__ == '__main__':
    work_program()
    # default_params = take_params()
    #
    # id = input('Введите id пользователя или id: ')
    # # id = input('Введите имя пользователя или его id: ')
    # # id = '171691064'  # Шмаргунов
    # # id = '9897521'  # Азаров
    # # id = '230412273'  # В этом id всего 25 друзей
    #
    # user = User(made_id(id))
    #
    # print('Поиск секретных групп пользователя - 1')
    # print('Поиск общих групп с друзьями - 2')
    # what_find = input('Выберите режим поиска: ')
    #
    # if what_find == '1':
    #     search_for_secret_groups()
    # elif what_find == '2':
    #     search_for_common_groups()
    # else:
    #     print('Вы ввели некорректные данные')
    #
    # # user = User(230412273)
    # # search_for_secret_groups()








