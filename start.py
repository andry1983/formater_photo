import os
from shutil import copyfile

from os import listdir
from os.path import isfile, join

sufix_name = '.jpg'  # розширення файлів для копіювання

FORMATS_PHOTO = [  # Допустимі формати для створення папок для переіменування
    '10х15',
    '13х18',
    '15х21',
    '18х24',
    '20х28',
    '10х15 Мат',
    '13х18 Мат',
    '15х21 Мат',
    '18х24 Мат',
    '20х28 Мат'
]

list_for_rename = 'form.txt'  # назва файла сценарію переіменування
delimiter = '$'  # розділювач по якому ми розбиваємо стрічку в масив (формат, імя файлу, к-ть)

copy_root_path_name = 'copy_photo'  # назва папку куди ми копіюємо переіменовані файли

formats_photo = ['.jpg', '.JPG', '.jpeg']  # допустимі формати фоток

file_path = os.path.dirname(os.path.abspath(__file__))


def create_copy_dir(name=None):
    try:
        dir_copy_names = copy_root_path_name if name is None else str(name)
        full_path = os.path.join(file_path, dir_copy_names)
        if name:
            if name not in FORMATS_PHOTO:
                raise Exception(f'Недопустиме імя формату: {name}')
            else:
                full_path = os.path.join(file_path, copy_root_path_name, dir_copy_names)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return True
    except Exception as e:
        print(f'An error occurred while trying to create a folder: {dir_copy_names} ')
        return False


def read_dir_files():
    list_files = listdir(file_path)
    list_file_sorts_for_types = []
    for files in list_files:
        _, file_extension = os.path.splitext(files)
        if isfile(join(file_path, files)) and file_extension in formats_photo:
            list_file_sorts_for_types.append(files)
        else:
            continue
    return list_file_sorts_for_types


def file_list_for_rename():
    file_list = os.path.join(file_path, list_for_rename)
    renames_lists = []
    if os.path.exists(file_list):
        with open(file_list, "r", encoding='utf-16') as file:
            for line in file:
                clear_data = line.strip(' \t\n\r\s').split(delimiter)
                if len(clear_data) > 1:
                    renames_lists.append(clear_data)
        return renames_lists
    else:
        raise Exception(
            f'Увага файл з іменами для сортування ({list_for_rename}) відсутній в даному каталозі. \n Подальше виконання переіменування не можливе')


def copy_file(old_name, new_name, new_path):
    # print(old_name, new_name, new_path)
    copy_root_path = os.path.join(file_path, copy_root_path_name)
    if not os.path.exists(copy_root_path):
        create_copy_dir()
    old_file_name = os.path.join(file_path, old_name)
    new_file_name = os.path.join(new_path, new_name)

    if os.path.exists(old_file_name) and not os.path.isdir(old_file_name):
        dir_new_path = os.path.basename(new_path)
        if not os.path.exists(new_path):
            create_copy_dir(name=dir_new_path)
        try:
            if os.path.exists(old_file_name):
                copyfile(old_file_name, new_file_name)
            return os.path.exists(new_file_name)
        except Exception as e:
            print(f'Виникла помилка при копіюванні файлу ({old_name}). \n{e}')

    else:
        # print(f'Увага файл з імям {old_name} не існує в даному каталозі')
        return False


def sufix_counter(all_counter)->str:
    if all_counter < 10:
        sufix = f'00{all_counter}'
    elif 9 < all_counter < 100:
        sufix = f'0{all_counter}'
    else:
        sufix = f'{all_counter}'
    return sufix

def start():
    try:
        data_clear = file_list_for_rename()
        if len(data_clear) > 0:
            all_counter = 0
            smal_counter = 0
            file_list=''
            for data in data_clear:
                format, filename, counts = data
                full_file_old_name = f'{filename}{sufix_name}'
                counts = int(counts)
                new_path_copy = os.path.join(file_path, copy_root_path_name, format)
                old_file_exist_copy = os.path.join(file_path, full_file_old_name)
                if os.path.exists(old_file_exist_copy):
                    sufix=sufix_counter(all_counter)
                    if counts == 1:
                        new_full_file_name = f'{sufix}__{filename}{sufix_name}'
                        all_counter += 1
                        if new_full_file_name:
                            file_list += f'\t{new_path_copy}\{new_full_file_name}\n'
                            copy_file(old_name=full_file_old_name, new_name=new_full_file_name, new_path=new_path_copy)
                    elif counts > 1:
                        sufix = sufix_counter(all_counter)
                        all_counter += 1
                        smal_counter -= 1
                        for i in range(1, counts + 1):
                            smal_counter += 1
                            new_full_file_name = f'{sufix}__{filename}_{i}{sufix_name}'
                            if new_full_file_name:
                                file_list +=f'\t{new_path_copy}\{new_full_file_name}\n'
                                copy_file(old_name=full_file_old_name, new_name=new_full_file_name,
                                          new_path=new_path_copy)
                    else:
                        print(f'Увага к-ть не може  дорівнювати 0 (файл :{filename})')
                        continue
                else:
                    print(f'\t\t\tУВАГА Файл не знайдено {old_file_exist_copy} format {format}\n')
                    continue
            print(
                f'Переіменування в каталозі({file_path}) пройшло успішно.'
                f'\nСписок скопійованих файлів:'
                f'\n{file_list}'
                f'\nК-ть скопійованих файлів ({all_counter + smal_counter})')
        else:
            raise Exception(
                f'Файл для сортування ({list_for_rename}) напевно, що не містить данних для переіменування первірте його і запустіть програму знову')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start()
