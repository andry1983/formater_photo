import os
from shutil import copyfile
from os.path import join
import re

COPY_ROOT_PATH_NAME = 'copy_photo_whitout_2x3_and_3x4'

file_path = os.path.dirname(os.path.abspath(__file__))

LIST_FOR_RENAME = 'form.txt'  # назва файла сценарію переіменування

DELIMETR = '$'  # розділювач по якому ми розбиваємо стрічку в масив (формат, імя файлу, к-ть)

error_str = ''

TWO_ON_THREE = ['10x15', '30x20', '25x38', '10x15 мат', '30x20 мат', '25x38 мат']

THREE_ON_FORE = ['13x18', '15x21', '18x24', '20x28', '13x18 мат', '15x21 мат', '18x24 мат', '20x28 мат']

ENABLES_FOLDERS_NAMES_FOR_PHOTO = ['2x3', '3x4']


def create_copy_dir(name=None):
    """
    створює каталоги для копіюваня фото
    """
    try:
        dir_copy_names = COPY_ROOT_PATH_NAME if name is None else str(name)
        full_path = join(file_path, dir_copy_names)
        if name:
            if dir_copy_names.lower() not in ENABLES_FOLDERS_NAMES_FOR_PHOTO:
                raise Exception(
                    f'Недопустиме імя формату: {dir_copy_names} превірте список допустимих форматів {ENABLES_FOLDERS_NAMES_FOR_PHOTO}')
            else:
                full_path = join(file_path, COPY_ROOT_PATH_NAME, dir_copy_names)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return True
    except Exception as e:
        write_error(f'An error occurred while trying to create a folder: {dir_copy_names} \n {e}')
        return False


def write_error(msg):
    """
    формує список помилок
    """
    global error_str
    if msg:
        error_str = f'{error_str}\n-\t{msg}\n'


def change_ua_x_on_en_x(name_format, lang='ua'):
    """
    міняє англ на укр "х" і навпаки згідно параметра lang(if ua міняєм на англ х)
    """
    return re.sub(r'[хХ]', 'x', name_format) if lang == 'ua' else re.sub(r'[xX]', 'х', name_format)


def file_list_for_rename():
    """
    формує список для копієвання файлів зчитуючи данні з файлу from.txt
    """
    file_list = join(file_path, LIST_FOR_RENAME)
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


def start():
    all_counter = 0
    counter_no_search_file = 0
    try:
        data_clear = file_list_for_rename()
        copy_root_path = join(file_path, COPY_ROOT_PATH_NAME)
        if not os.path.exists(copy_root_path):
            create_copy_dir()
        full_copy_path = join(file_path, COPY_ROOT_PATH_NAME)
        two_three, three_fore = map(lambda x: join(full_copy_path, x), ENABLES_FOLDERS_NAMES_FOR_PHOTO)
        if not os.path.exists(two_three):
            create_copy_dir(ENABLES_FOLDERS_NAMES_FOR_PHOTO[0])
        if not os.path.exists(three_fore):
            create_copy_dir(ENABLES_FOLDERS_NAMES_FOR_PHOTO[1])
        for data in data_clear:
            format_photo, filename, _ = data
            filename = re.sub(r'[^\d]', '', filename)
            format_photo = change_ua_x_on_en_x(format_photo).lower()
            full_file_name = f'{filename}.jpg'
            old_file_copy_path = join(file_path, full_file_name)
            new_file_copy_path = ''
            if os.path.exists(old_file_copy_path):
                if format_photo in TWO_ON_THREE:
                    new_file_copy_path = join(two_three, f'{filename}.jpg')
                elif format_photo in THREE_ON_FORE:
                    new_file_copy_path = join(three_fore, full_file_name)
                if new_file_copy_path and not os.path.exists(new_file_copy_path):
                    copyfile(old_file_copy_path, new_file_copy_path)
                    all_counter += 1
            else:
                counter_no_search_file += 1
                write_error(f'Увага файл з імям {full_file_name} не існує в даному каталозі {file_path}')
    except Exception as e:
        print(e)
    else:
        if error_str:
            print(
                f'Увага під час роботи програми виникли наступні помилки: \n\n {error_str} \n К-ть незнайдених файлів: {counter_no_search_file} шт.)')
        print(
            f'\n\n Операція в каталозі {file_path} виконана. \n К-ть скопійованих файлів {all_counter}')


if __name__ == "__main__":
    start()
