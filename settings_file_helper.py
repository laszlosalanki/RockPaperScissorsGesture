from data import constants
from os import remove


def update_settings_file(file_with_path, key, value, header=constants.ACT_GAME_SETTINGS_HEADER):
    with open(file_with_path, 'r') as settings_file:
        lines = settings_file.readlines()[1:]
    #

    if key in ''.join(lines):
        remove(file_with_path)

        for i in range(len(lines)):
            if lines[i].startswith(key):
                lines[i] = key + str(value) + '\n'
        #

        with open(file_with_path, 'w') as settings_file:
            settings_file.write(header + '\n')
            settings_file.writelines(lines)
        #
    else:
        remove(file_with_path)

        lines.append(key + str(value) + '\n')

        with open(file_with_path, 'w') as settings_file:
            settings_file.write(header + '\n')
            settings_file.writelines(lines)
        #
    #


def create_settings_file(file_with_path, header=constants.ACT_GAME_SETTINGS_HEADER):
    with open(file_with_path, 'w') as settings_file:
        settings_file.write(header)
        settings_file.write('\n')
    #
