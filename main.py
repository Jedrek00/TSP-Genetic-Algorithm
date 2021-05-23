import os
import time
import pygame
import createdata
import ga


WIDTH = 900
HEIGHT = 600


def create_list(file_path):
    """
    create a list from file
    :param name: name of file (String)
    :return: list of tuples with int values
    """
    coordinates = []
    with open(file_path) as source_file:
        content = source_file.read().splitlines()
        number_of_elements = int(content.pop(0))
        for number in range(number_of_elements):
            tmp = content[number].replace('  ', ' ').split(' ')
            coordinates.append((int(tmp[1]), int(tmp[2])))
    return coordinates


def calculate_scale(coordinates):
    """
    Find the biggest x and y value from list of coordinates
    :param coordinates: list of tuples (int, int)
    :return: the biggest x value (int) and the biggest y value (int)
    """
    m_x = max(coordinates, key=lambda m: m[0])[0]
    m_y = max(coordinates, key=lambda m: m[1])[1]
    return m_x, m_y


def refactor_lis(coordinates, m_x, m_y):
    """
    Change all coordinates to fit in pygame window
    :param coordinates: list of tuples (int, int)
    :param m_x: the biggest x value
    :param m_y: the biggest y value
    :return: refactored list
    """
    coordinates = [(int(x * ((WIDTH - 100) / m_x) + 20), int(y * ((HEIGHT - 150) / m_y) + 80)) for x, y in coordinates]
    return coordinates


def main():

    while True:
        file = createdata.choose_file(os.getcwd() + '\\instances')
        # file = ''.join((os.getcwd(), '\\instances\\bier127.txt'))
        if createdata.check_file(file):
            matrix = createdata.create_matrix(file)
            break
        else:
            print("Choose another file or use a generator.")

    pygame.init()
    pygame.display.set_caption("TSP Genetic Algorithm")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Calibri', 25)
    run = True
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    colour = (127, 0, 127)
    # start_time = time.time()

    genetic = ga.GA(matrix)
    genetic.create_first_generation()
    elements = create_list(file)
    max_x, max_y = calculate_scale(elements)
    elements = refactor_lis(elements, max_x, max_y)
    while run:
        win.fill((0, 0, 0))
        clock.tick(30)

        for click in pygame.event.get():
            if click.type == pygame.QUIT:
                run = False

        # draw points on the surface
        for x, y in elements:
            pygame.draw.circle(win, colour, (x, y), 5)

        # get and draw the currently shortest route
        route = genetic.run()
        for i in range(len(route)):
            pygame.draw.line(win, colour, (elements[route[i]][0], elements[route[i]][1]),
                             (elements[route[(i+1) % (len(route))]][0], elements[route[(i+1) % (len(route))]][1]))

        # print information about algorithm results
        num_gen_txt = font.render('Number of generation: ' + str(genetic.number_of_generation), False, colour)
        route_len_txt = font.render('Length of the shortest route: ' + str(genetic.shortest_distance), False, colour)
        win.blit(num_gen_txt, (0, 0))
        win.blit(route_len_txt, (0, 30))

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
