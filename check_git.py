import os
import csv


def main():
    path = './'
    folders = [f.path for f in os.scandir(path) if f.is_dir()]
    data = []
    for folder in sorted(folders):
        folder_obj = {
            'path': folder
        }
        folder_obj['git_init'] = os.path.exists(f'{folder}/.git')

        if folder_obj['git_init']:
            with open(f'{folder}/.git/config', 'r') as f:
                config = f.readlines()

            for index, line in enumerate(config):
                if line.startswith('[remote'):
                    full_url = config[index +
                                      1].replace('\t', '').replace('\n', '')
                    host_and_user = full_url.split(
                        '@')[1].split('/')[0].split(':')
                    folder_obj['host'] = host_and_user[0]
                    folder_obj['user'] = host_and_user[1]

        data.append(folder_obj)

    with open('done-folders.csv', 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['path', 'git_init', 'host', 'user'])

        writer.writeheader()
        writer.writerows([f for f in data if f.get('host') == 'github.com'])

    with open('folders.csv', 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['path', 'git_init', 'host', 'user'])

        writer.writeheader()
        writer.writerows([f for f in data if not f.get(
            'host') or f.get('host') != 'github.com'])


if __name__ == '__main__':
    main()
