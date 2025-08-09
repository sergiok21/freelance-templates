import json
from os import listdir, mkdir
from os.path import basename


def convert_cookies(json_cookies_file, netscape_cookies_file):
    with open(json_cookies_file, 'r') as j:
        json_cookies = json.load(j)

    netscape_cookies = ""

    for cookie in json_cookies:
        netscape_cookie_line = "{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n".format(
            domain=cookie['domain'],
            flag="TRUE" if cookie['httpOnly'] else "FALSE",
            path=cookie['path'],
            secure="TRUE" if cookie['secure'] else "FALSE",
            expiry=str(int(cookie['expirationDate'])),
            name=cookie['name'],
            value=cookie['value']
        )
        netscape_cookies += netscape_cookie_line

    with open(netscape_cookies_file, 'w') as n:
        n.write(netscape_cookies)


def files_processing(files):
    for file in files:
        file_read = open(file, 'r')
        json_data = json.loads(file_read.read())
        file_read.close()

        file_write = open(f'{basename(file)}_netscape.json', 'w')
        file_write.write(json.dumps(json_data))
        file_write.close()


if __name__ == '__main__':
    mkdir('jsons')
    files = listdir('.')
    files_processing(files)

    mkdir('netscape')
    jsons = listdir('json')
    for file in jsons:
        convert_cookies(file, f'{basename(file)}result.txt')
