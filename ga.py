import random
import time


class GA:

    def __init__(self, matrix):
        self.generation = None
        self.matrix = matrix
        self.size_of_generation = 200
        self.parents_for_next_generation = 100
        self.number_of_generation = 0
        self.shortest_route = None
        self.shortest_distance = None
        self.ranks = None
        self.max_rank = 0
        self.chance_for_mutation = 7
        self.create_first_generation()
        self.__create_ranks(self.size_of_generation)

    def create_first_generation(self):
        """
        Create first generation, some of them will be created with greedy algorithm
        """
        generation = []
        cities = [x for x in range(len(self.matrix))]

        while len(generation) < self.size_of_generation:
            chance = random.randint(1, 100)
            if chance <= 85:
                route = random.sample(cities, len(cities))
            else:
                route = self.__greedy(random.randint(0, len(cities) - 1))
            if route not in generation:
                generation.append(route)
        self.generation = generation

    def run(self):
        """
        Function with main loop where generation is modified by selection, crossover and mutation
        :return: None
        """
        start_time = time.time()
        self.create_first_generation()

        while True:
            self.selection()
            self.crossover()
            self.mutation()
            self.number_of_generation += 1

            if time.time() - start_time >= 5:
                self.find_shortest_route()
                # print(f'\n\nShortest distance: {self.shortest_distance}\nRoute:')
                for city in self.shortest_route:
                    print(city + 1, end='->')
                # print(self.shortest_route[0] + 1)
                break

    def selection(self):
        """
        Choose parents for crossover using one of selection algorithms
        Shortest route never will be removed
        :return: None
        """

        self.find_shortest_route()
        print(f"Route's length: {self.shortest_distance}")
        self.generation.remove(self.shortest_route)

        # self.tournament()
        self.rank_based_wheel_selection()

        self.generation.append(self.shortest_route)

    def crossover(self):
        """
        Creates new routes from given generation
        :return: new list of routes
        """
        available_parents = [x for x in range(0, len(self.generation))]

        while available_parents:

            parent1_index = random.choice(available_parents)
            available_parents.remove(parent1_index)

            parent2_index = random.choice(available_parents)
            available_parents.remove(parent2_index)

            chance = random.randint(1, 10)
            if chance <= 10:
                tmp1, tmp2 = self.ox(self.generation[parent1_index], self.generation[parent2_index])
            else:
                tmp1, tmp2 = self.pmx(self.generation[parent1_index], self.generation[parent2_index])

            self.generation.append(tmp1)
            self.generation.append(tmp2)

    def mutation(self):
        """
        Change some of routes
        :return: changed list of routes
        """
        self.inversion_mutation()
        # self.simple_mutation()

    def simple_mutation(self):
        """
        This mutation swaps two random vertices with each other
        :return: list of changed routes
        """
        for route in self.generation:

            if random.randint(1, 100) <= self.chance_for_mutation:
                a = random.randint(0, len(route) - 2)
                b = random.randint(a, len(route) - 1)
                route[a], route[b] = route[b], route[a]

    def inversion_mutation(self):
        """
        This mutation turns upside down selected part of route
        :return: list of changed routes
        """
        for route in self.generation:

            if random.randint(1, 100) <= self.chance_for_mutation:
                a = random.randint(0, len(route) - 3) + 1
                b = random.randint(a, len(route) - 2) + 1
                route[a:b] = reversed(route[a:b])

    @staticmethod
    def pmx(parent1, parent2):
        """
        Create two new routes from given routes using pmx operator
        https://www.hindawi.com/journals/cin/2017/7430125/
        :param parent1: route
        :param parent2:  route
        :return: two routes
        """
        length = len(parent1)
        point1 = random.randint(0, length - 2)
        point2 = random.randint(point1, length - 1)

        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        for x in range(length):

            if x in range(point1, point2):
                continue

            while child1[x] in child1[point1:point2]:
                child1[x] = child2[child1.index(child1[x], point1, point2)]

            while child2[x] in child2[point1:point2]:
                child2[x] = child1[child2.index(child2[x], point1, point2)]

        return child1, child2

    @staticmethod
    def ox(parent1, parent2):
        """
        Create two new routes from given routes using ox operator
        https://www.hindawi.com/journals/cin/2017/7430125/
        :param parent1: route
        :param parent2:  route
        :return: two routes
        """
        length = len(parent1)
        point1 = random.randint(0, length - 2)
        point2 = random.randint(point1, length - 1)

        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        pattern1 = [elem for elem in parent1[point2:] + parent1[:point2] if elem not in child1[point1:point2]]
        pattern2 = [elem for elem in parent2[point2:] + parent2[:point2] if elem not in child2[point1:point2]]

        for index in range(point2, point1 + length):
            child1[index % length] = pattern1[index - point2]
            child2[index % length] = pattern2[index - point2]

        return child1, child2

    def rank_based_wheel_selection(self):
        """
        Rank-based roulette wheel selection is the selection strategy where the probability of a chromosome being
        selected is based on its fitness rank relative to the entire population.
        :return: list of new routes
        """
        distances = self.__calculate_fitness_of_generation()
        generation_with_distance = sorted(list(zip(self.generation, distances)), key=lambda pair: pair[1])
        new_generation = []

        while len(new_generation) < self.parents_for_next_generation - 1:

            guess = random.uniform(0.0, float(self.max_rank))
            for index, rank in enumerate(self.ranks):
                if rank[0] <= guess < rank[1]:
                    if generation_with_distance[index][0] not in new_generation:
                        new_generation.append(generation_with_distance[index][0])

        self.generation = new_generation

    def tournament(self):
        """
         In tournament selection, n individuals are selected randomly from the larger
        population, and the selected individuals compete against each other.
        :return: list of new routes
        """
        distances = self.__calculate_fitness_of_generation()
        generation_with_distance = list(zip(self.generation, distances))

        new_generation = []
        while len(new_generation) != self.parents_for_next_generation - 1:
            size_of_tournament = random.randint(2, 6)
            random.shuffle(generation_with_distance)
            for route in sorted(generation_with_distance[:size_of_tournament], key=lambda pair: pair[1]):
                if route[0] not in new_generation:
                    new_generation.append(route[0])
                    break

        self.generation = new_generation

    def find_shortest_route(self):
        """
        Find the shortest route of a generation
        :return: distance of shortest route (float) and shortest route (list of ints)
        """
        routes = self.__calculate_fitness_of_generation()
        self.shortest_distance = min(routes)
        self.shortest_route = self.generation[routes.index(min(routes))]

    def __calculate_fitness_of_generation(self):
        """
        Calculate fitness of each route
        :return: list of route's length (float)
        """
        result = []
        for route in self.generation:
            distance = 0
            tmp_route = route + [route[0]]
            for index in range(len(tmp_route) - 1):
                distance += self.matrix[tmp_route[index]][tmp_route[index + 1]]
            result.append(round(distance, 3))

        return result

    def __create_ranks(self, length):
        """
        Create ranks used in rank-based roulette wheel selection
        :param length: number of vertices (int)
        :return: list of ranks and max rank
        """
        ranks = []
        counter = 0
        for pos in range(length):
            rank = (2 - (2 * pos / (length - 1))) * 2
            ranks.append((round(counter, 2), round(counter + rank, 2)))
            counter += rank

        self.ranks, self.max_rank = ranks, counter

    def __greedy(self, starting_index):
        """
        Finding route finding the closest to the each vertex
        :param starting_index: vertex from which algorithm starts searching
        :return: list of vertices
        """
        visited = [starting_index]
        while len(visited) < len(self.matrix):
            i = visited[-1]
            min_tmp = 0
            min_index = 0
            for index, value in enumerate(self.matrix[i]):
                if value != 0 and index not in visited:
                    if min_tmp == 0:
                        min_tmp = value
                        min_index = index
                    elif min_tmp >= value:
                        min_tmp = value
                        min_index = index
            visited.append(min_index)

        return visited
