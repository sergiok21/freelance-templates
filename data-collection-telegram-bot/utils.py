import os
import re
import shutil


async def add_user_id(user_id: str) -> None:
    if not os.path.exists('users_id.txt'):
        open('users_id.txt', 'w').close()
    read_data = open('users_id.txt', 'r')
    users = read_data.read()
    read_data.close()
    if user_id not in users:
        write_data = open('users_id.txt', 'a')
        write_data.write(user_id + '\n')
        write_data.close()


async def process_files() -> bool:
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.mkdir('results')
    os.mkdir('results/cookies')

    cookies_path = 'results/cookies'

    if not os.path.exists('data'):
        os.mkdir('data')
    dir_list = os.listdir('data')

    if dir_list:
        for directory in dir_list:
            files = os.listdir(f'data/{directory}')
            for file in files:
                shutil.copyfile(f'data/{directory}/{file}', f'{cookies_path}/{file}')

        shutil.make_archive('results', 'zip', 'results')
        shutil.make_archive('for_search', 'zip', 'data')
        return True
    else:
        return False


async def define_user(pattern) -> str or None:
    if os.path.exists('search'):
        shutil.rmtree('search')
    os.mkdir('search')

    shutil.unpack_archive('for_search.zip', 'search')

    dir_list = os.listdir('search')

    for directory in dir_list:
        for child_dir in os.listdir(f'search/{directory}'):
            if pattern in os.path.basename(child_dir):
                for file in os.listdir('.'):
                    if '.zip' in file:
                        os.remove(file)
                shutil.rmtree('search')
                return directory
    shutil.rmtree('search')
    os.remove('for_search.zip')
    return None


async def get_results() -> dict or None:
    list_dirs = os.listdir('data')

    data = {}
    if list_dirs:
        for directory in list_dirs:
            data_list_dirs = os.listdir(f'data/{directory}')
            data[directory] = len(data_list_dirs)
        return data
    return None
