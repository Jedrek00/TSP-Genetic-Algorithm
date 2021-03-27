import os
import pygame


class Simulation:

    WIDTH = 900
    HEIGHT = 600

    def __init__(self, name):
        self.elements = None
        self.max_x = 0
        self.max_y = 0
        self.create_list(name)
        self.calculate_scale()
        self.refactor_lis()

    def create_list(self, name):
        """
        create a list from file
        :param name: name of file (String)
        :return: list of tuples with int values
        """
        self.elements = []
        file_path = ''.join((os.getcwd(), '\\instances\\', name))
        with open(file_path) as file:
            content = file.read().splitlines()
            number_of_elements = int(content.pop(0))
            for number in range(number_of_elements):
                tmp = content[number].replace('  ', ' ').split(' ')
                self.elements.append((int(tmp[1]), int(tmp[2])))

    def calculate_scale(self):
        self.max_x = max(self.elements, key=lambda i: i[0])[0]
        self.max_y = max(self.elements, key=lambda i: i[1])[1]

    def refactor_lis(self):
        self.elements = [(int(x*((self.WIDTH-10)/self.max_x)), int(y*((self.HEIGHT-10)/self.max_y))) for x, y in self.elements]

    def loop(self, route):
        pygame.init()
        pygame.display.set_caption("TSP Genetic Algorithm")
        clock = pygame.time.Clock()
        run = True
        win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        while run:
            clock.tick(30)

            for click in pygame.event.get():
                if click.type == pygame.QUIT:
                    run = False
            for x, y in self.elements:
                pygame.draw.circle(win, (127, 0, 127), (x, y), 5)
            for i in range(len(route)):
                pygame.draw.line(win, (127, 0, 127), (self.elements[route[i]][0], self.elements[route[i]][1]),
                                 (self.elements[route[(i+1)%(len(route))]][0], self.elements[route[(i+1)%(len(route))]][1]))
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    xdd = Simulation('berlin52.txt')
    print(xdd.elements)
    r = [27, 12, 13, 51, 10, 50, 32, 42, 9, 8, 7, 40, 18, 44, 2, 17, 30, 21, 0, 31, 48, 35, 34, 33, 38, 39, 36, 37, 47, 23, 4, 14, 5, 3, 24, 45, 43, 15, 49, 29, 1, 6, 41, 16, 20, 22, 19, 28, 46, 25, 26, 11]
    xdd.loop(r)
