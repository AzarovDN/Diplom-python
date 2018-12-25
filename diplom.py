import requests
import json
import time
import sys
import logging


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
            time.sleep(0.33)
            id = id_json.json()['response'][0]['id']

        except KeyError:
            if id_json.json()['error']['error_code'] == 5:
                logging.error(f"Ошибка в запросе {id_json.json()['error']['error_msg']}")
                print('Программа перезапущенна из-за ошибки!!!')
                work_program()

            elif id_json.json()['error']['error_code'] == 113:
                logging.error(f"{id_json.json()['error']['error_msg']}")
                print('Имя пользователя введено некорректно')
                print('Программа перезапущена!!!')
                work_program()

            else:
                logging.error(f"Ошибка в запросе {id_json.json()['error']['error_msg']}")
                print('Программа перезапущена из-за ошибки')
                work_program()

    return id


def get_friends_list(default_params, user):

    friends_list = []

    code = '''
    var friends_list = [];
    var count;
    var offset = 0;
    var friends = API.friends.get({"user_id": ''' + str(user.user_id) + '''});
    friends_list = friends.items;
    count = friends.count;
    return {"count": count, "friends_list": friends_list}; 
    '''

    params = default_params
    params['code'] = code

    try:
        response = requests.get('https://api.vk.com/method/execute?', params)
        time.sleep(0.33)
        friends_list.extend(response.json()['response']['friends_list'])
        count = response.json()['response']['count']
        if count is None:
            count = 0

        if count > 5000:
            counter_iterations = count // 125000
            print('\n')

            for offset in range(5000, count, 125000):
                counter_iterations -= 1
                code = '''
                    var friends_list = [];
                    var offset = ''' + str(offset) + ''';
                    var i = ''' + str(offset + 125000) + ''';
                    while (offset <= i){
                        var friends = API.friends.get({"user_id": ''' + str(user.user_id) + ''', "offset": offset});
                        friends_list = friends_list + friends.items;
                            offset = offset + 5000;
                        };
                    return {"friends_list": friends_list}; 
                    '''
                params['code'] = code

                try:
                    response = requests.get('https://api.vk.com/method/execute?', params)
                    time.sleep(0.33)
                    print(f'Осталось итераций {counter_iterations}')
                    friends_list.extend(response.json()['response']['friends_list'])

                except KeyError:
                    if response['error']['error_code'] == 6:
                        logging.error(f'Превышение запросов API')
                        time.sleep(0.5)
                        response = requests.get('https://api.vk.com/method/execute?', params)
                        time.sleep(0.33)
                        friends_list.extend(response.json()['response']['friends_list'])
                        continue

    except KeyError:

        if response.json()['error']['error_code'] == 5:
            logging.error(f"Ошибка в запросе {response.json()['error']['error_msg']}")
            print('Программа перезапущенна из-за ошибки!!!')
            work_program()

        else:
            logging.error(f"Ошибка в запросе {response.json()}")
            print('Программа перезапущена из-за ошибки')
            work_program()
    except TypeError:
        if response.json()['execute_errors'][0]['error_code'] == 30:
            logging.error(f"Ошибка в запросе {response.json()['execute_errors'][0]['error_msg']}")
            print('Программа перезапущена из-за ошибки')
            work_program()
        else:
            logging.error(f"Ошибка в запросе {response.json()}")
            print('Программа перезапущена из-за ошибки')
            work_program()

    return friends_list


def get_my_group_list(default_params, user):
    my_group_list = []
    code = '''
        var my_group_list = [];
        var count;
        var my_groups = API.groups.get({"user_id":''' + str(user.user_id) + '''});
        my_group_list = my_groups.items;
        count = my_groups.count;
        return {"count": count, "my_group_list": my_group_list};  
        '''

    params = default_params
    params['code'] = code

    try:
        response = requests.get('https://api.vk.com/method/execute?', params)
        my_group_list.extend(response.json()['response']['my_group_list'])
        count = response.json()['response']['count']
        time.sleep(0.33)
        if count is None:
            count = 0

        if count > 5000:
            counter_iterations = count // 25000
            print('\n')

            for offset in range(5000, count, 25000):
                counter_iterations -= 1
                code = '''
                        var my_group_list = [];
                        var offset = ''' + str(offset) + ''';
                        var i = ''' + str(offset + 25000) + ''';
                        while (offset <= i){
                            var my_groups = API.groups.get({"user_id":''' + str(user.user_id) + ''', "offset": offset});
                            my_group_list = my_group_list + my_groups.items;
                                offset = offset + 1000;   
                            };
                        return {"my_group_list": my_group_list}; 
                        '''
                params['code'] = code

                try:
                    response = requests.get('https://api.vk.com/method/execute?', params)
                    my_group_list.extend(response.json()['response']['my_group_list'])
                    print(f'Осталось итераций {counter_iterations}')
                    time.sleep(0.33)

                except KeyError:
                    if response['error']['error_code'] == 6:
                        logging.error(f'Превышение запросов API')
                        time.sleep(0.5)
                        response = requests.get('https://api.vk.com/method/execute?', params)
                        my_group_list.extend(response.json()['response']['my_group_list'])
                        time.sleep(0.33)
                        continue

    except KeyError:
        if response.json()['error']['error_code'] == 5:
            logging.error(f"Ошибка в запросе {response.json()['error']['error_msg']}")
            print('Программа перезапущенна из-за ошибки!!!')
            work_program()

        else:
            logging.error(f"Ошибка в запросе {response.json()['error']['error_msg']}")
            print('Программа перезапущена из-за ошибки')
            work_program()

    return my_group_list


def find_friend_in_group(n, my_group_list, friends_list, default_params):

    all_group_list = []
    counter = len(my_group_list)
    counter_group = 0

    for group in my_group_list:
        members_list = []
        counter -= 1
        backspace()
        s = f'Осталось обработать {counter} групп.'
        sys.stdout.write(s)

        code = ''' 
                var members_list = [];
                var count;
                var resp = API.groups.getMembers({"group_id":''' + str(group) + '''});
                members_list = members_list + resp.items;
                count = resp.count;
                return {"count": count, "members_list": members_list}; 
                '''

        params = default_params
        params['code'] = code

        try:
            response = requests.get('https://api.vk.com/method/execute?', params).json()
            print(response)
            time.sleep(0.33)

            count = response['response']['count']
            if count is None:
                count = 0

            members_list.extend(response['response']['members_list'])

            if count > 1000:
                counter_iterations = (count // 25000) + 1

                for offset in range(1000, count, 25000):
                    backspace()
                    s = f'Осталось обработать {counter} групп. Осталось итераций в группе {counter_iterations}'
                    sys.stdout.write(s)
                    counter_iterations -= 1
                    code = '''
                            var members_list = [];
                            var offset = ''' + str(offset) + ''';
                            var i = ''' + str(offset + 25000) + ''';
                            while (offset < i) {
                                var resp = API.groups.getMembers({"group_id":''' + str(group) + ''', "offset": offset});
                                members_list = members_list + resp.items;
                                offset = offset + 1000;
                            };
                            return {"members_list": members_list}; 
                            '''
                    params['code'] = code
                    response = requests.get('https://api.vk.com/method/execute?', params).json()
                    time.sleep(0.33)
                    members_list.extend(response['response']['members_list'])

            if (len(set(friends_list) & set(members_list)) > 0) & (len(set(friends_list) & set(members_list)) <= n):
                counter_group += 1
                all_group_list.append(group)

            elif (n == 0) & ((len(set(friends_list) & set(members_list))) == 0):
                all_group_list.append(group)

        except KeyError:
            if response['error']['error_code'] == 6:
                logging.error(f'Превышение запросов API')
                time.sleep(0.5)
                response = requests.get('https://api.vk.com/method/execute?', params).json()
                time.sleep(0.33)
                members_list.extend(response['response']['members_list'])

                if (len(set(friends_list) & set(members_list)) > 0) & (len(set(friends_list) & set(members_list)) <= n):
                    counter_group += 1
                    all_group_list.append(group)

                elif (n == 0) & ((len(set(friends_list) & set(members_list))) == 0):
                    all_group_list.append(group)
                continue

            else:
                logging.error(f"Ошибка в запросе {response['error']['error_msg']}")
                continue

        except TypeError:
            if response['response']['execute_errors'][0]['error_code'] == 30:
                logging.error(f'Закрытый доступ в профиль {friends_list}')
            continue

    return all_group_list


def write_file(writes_file, default_params):

    out_data = []
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
            time.sleep(0.33)
            group_info_dict = {
                'name': response.json()['response']['group_info'][0]['name'],
                'gid': response.json()['response']['group_info'][0]['id'],
                'members_count': response.json()['response']['group_members']['count']
            }
            out_data.append(group_info_dict)

        except KeyError:
            if response.json()['error']['error_code'] == 6:
                logging.error(f'Превышение запросов API')
                time.sleep(0.5)
                response = requests.get('https://api.vk.com/method/execute?', params)
                time.sleep(0.33)
                group_info_dict = {
                    'name': response.json()['response']['group_info'][0]['name'],
                    'gid': response.json()['response']['group_info'][0]['id'],
                    'members_count': response.json()['response']['group_members']['count']
                }
                out_data.append(group_info_dict)
                continue

            else:
                logging.error(f"Ошибка в запросе {response.json()['error']['error_msg']}")
                continue

    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)
    print('\n')
    print('Данные записаны в файл.')


def search_for_secret_groups(default_params, user):
    friends_list = get_friends_list(default_params, user)
    my_group_list = get_my_group_list(default_params, user)
    result = find_friend_in_group(0, my_group_list, friends_list, default_params)
    write_file(result, default_params)


def search_for_common_groups(default_params, user):
    n = int(input('N - максимальное количество друзей в группе. Введите N: '))
    friends_list = get_friends_list(default_params, user)
    my_group_list = get_my_group_list(default_params, user)
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

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filename=u'mylog.log')
    work_program()

    # # id = '171691064'  # Шмаргунов
    # # id = '9897521'  # Азаров
    # # id = '230412273'  # В этом id всего 25 друзей