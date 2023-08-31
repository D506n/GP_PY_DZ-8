import re
from os import system, name as name_os

PATH = "my_phones.txt"

def delete_trash_form_str(string = str, pattern = str):
    string = string.split(pattern)
    match len(string):
        case 2:
            return string[0]
        case _:
            return string

def read_file():
    result_dict = {}
    file = open(PATH, 'r', encoding='UTF-8')
    all_data_array = file.readlines()
    for step in range(0, len(all_data_array)):
        current_full_name = re.search(r'([А-Яа-яЁёA-Za-z\s]{1,})', all_data_array[step]).group(0)
        current_number = re.search(r'\d{1,}', all_data_array[step]).group(0)
        result_dict.update({current_number: current_full_name})
    file.close()
    return result_dict

def update_file(phones_dict = dict):
    file = open(PATH, 'w', encoding='UTF-8').close()
    file = open(PATH, 'w', encoding='UTF-8')
    list_of_numbers = list(phones_dict.keys())
    for step in range(0, len(list_of_numbers)):
        temp_fullname = phones_dict.get(list_of_numbers[step])
        file.write(f'{temp_fullname}_{list_of_numbers[step]}\n')
    file.close()

def show_menu():
    menu_points = ['1. Показать все контакты', '2. Добавить контакт', '3. Изменить контакт', '4. Удалить контакт', '5. Поиск контакта']
    print('Главное меню.\n---')
    for step in range(0, len(menu_points)):
        print(menu_points[step])
    print('---')
    chose = input('Выберите пункт меню: ')
    return chose

def show_contacts(phones_dict = dict):
    list_of_numbers = list(phones_dict.keys())
    for step in range(0, len(list_of_numbers)):
        temp_fullname = phones_dict.get(list_of_numbers[step])
        print(f'{step+1}. {list_of_numbers[step]} ФИО: {temp_fullname}')
    print(f'---\nВсего контактов: {len(list_of_numbers)}\n---')

def add_contact(phones_dict = dict):
    new_number = input('Введите номер телефона нового контакта: ')
    new_name = input('Введите ФИО нового контакта: ')
    phones_dict.update({new_number: new_name})
    update_file(phones_dict)
    print('Контакт добавлен.')

def list_matching(find_pattern = str, first_list = list, second_list = list, phones_dict = dict):
    result_list = []
    for step in range(0, len(first_list)):
        find_result = re.search(find_pattern, first_list[step])
        if find_result != None:
            result_list.append(second_list[step])
    if len(result_list) == 0:
        print('Контакты не найдены.')
        return result_list
    print('Найденые контакты: ')
    for step in range(0, len(result_list)):
        print(f'{step+1}. {result_list[step]} ФИО: {phones_dict.get(result_list[step])}')
    return result_list

def find_contact(phones_dict = dict, find_pattern = str):
    all_numbers = list(phones_dict.keys())
    all_names = list(phones_dict.values())
    if find_pattern.isnumeric() == False:
        return list_matching(find_pattern, all_names, all_numbers, phones_dict)
    else:
        return list_matching(find_pattern, all_numbers, all_numbers, phones_dict)

def delete_contact(find_pattern = str, phones_dict = dict):
    delete_number = find_contact(phones_dict, find_pattern)
    if len(delete_number) == 0:
        return None
    elif len(delete_number) != 1:
        to_do = input('Найдено несколько контактов, уточните, пожалуйста, какой вы хотите удалить, оставьте поле пустым, если нужно удалить все найденые контакты: ')
        if to_do == '':               
            print('Вы уверены, что хотите удалить эти контакты?')
            sure = input('Для подтверждения введите "УДАЛИТЬ": ')
            if sure == "УДАЛИТЬ":
                print('Приступаю к удалению контактов.')
                print(len(delete_number))
                for step in range(0, len(delete_number)):
                    print(f'Контакт с номером {delete_number[step]} удалён из телефонной книги.')
                    phones_dict.pop(delete_number[step])
            else:
                print('Контакты не удалены.')
                return None
        elif to_do.isnumeric() == True and int(to_do) <= len(delete_number):
            print(f'Вы уверены, что хотите удалить контакт с номером {delete_number[int(to_do)-1]}?')
            sure = input('Для подтверждения введите "УДАЛИТЬ": ')
            if sure == "УДАЛИТЬ":
                print(f'Контакт с номером {delete_number[int(to_do)-1]} удалён из телефонной книги.')
                phones_dict.pop(delete_number[int(to_do)-1])
            else:
                print('Подтверждение не получено, контакт не удалён.')
        else:
            print('Выбранного пункта нет в списке.')
    elif len(delete_number) == 1:
        print(f'Вы уверены, что хотите удалить контакт с номером {delete_number[0]}?')
        sure = input('Для подтверждения введите "УДАЛИТЬ": ')
        if sure == "УДАЛИТЬ":
            print(f'Контакт с номером {delete_number[0]} удалён из телефонной книги.')
            phones_dict.pop(delete_number[0])
        else:
            print('Подтверждение не получено, контакт не удалён.')
    update_file(phones_dict)

def edit_contact(find_pattern = str, phones_dict = dict):
    edit_number = find_contact(phones_dict, find_pattern)
    if len(edit_number) == 0:
        return None
    elif len(edit_number) != 0:
        if len(edit_number) != 1:
            to_do = input('Найдено несколько контактов, уточните, пожалуйста, порядковый номер контакта, который нужно изменить: ')
        else:
            to_do = '1'
        if to_do != '' and to_do.isnumeric() == True:
            if int(to_do) <= len(edit_number):
                new_number = edit_number[int(to_do)-1]
                new_name = phones_dict.get(new_number)
                need_to_edit_number = input('Введите новый номер телефона для этого контакта, если изменять номер не нужно, оставьте поле пустым: ')
                need_to_edit_name = input('Введите новое имя для этого контакта, если имя изменять не нужно, оставьте поле пустым: ')
                if need_to_edit_number != '' and need_to_edit_number != new_number:
                    print('Новый номер принят.')
                    new_number = need_to_edit_number
                if need_to_edit_name != '' and need_to_edit_name != new_name:
                    print('Новое имя принято.')
                    new_name = need_to_edit_name
                phones_dict.pop(edit_number[int(to_do)-1])
                phones_dict.update({new_number: new_name})
                update_file(phones_dict)
                print('Контакт сохранён.')
            else:
                print('Выбранного пункта нет в списке.')
                return None
        else:
            print('Выбранного пункта нет в списке.')
            return None
    

def cls(name_os):
    if name_os == 'nt':
        system('cls')
    else:
        system('clear')

err_in_menu = True

while True:
    if err_in_menu == False:
        cls(name_os)
    err_in_menu = False
    phones_dict = read_file()
    chose = show_menu()
    match chose:
        case '1':
            cls(name_os)
            print('Список контактов.\n---')
            show_contacts(phones_dict)
            input('Введите любой символ для возврата в главное меню: ')
        case '2':
            cls(name_os)
            print('Добавление контакта.\n---')
            add_contact(phones_dict)
            input('Введите любой символ для возврата в главное меню: ')
        case '3':
            cls(name_os)
            print('Изменение контакта.\n---')
            find_pattern = input('Для внесения изменений, нужно сначала найти контакт. Пожалуйста, укажите номер телефона или ФИО(часть, или полностью) контакта: ')
            edit_contact(find_pattern, phones_dict)
            input('Введите любой символ для возврата в главное меню: ')
        case '4':
            cls(name_os)
            print('Удаление контакта.\n---')
            find_pattern = input('Для удаления, нужно сначала найти контакт. Пожалуйста, укажите номер телефона или ФИО(часть, или полностью) контакта: ')
            delete_contact(find_pattern, phones_dict)
            input('Введите любой символ для возврата в главное меню: ')
        case '5':
            cls(name_os)
            print('Поиск контакта.\n---')
            find_pattern = input('Для поиска введите номер телефона или ФИО(часть, или полностью) контакта: ')
            find_contact(phones_dict, find_pattern)
            input('Введите любой символ для возврата в главное меню: ')
        case _:
            cls(name_os)
            print(f'Такого пункта в меню нет, пожалуйста, введите число от 1 до 5.')
            err_in_menu = True