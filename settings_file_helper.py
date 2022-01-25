from os import remove

from data import constants


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


def read_into_dict(filename, d=None):
    if d is None:
        d = dict()
    with open(filename, 'r') as settings_file:
        file_lines = settings_file.readlines()[1:]
        for line in file_lines:
            line_parts = line.split(' ')
            line_parts[0] = line_parts[0] + ' '
            line_parts[1] = ' '.join(line_parts[1:])
            d[line_parts[0]] = line_parts[1].strip()
        #
    #
    return d
