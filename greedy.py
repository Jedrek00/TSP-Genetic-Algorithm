import createdata


def calculate(matrix, starting_index):
    visited = [starting_index]   # wierzchołki w kolejności w jakiej nalezy je odwiedzić
    road = 0        # całkowita odległość do pokonania
    minindex = 0

    # dla każdego wierzchołka znajdz najblizeszego sasiada
    while len(visited) < len(matrix):
        i = visited[-1]
        mintmp = 0
        minindex = 0
        for index, value in enumerate(matrix[i]):
            # nie można pojechać do samego siebie oraz już do odwiedzonego wierzchołka
            if value != 0 and index not in visited:
                # jak mintmp podstaw pierwsze miasto spełniające powyższy warunek
                if mintmp == 0:
                    mintmp = value
                    minindex = index
                elif mintmp >= value:
                    mintmp = value
                    minindex = index
        visited.append(minindex)
        road += mintmp

    print('The distance is equal to: ', round(road + matrix[minindex][0], 3))
    print(*(visited + [starting_index]), sep=' -> ')


def main():
    # while True:
    #     file = createdata.choose_file()
    #     if createdata.check_file(file):
    #         matrix = createdata.create_matrix(file)
    #         break
    #     else:
    #         print("Choose another file or use a generator.")

    file = createdata.choose_file()
    matrix = createdata.create_matrix(file)
    calculate(matrix, 3)


if __name__ == '__main__':
    main()
