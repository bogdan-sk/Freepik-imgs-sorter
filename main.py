import os
import time


WORK_DIR = 'D:\\Mokaups\\Mockups A decals'
NON_SORTED = 'non sorted'


def make_non_sorted_dir():
    """
    Make NON SORTED directory  in work directory if that not exist
    :return:
    """
    if not os.path.isdir(f'{WORK_DIR}\\{NON_SORTED.capitalize()}'):
        os.mkdir(f'{WORK_DIR}\\{NON_SORTED.capitalize()}')


def copy_files_to_non_sorted():
    """
    Copy all files from work dir not placed in directories to NON SORTED directory
    :return:
    """
    file_names_list = [f'{WORK_DIR}\\{file_name}' for file_name in os.listdir(WORK_DIR)
                       if os.path.isfile(f'{WORK_DIR}\\{file_name}')]
    for file_name in file_names_list:
        try:
            src = file_name
            dst = f'{WORK_DIR}\\{NON_SORTED.capitalize()}\\{get_file_name_from_path(file_name)}'
            os.rename(src, dst)
        except Exception as ex:
            print(f'Error: {ex}')
            print(file_name)


def get_folders_list() -> list:
    """
    Get all folders name in work dir except for dir named NON SORTED
    :return: list
    """
    folder_names_list = [f'{WORK_DIR}\\{fold_name}' for fold_name in os.listdir(WORK_DIR)
                         if os.path.isdir(f'{WORK_DIR}\\{fold_name}') and fold_name.lower() != NON_SORTED]
    return folder_names_list


def get_files_from_non_sorted_dir(extension: str) -> list or None:
    """
    Get all files in dir NON SORTED with indicated extensions
    :return: list (pdf file names list or None)
    """
    non_sorted_dir_path = [f'{WORK_DIR}\\{fold_name}' for fold_name in os.listdir(WORK_DIR)
                           if fold_name.lower() == NON_SORTED]

    if len(non_sorted_dir_path) > 0:
        path = non_sorted_dir_path[0]
        pdf_file_names = [f'{path}\\{pdf_file_name}' for pdf_file_name in os.listdir(path)
                          if pdf_file_name.endswith(f'.{extension}')]
        return pdf_file_names
    else:
        return None


def get_file_name_from_path(path: str) -> str:
    """
    Get from file path file name
    :param path:
    :return: file_name
    """
    file_name = path.split('\\')[-1]
    return file_name


def get_unique_code() -> str:
    """
    Get time stamp in milliseconds like a unique code for files
    :return: code
    """
    return str(int(time.time()*1000000))


def get_filtered(file_name: str) -> str:
    """
    Remove elements by list from file name
    :param file_name:
    :return: file_name
    """
    elements = ('-and-', '-of-', '-in-', '-on-')
    for element in elements:
        file_name = file_name.replace(element, '-')
    return file_name


def find_files_by_dir_name(dir_names: list, pdf_file_names: list, filt=False) -> dict or None:
    """
    Find pdf file names in file names list by dir name.
    :param dir_names:
    :param pdf_file_names:
    :param filt: bool
    :return: sorted_pdf_by_dir_name (dict (key is dir name, value is file name))
    """
    sorted_pdf_by_dir_name = dict()
    for dir_name in dir_names:
        for pdf_file_name in pdf_file_names:
            if not filt:
                if dir_name.split('\\')[-1] in pdf_file_name:
                    sorted_pdf_by_dir_name.update({dir_name: pdf_file_name})
            else:
                if dir_name.split('\\')[-1] in get_filtered(pdf_file_name):
                    sorted_pdf_by_dir_name.update({dir_name: pdf_file_name})

    if len(sorted_pdf_by_dir_name) > 0:
        return sorted_pdf_by_dir_name
    else:
        return None


def create_dirs_by_list(file_names: list):
    """
    Create directories by file names list
    :param file_names:
    """
    for name in file_names:
        dir_path = f"{WORK_DIR}\\{get_file_name_from_path(name).split('.')[0]}"
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)


def move_files_to_dir(sorted_pdf_by_dir_name: dict):
    """
    Move files to destination directory
    :param sorted_pdf_by_dir_name:
    """
    for dir_path, file_path in sorted_pdf_by_dir_name.items():
        try:
            src = file_path
            dst = f"{dir_path}\\{get_file_name_from_path(file_path)}"
            os.rename(src, dst)
        except Exception as ex:
            print(f"Error: {ex}")
            print(f"{file_path}")


if __name__ == '__main__':
    # prepare work directory
    make_non_sorted_dir()
    copy_files_to_non_sorted()
    # move to directories jpg files from NON SORTED directory
    jpg_file_names_list = get_files_from_non_sorted_dir('jpg')
    if jpg_file_names_list is not None:
        create_dirs_by_list(jpg_file_names_list)
        dir_names_list = get_folders_list()
        sorted_jpg_list = find_files_by_dir_name(dir_names_list, jpg_file_names_list)
        if sorted_jpg_list is not None:
            move_files_to_dir(sorted_jpg_list)

    # find and move pdf files (license) to mockup directory process
    # if first time didn't move all pdf files try again with filter option
    filtered = False
    while True:
        pdf_file_names_list = get_files_from_non_sorted_dir('pdf')
        if pdf_file_names_list is not None:
            dir_names_list = get_folders_list()
            sorted_pdf_list = find_files_by_dir_name(dir_names_list, pdf_file_names_list, filt=filtered)
            if sorted_pdf_list is not None:
                move_files_to_dir(sorted_pdf_list)
            pdf_file_names_list = get_files_from_non_sorted_dir('pdf')
            if (not filtered) and (pdf_file_names_list is not None):
                filtered = True
            else:
                break
