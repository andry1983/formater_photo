import os
from shutil import copyfile
from os import listdir
from os.path import isfile, join
import re

SUFIX_NAME = '.jpg'  # розширення файлів для копіювання

FORMATS_PHOTO_ENABLES = [  # Допустимі формати для створення папок для переіменування
    '10x15',
    '10х15',
    '13x18',
    '13х18',
    '15x21',
    '15х21',
    '18x24',
    '18х24',
    '20x28',
    '20х28',
    '25x38',
    '25х38',
    '10x15 мат',
    '10х15 мат',
    '13x18 мат',
    '13х18 мат',
    '15x21 мат',
    '15х21 мат',
    '18x24 мат',
    '18х24 мат',
    '20x28 мат'
    '20х28 мат'
    '25x38 мат'
    '25х38 мат'
]

LIST_FOR_RENAME = 'form.txt'  # назва файла сценарію переіменування
DELIMETR = '$'  # розділювач по якому ми розбиваємо стрічку в масив (формат, імя файлу, к-ть)

COPY_ROOT_PATH_NAME = 'copy_photo'  # назва папку куди ми копіюємо переіменовані файли

FORMATS_PHOTO = ['.jpg', '.JPG', '.jpeg']  # допустимі формати фоток

FOLDERS_FOR_READ = [
    '13х18',
    '20х28',
    '25х38',
    'JPG2'
]

IN_JPG2 = [
    '20х28',
    '25х38',
    'на диск'
]

SMALL_FORMAT_PHOTO = [
    '10х15',
    '13х18',
    '15х21',
    '10х15 мат',
    '13х18 мат',
    '15х21 мат'
]

BIG_FORMAT_PHOTO = [
    '18х24',
    '20х28',
    '18х24 мат',
    '20х28 мат'
]

BIGEST_FORMAT_PHOTO = [
    '25x38',
    '25х38',
    '25x38 мат',
    '25х38 мат'
]

file_path = os.path.dirname(os.path.abspath(__file__))

error_str = ''


def indicator_format(format) -> str:
    format = format.strip('\t\n\r\s')
    indicator = ''
    if format in SMALL_FORMAT_PHOTO:
        indicator = 'small'
    if format in BIG_FORMAT_PHOTO:
        indicator = 'big'
    if format in BIGEST_FORMAT_PHOTO:
        indicator = 'bigest'
    return indicator


def create_copy_dir(name=None):
    try:
        dir_copy_names = COPY_ROOT_PATH_NAME if name is None else str(name)
        full_path = os.path.join(file_path, dir_copy_names)
        if name:
            if name.lower() not in FORMATS_PHOTO_ENABLES:
                raise Exception(f'Недопустиме імя формату: {name}')
            else:
                full_path = os.path.join(file_path, COPY_ROOT_PATH_NAME, dir_copy_names)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return True
    except Exception as e:
        write_error(f'An error occurred while trying to create a folder: {dir_copy_names} ')
        return False


def read_dir_files():
    list_files = listdir(file_path)
    list_file_sorts_for_types = []
    for files in list_files:
        _, file_extension = os.path.splitext(files)
        if isfile(join(file_path, files)) and file_extension in FORMATS_PHOTO:
            list_file_sorts_for_types.append(files)
        else:
            continue
    return list_file_sorts_for_types


def file_list_for_rename():
    file_list = os.path.join(file_path, LIST_FOR_RENAME)
    renames_lists = []
    if os.path.exists(file_list):
        with open(file_list, "r", encoding='utf-16') as file:
            for line in file:
                clear_data = line.strip('\t\n\r\s').split(DELIMETR)
                if len(clear_data) > 1:
                    renames_lists.append(clear_data)
        return renames_lists
    else:
        raise Exception(
            f'Увага файл з іменами для сортування ({LIST_FOR_RENAME}) відсутній в даному каталозі. \n Подальше виконання переіменування не можливе')


def copy_file(old_name, new_name, new_path):
    copy_root_path = os.path.join(file_path, COPY_ROOT_PATH_NAME)
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
            write_error(f'Виникла помилка при копіюванні файлу ({old_name}). \n{e}')

    else:
        write_error(f'Увага файл з імям {old_name} не існує в даному каталозі')
        return False


def sufix_counter(all_counter) -> str:
    if all_counter < 10:
        sufix = f'00{all_counter}'
    elif 9 < all_counter < 100:
        sufix = f'0{all_counter}'
    else:
        sufix = f'{all_counter}'
    return sufix


all_counter = 0
smal_counter = 0


def copy_search_file(filename, old_file_name, new_path_copy, counts):
    global all_counter, smal_counter
    old_file_exist_copy = os.path.join(file_path, old_file_name)
    if os.path.exists(old_file_exist_copy):
        sufix = sufix_counter(all_counter)
        if counts == 1:
            all_counter += 1
            new_full_file_name = f'{sufix}__{filename}{SUFIX_NAME}'
            copy_file(old_name=old_file_name, new_name=new_full_file_name, new_path=new_path_copy)
        elif counts > 1:
            sufix = sufix_counter(all_counter)
            all_counter += 1
            smal_counter -= 1
            for i in range(1, counts + 1):
                smal_counter += 1
                new_full_file_name = f'{sufix}__{filename}_{i}{SUFIX_NAME}'
                if new_full_file_name:
                    copy_file(old_name=old_file_name, new_name=new_full_file_name, new_path=new_path_copy)
        else:
            write_error(f'Увага к-ть не може  дорівнювати 0 (файл :{filename})')


def search_smal_photo(number_photo: str):
    if number_photo:
        first_file_path = os.path.join(file_path, '13х18'.lower())
        second_file_path = os.path.join(file_path, '20х28'.lower())
        third_file_path = os.path.join(file_path, '25х38'.lower())
        if os.path.exists(first_file_path) and os.path.exists(os.path.join(first_file_path, number_photo)):
            return os.path.join(first_file_path, number_photo)
        elif os.path.exists(second_file_path) and os.path.exists(os.path.join(second_file_path, number_photo)):
            return os.path.join(second_file_path, number_photo)
        elif os.path.exists(third_file_path) and os.path.exists(os.path.join(third_file_path, number_photo)):
            return os.path.join(third_file_path, number_photo)
        else:
            return False


def search_big_photo(number_photo: str):
    file_path_serch = os.path.join(file_path, '20х28'.lower())
    if os.path.exists(file_path_serch) and os.path.exists(os.path.join(file_path_serch, number_photo)):
        return os.path.join(file_path_serch, number_photo)
    return False


def search_bigest_photo(number_photo: str):
    file_path_serch = os.path.join(file_path, '25х38'.lower())
    if os.path.exists(file_path_serch) and os.path.exists(os.path.join(file_path_serch, number_photo)):
        return os.path.join(file_path_serch, number_photo)
    return False


def write_error(msg) -> str:
    global error_str
    if msg:
        error_str = f'{error_str}\n-\t{msg}\n'


def start():
    global all_counter
    try:
        data_clear = file_list_for_rename()
        if len(data_clear) > 0:
            for data in data_clear:
                format, filename, counts = data
                filename = re.sub(r'[^\d]', '', filename)
                counts = int(counts)
                indicator_search = indicator_format(format)
                full_file_old_name = f'{filename}{SUFIX_NAME}'.lower()
                new_path_copy = os.path.join(file_path, COPY_ROOT_PATH_NAME, format)
                file_search = ''
                if indicator_search == 'small':
                    file_search = search_smal_photo(full_file_old_name)
                    if not file_search:
                        write_error(f'Увага файл не знайдено: {full_file_old_name}, format: {format}, к-ть={counts}')
                elif indicator_search == 'big':
                    file_search = search_big_photo(full_file_old_name)
                elif indicator_search == 'bigest':
                    file_search = search_bigest_photo(full_file_old_name)
                if file_search:
                    copy_search_file(
                        filename=filename,
                        old_file_name=file_search,
                        new_path_copy=new_path_copy,
                        counts=counts
                    )
                else:
                    write_error(f'Увага файл не знайдено: {full_file_old_name}, format: {format}, к-ть={counts}')
        else:
            raise Exception(
                f'Файл для сортування ({LIST_FOR_RENAME}) напевно, що не містить данних для переіменування первірте його і запустіть програму знову')
    except Exception as e:
        write_error(e)
    else:
        if error_str:
            print(f'Увага під час роботи програми виникли наступні помилки: \n\n {error_str}')
        print(
            f'\n\n Операція в каталозі {file_path} виконана. \n К-ть скопійованих файлів {all_counter + smal_counter}')


if __name__ == "__main__":
    start()
