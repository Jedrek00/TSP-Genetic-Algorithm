import os
import sys
import re
import random


def generator():

    file = open("generator.txt", 'w')
    while True:
        vertices = input('Type number of vertices: ')
        try:
            vertices = int(vertices)
            if vertices > 1:
                break
            else:
                print('Number of vertices should be at least one!')
        except ValueError:
            print('Number of vertices should be an integer!')

    file.write(str(vertices) + "\n")

    pairs = []
    i = 0
    while len(pairs) < vertices:
        x = random.randint(0, 200)
        y = random.randint(0, 200)
        if (x, y) not in pairs:
            pairs.append((x, y))
            file.write(str(i + 1) + " " + str(x) + " " + str(y) + "\n")
            i += 1

    file.close()
    return file.name


def choose_file(dir_path=None):

    if dir_path is None:
        dir_path = os.getcwd()

    dir_content = os.listdir(dir_path)
    dir_txts = list(filter(lambda x: x[-4:] == '.txt', dir_content))
    dir_txts.append('generator')

    print('\nYou can use data from: ')
    print(*dir_txts, sep='\n')

    while True:
        answer = input('Type which one would you like to use: ')

        if answer == 'generator':
            return generator()

        elif answer in dir_txts:
            print('xd')
            return dir_path + '\\' + answer

        else:
            print('Please, enter a correct name.')


def check_file(filename):

    with open(filename, encoding='utf-8-sig') as file:
        lines = file.readlines()

        try:

            number_of_lines = int(lines[0])
            for index, line in enumerate(lines[1:]):

                if index == number_of_lines:
                    print('File has too many lines!')
                    return False

                # wyrazenie regularne postaci: 'numer linii''spacja''liczba calkowita''spacja''liczba calkowita'
                # result = re.search('^' + str(index + 1) + ' -?\\d+ -?\\d+$', line)
                result = re.search(r'^\d+\s+(-?)\d+\s+(-?)\d+(\s+|$)', line)

                if result is None:
                    print(f'Invalid data in line {index + 2}')
                    return False

                if index + 1 == number_of_lines:
                    file.close()
                    return True

            print('File has not enough lines!')
            return False

        except ValueError:
            print('First line should be a single integer value!')
            return False


def distance(x1, y1, x2, y2):
    return round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2), 3)


def create_matrix(filename):

    with open(filename, encoding='utf-8-sig') as file:
        content = file.read().splitlines()

    number_of_vertices = int(content.pop(0))

    a = []
    for number in range(number_of_vertices):
        tmp = content[number].replace('  ', ' ').split(' ')
        a.append((int(tmp[1]), int(tmp[2])))

    matrix = []
    for vertex_index in range(number_of_vertices):
        distances = []
        for index in range(number_of_vertices):
            if index > vertex_index:
                distances.append(distance(a[vertex_index][0], a[vertex_index][1], a[index][0], a[index][1]))
            elif index < vertex_index:
                distances.append(matrix[index][vertex_index])
            else:
                distances.append(0)
        matrix.append(distances)

    return matrix


if __name__ == '__main__':
    f = choose_file()
    if check_file(f):
        print('Robie macierza')
        create_matrix(f)
    else:
        sys.exit(0)
