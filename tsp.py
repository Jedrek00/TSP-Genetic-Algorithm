import random
import time

"""
route: list of vertices in order which they be visited
"""


def calculate_fitness_of_generation(generation, matrix):
    """
    Calculate fitness of each route
    :param generation: list of routes
    :param matrix: matrix with distances between each vertices
    :return: list of route's length (float)
    """
    result = []
    for route in generation:
        distance = 0
        tmp_route = route + [route[0]]
        for index in range(len(tmp_route) - 1):
            distance += matrix[tmp_route[index]][tmp_route[index + 1]]
        result.append(round(distance, 3))

    return result


def find_shortest_route(generation, matrix):
    """
    Find the shortest route of a generation
    :param generation: list of routes
    :param matrix: matrix with distances between each vertices
    :return: distance of shortest route (float) and shortest route (list of ints)
    """
    routes = calculate_fitness_of_generation(generation, matrix)
    return min(routes), generation[routes.index(min(routes))]


def greedy(matrix, starting_index):
    visited = [starting_index]

    while len(visited) < len(matrix):
        i = visited[-1]
        min_tmp = 0
        min_index = 0
        for index, value in enumerate(matrix[i]):
            if value != 0 and index not in visited:
                if min_tmp == 0:
                    min_tmp = value
                    min_index = index
                elif min_tmp >= value:
                    min_tmp = value
                    min_index = index
        visited.append(min_index)

    return visited


# SELECTION ALGORITHMS


def tournament(generation, matrix, parents_for_next_generation):
    """
     In tournament selection, n individuals are selected randomly from the larger
    population, and the selected individuals compete against each other.
    :param generation: list of routes
    :param matrix: matrix with distances between each vertices
    :param parents_for_next_generation: number of parents (int)
    :return: list of new routes
    """
    distances = calculate_fitness_of_generation(generation, matrix)
    generation_with_distance = list(zip(generation, distances))

    new_generation = []
    while len(new_generation) != parents_for_next_generation - 1:
        size_of_tournament = random.randint(2, 6)
        random.shuffle(generation_with_distance)
        for route in sorted(generation_with_distance[:size_of_tournament], key=lambda pair: pair[1]):
            if route[0] not in new_generation:
                new_generation.append(route[0])
                break

    return new_generation


def choose_the_best(generation, matrix, parents_for_next_generation):
    """
    Choose the chromosomes with the best fitness value
    :param generation: list of routes
    :param matrix: matrix with distances between each vertices
    :param parents_for_next_generation: number of parents (int)
    :return: list of new routes
    """
    distances = calculate_fitness_of_generation(generation, matrix)
    generation_with_distance = zip(distances, generation)

    result = [x for _, x in sorted(generation_with_distance)]

    return result[:parents_for_next_generation]


def create_ranks(length):
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

    return ranks, counter


def rank_based_wheel_selection(generation, matrix, ranks, max_rank, parents_for_next_generation):
    """
    Rank-based roulette wheel selection is the selection strategy where the probability of a chromosome being
    selected is based on its fitness rank relative to the entire population.
    :param generation: list of routes
    :param matrix: matrix with distances between each vertices
    :param ranks: list of ranks used to calculate probability
    :param max_rank: highest rank
    :param parents_for_next_generation: number of parents (int)
    :return: list of new routes
    """
    distances = calculate_fitness_of_generation(generation, matrix)
    generation_with_distance = sorted(list(zip(generation, distances)), key=lambda pair: pair[1])
    new_generation = []

    while len(new_generation) < parents_for_next_generation - 1:

        guess = random.uniform(0.0, float(max_rank))
        for index, rank in enumerate(ranks):
            if rank[0] <= guess < rank[1]:
                if generation_with_distance[index][0] not in new_generation:
                    new_generation.append(generation_with_distance[index][0])

    return new_generation


# CROSSOVER ALGORITHMS


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


# MUTATION ALGORITHMS


def simple_mutation(generation, chance_for_mutation):
    """
    This mutation swaps two random vertices with each other
    :param generation: list of routes
    :param chance_for_mutation: probability that mutation will be done (int)
    :return: list of changed routes
    """
    for route in generation:

        if random.randint(1, 100) <= chance_for_mutation:
            a = random.randint(0, len(route) - 2)
            b = random.randint(a, len(route) - 1)
            route[a], route[b] = route[b], route[a]

    return generation


def inversion_mutation(generation, chance_for_mutation):
    """
    This mutation turnes upside down selected part of route
    :param generation: list of routes
    :param chance_for_mutation: probability that mutation will be done (int)
    :return: list of changed routes
    """
    for route in generation:

        if random.randint(1, 100) <= chance_for_mutation:
            a = random.randint(0, len(route) - 3) + 1
            b = random.randint(a, len(route) - 2) + 1
            route[a:b] = reversed(route[a:b])

    return generation


# GENETIC ALGORITHM STAGES


def create_first_generation(matrix, size_of_generation):
    """
    Create first generation, some of them will be created with greedy algorithm
    :param matrix: matrix with distances between each vertices
    :param size_of_generation: number of vertices
    :return: list of routes
    """
    generation = []
    cities = [x for x in range(len(matrix))]

    while len(generation) < size_of_generation:
        chance = random.randint(1, 100)
        if chance <= 85:
            route = random.sample(cities, len(cities))
        else:
            route = greedy(matrix, random.randint(0, len(cities) - 1))
        if route not in generation:
            generation.append(route)

    return generation


# def check_generation(matrix, generation, last_distance, generation_without_change):
#     shortest_distance, shortest_route = find_shortest_route(generation, matrix)
#
#     if abs(last_distance - shortest_distance) < shortest_distance * 0.001:
#         generation_without_change += 1
#     else:
#         generation_without_change = 0
#
#     chance_for_mutation = float(min(10.0, 2.0 + float(generation_without_change) / 100))
#
#     return generation_without_change, chance_for_mutation, shortest_route, shortest_distance


# B


def selection(matrix, generation, parents_for_next_generation, ranks, max_rank):
    """
    Choose parents for crossover using one of selection algorithms
    Shortest route never will be removed
    :param matrix: matrix with distances between each vertices
    :param generation: list of routes
    :param parents_for_next_generation: number of routes to select
    :param ranks: list of ranks, used in rank_based_wheel_selection()
    :param max_rank: highest rank, used in rank_based_wheel_selection()
    :return: list of routes which will be used in crossover
    """

    shortest_distance, shortest_route = find_shortest_route(generation, matrix)
    print(f"Route's length: {shortest_distance}")
    generation.remove(shortest_route)

    # generation = tournament(generation, matrix, parents_for_next_generation)
    generation = rank_based_wheel_selection(generation, matrix, ranks, max_rank, parents_for_next_generation)
    # generation = choose_the_best(generation, matrix)

    generation.append(shortest_route)

    return generation


def crossover(generation):
    """
    Creates new routes from given generation
    :param generation: list of routes
    :return: new list of routes
    """
    available_parents = [x for x in range(0, len(generation))]

    while available_parents:

        parent1_index = random.choice(available_parents)
        available_parents.remove(parent1_index)

        parent2_index = random.choice(available_parents)
        available_parents.remove(parent2_index)

        chance = random.randint(1, 10)
        if chance <= 10:
            tmp1, tmp2 = ox(generation[parent1_index], generation[parent2_index])
        else:
            tmp1, tmp2 = pmx(generation[parent1_index], generation[parent2_index])

        generation.append(tmp1)
        generation.append(tmp2)

    return generation


def mutation(generation, chance_for_mutation):
    """
    Change some of routes
    :param generation: list of routes
    :param chance_for_mutation: probability to change single route (int)
    :return: changed list of routes
    """
    generation = inversion_mutation(generation, chance_for_mutation)
    # generation = simple_mutation(generation, chance_for_mutation)

    return generation


def genetic_algorithm(matrix):
    """
    Function with main loop where generation is modified by selection, crossover and mutation
    :param matrix: matrix with distances between each vertices
    :return: None
    """
    # GA parameters
    size_of_generation = 200
    parents_for_next_generation = int(size_of_generation * 0.5)
    number_of_generation = 0
    shortest_distance = 0
    ranks, max_rank = create_ranks(size_of_generation)

    start_time = time.time()

    generation = create_first_generation(matrix, size_of_generation)

    while True:
        generation = selection(matrix, generation, parents_for_next_generation, ranks, max_rank)
        generation = crossover(generation)
        generation = mutation(generation, 7)
        number_of_generation += 1

        if time.time() - start_time >= 5:
            shortest_distance, shortest_route = find_shortest_route(generation, matrix)
            print(f'\n\nShortest distance: {shortest_distance}\nRoute:')
            for city in shortest_route:
                print(city + 1, end='->')
            print(shortest_route[0] + 1)
            break


if __name__ == '__main__':
    # genetic_algorithm()
    print(create_ranks(50, 2))
