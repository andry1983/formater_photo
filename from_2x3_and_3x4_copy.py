import os
from shutil import copyfile
from os.path import join
import re

SUFIX_NAME = '.jpg'  # розширення файлів для копіювання

ENABLES_FOLDERS_NAMES_FOR_PHOTO = [  # Допустимі формати для створення папок для переіменування
    '10x15',
    '13x18',
    '15x21',
    '18x24',
    '20x28',
    '25x38',
    '30x20',
    '10x15 мат',
    '13x18 мат',
    '15x21 мат',
    '18x24 мат',
    '20x28 мат',
    '25x38 мат',
    '30x20 мат'
]

LIST_FOR_RENAME = 'form.txt'  # назва файла сценарію переіменування
DELIMETR = '$'  # розділювач по якому ми розбиваємо стрічку в масив (формат, імя файлу, к-ть)

COPY_THIS_ROOT_PATH_NAME = 'copy_photo_whitout_2x3_and_3x4'  # назва папки звідки ми копіюємо переіменовані файли
COPY_ROOT_PATH_NAME = 'copy_photo_vinetka_sort_2'  # назва папки куди ми копіюємо переіменовані файли

SMALL_FORMAT_PHOTO = [
    '10x15',
    '30x20',
    '25x38',
    '10x15 мат',
    '30x20 мат',
    '25x38 мат'
]

BIG_FORMAT_PHOTO = [
    '13x18',
    '15x21',
    '18x24',
    '20x28',
    '13x18 мат',
    '15x21 мат',
    '18x24 мат',
    '20x28 мат'
]

file_path = os.path.dirname(os.path.abspath(__file__))

error_str = ''


def change_ua_x_on_en_x(name_format, lang='ua'):
    """
    міняє англ на укр "х" і навпаки згідно параметра lang(if ua міняєм на англ х)
    """
    return re.sub(r'[хХ]', 'x', name_format) if lang == 'ua' else re.sub(r'[xX]', 'х', name_format)


def search_latin_x_in_name_folder(name_folder):
    """
    шукає кирелічний "х" в імені каталогу і замінює його на латинський х, якщо каталок незнайдено і пробує знайти його по новому імені
    """
    search_x = re.match(r'\d*[х]\d*', name_folder, re.MULTILINE) is not None
    full_path = join(file_path, COPY_THIS_ROOT_PATH_NAME, name_folder)
    if search_x:
        if os.path.exists(full_path):
            return name_folder
        else:
            folder_sub_name = change_ua_x_on_en_x(name_folder)  # cirilic x(ua)
            full_path = join(file_path, COPY_THIS_ROOT_PATH_NAME, folder_sub_name)
            return folder_sub_name if os.path.exists(full_path) else False
    else:
        folder_sub_name = change_ua_x_on_en_x(name_folder, lang='en')  # latin x (en)
        return name_folder if os.path.exists(full_path) else search_latin_x_in_name_folder(folder_sub_name)


def flag_format(format_photo) -> str:
    """
    оприділяє флаг для формата фото
    """
    format_photo = format_photo.strip('\t\n\r\s')
    flag = ''
    if format_photo in SMALL_FORMAT_PHOTO:
        flag = 'small'
    if format_photo in BIG_FORMAT_PHOTO:
        flag = 'big'
    return flag


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


def copy_file(old_name, new_name, new_path):
    """
    копіює файл по заданому шляху
    """
    copy_root_path = join(file_path, COPY_ROOT_PATH_NAME)
    if not os.path.exists(copy_root_path):
        create_copy_dir()
    old_file_name = join(file_path, old_name)
    new_file_name = join(new_path, new_name)

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
    """
    формує суфікс імені для файла який копіюється
    """
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
    """
    шукає і копіює файли формуючи правильне імя файла згідно кількості(counts)
    """
    global all_counter, smal_counter
    old_file_exist_copy = join(file_path, old_file_name)
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


def serch_folder_in_path(list_formats):
    """
    вертає список імен каталогів зі списку, які існують в даній директорії
    """
    if isinstance(list_formats, list):
        folders_for_search_list = map(search_latin_x_in_name_folder, list_formats)
        return map(lambda x: join(join(file_path, COPY_THIS_ROOT_PATH_NAME), x) if x else False,
                   folders_for_search_list)
    else:
        return []


def search_photo(flag: str, number_photo: str):
    """
    шукає фото в певних каталогах згідно того який флаг передано
    :return: повний шлях до файлу який треба скопіювати якщо він існує
    """
    folders_for_search_list = []
    if flag == 'small':
        folders_for_search_list = ['2x3']
    elif flag == 'big':
        folders_for_search_list = ['3x4']
    folder_search_list = serch_folder_in_path(folders_for_search_list)
    if folder_search_list:
        for folder_name in folder_search_list:
            if folder_name and os.path.exists(join(folder_name, number_photo)):
                return join(folder_name, number_photo)
            else:
                continue
        else:
            return False
    else:
        return False


def write_error(msg):
    """
    формує список помилок
    """
    global error_str
    if msg:
        error_str = f'{error_str}\n-\t{msg}\n'


def start():
    try:
        global all_counter
        test_exist_part_1_path = join(file_path, COPY_THIS_ROOT_PATH_NAME)
        if not os.path.exists(test_exist_part_1_path):
            print(f'Увага каталог {test_exist_part_1_path} не знайдено.\n Запустіть спочатку на виконання файл copy_in_2x3_and_3x4.py')
            return
        data_clear = file_list_for_rename()
        if len(data_clear) > 0:
            for data in data_clear:
                format_photo, filename, counts = data
                filename = re.sub(r'[^\d]', '', filename)
                counts = int(counts)
                format_photo = change_ua_x_on_en_x(format_photo).lower()
                flag_search = flag_format(format_photo)
                full_file_old_name = f'{filename}{SUFIX_NAME}'.lower()
                new_path_copy = join(file_path, COPY_ROOT_PATH_NAME, format_photo)
                file_search = search_photo(flag=flag_search, number_photo=full_file_old_name)
                if file_search:
                    copy_search_file(
                        filename=filename,
                        old_file_name=file_search,
                        new_path_copy=new_path_copy,
                        counts=counts
                    )
                else:
                    write_error(
                        f'Увага файл не знайдено: {full_file_old_name}, format_photo: {format_photo}, к-ть={counts}')
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
    input("Press enter to close program")
