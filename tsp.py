import random
import time


def calculate_fitness_of_generation(generation, matrix):
    result = []
    for route in generation:
        distance = 0
        tmp_route = route + [route[0]]
        for index in range(len(tmp_route) - 1):
            distance += matrix[tmp_route[index]][tmp_route[index + 1]]
        result.append(round(distance, 3))

    return result


def find_shortest_route(generation, matrix):
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
    distances = calculate_fitness_of_generation(generation, matrix)
    generation_with_distance = zip(distances, generation)

    result = [x for _, x in sorted(generation_with_distance)]

    return result[:parents_for_next_generation]


def create_ranks(length, sp):
    ranks = []
    counter = 0
    for pos in range(length):
        rank = (2 - (2 * (sp - 1) * pos / (length - 1))) * 2
        ranks.append((round(counter, 2), round(counter + rank, 2)))
        counter += rank

    return ranks, counter


def rank_based_wheel_selection(generation, matrix, ranks, max_rank, parents_for_next_generation):
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
    for route in generation:

        if random.randint(1, 100) <= chance_for_mutation:
            a = random.randint(0, len(route) - 2)
            b = random.randint(a, len(route) - 1)
            route[a], route[b] = route[b], route[a]

    return generation


def inversion_mutation(generation, chance_for_mutation):
    for route in generation:

        if random.randint(1, 100) <= chance_for_mutation:
            a = random.randint(0, len(route) - 3) + 1
            b = random.randint(a, len(route) - 2) + 1
            route[a:b] = reversed(route[a:b])

    return generation


# GENETIC ALGORITHM STAGES


def create_first_generation(matrix, size_of_generation):
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


def check_generation(matrix, generation, last_distance, generation_without_change):
    shortest_distance, shortest_route = find_shortest_route(generation, matrix)

    if abs(last_distance - shortest_distance) < shortest_distance * 0.001:
        generation_without_change += 1
    else:
        generation_without_change = 0

    chance_for_mutation = float(min(10.0, 2.0 + float(generation_without_change) / 100))

    return generation_without_change, chance_for_mutation, shortest_route, shortest_distance


# B


def selection(matrix, generation, shortest_route, parents_for_next_generation, ranks, max_rank):

    generation.remove(shortest_route)

    # generation = tournament(generation, matrix, parents_for_next_generation)
    generation = rank_based_wheel_selection(generation, matrix, ranks, max_rank, parents_for_next_generation)
    # generation = choose_the_best(generation, matrix)

    generation.append(shortest_route)

    return generation


def crossover(generation):
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
    generation = inversion_mutation(generation, chance_for_mutation)
    # generation = simple_mutation(generation, chance_for_mutation)

    return generation


def genetic_algorithm(matrix):
    # GA parameters
    size_of_generation = 200
    parents_for_next_generation = int(size_of_generation * 0.5)
    number_of_generation = 0
    shortest_distance = 0
    generation_without_change = 0
    ranks, max_rank = create_ranks(size_of_generation, 2)

    start_time = time.time()

    generation = create_first_generation(matrix, size_of_generation)

    while True:

        generation_without_change, chance_for_mutation, shortest_route, shortest_distance = check_generation(matrix,
                                                                                                             generation,
                                                                                                             shortest_distance,
                                                                                                             generation_without_change)

        generation = selection(matrix, generation, shortest_route, parents_for_next_generation, ranks, max_rank)
        generation = crossover(generation)
        generation = mutation(generation, chance_for_mutation)
        number_of_generation += 1

        print(f"Route's length: {shortest_distance}")

        if time.time() - start_time >= 120:
            print(f'\n\nShortest distance: {shortest_distance}\nRoute:')
            for city in shortest_route:
                print(city + 1, end='->')
            print(shortest_route[0] + 1)
            break


# def main():
#
#     global chance_for_mutation
#     global size_of_generation
#     global parents_for_next_generation
#
#     # for size in range(15):
#     #     print((size + 1) * 20)
#     #     size_of_generation += 20
#     #     parents_for_next_generation = int(size_of_generation * 0.5)
#     #
#     #     createdata.generator(size_of_generation)
#     #     matrix = createdata.create_matrix('generator.txt')
#     #
#     #     greedy_route = greedy(matrix, 0)
#     #     print(f'Greedy: {calculate_fitness_of_generation([greedy_route], matrix)[0]}')
#
#     for attempt in range(5):
#
#         start_time = time.time()
#
#         cities = [x for x in range(len(matrix))]
#         ranks, max_rank = create_ranks(size_of_generation, 2)
#         # print(ranks)
#         generation = []
#         i = 0
#         generation_without_change = 0
#         last_distance = 0
#
#         while len(generation) < size_of_generation:
#             chance = random.randint(1, 100)
#             if chance <= 100:
#                 route = random.sample(cities, len(cities))
#             else:
#                 route = greedy(matrix, random.randint(0, len(cities) - 1))
#             if route not in generation:
#                 generation.append(route)
#
#         while True:
#
#             # random.shuffle(generation)
#
#             tmp_distance, tmp_route = find_shortest_route(generation, matrix)
#
#             if abs(last_distance - tmp_distance) < tmp_distance * 0.001:
#                 generation_without_change += 1
#             else:
#                 generation_without_change = 0
#
#             chance_for_mutation = float(min(10.0, 2.0 + float(generation_without_change) / 100))
#
#             print(f'{i + 1} :  {tmp_distance}, {tmp_route}')
#             last_distance = tmp_distance
#             i += 1
#
#             generation.remove(tmp_route)
#
#             generation = tournament(generation, matrix)
#             # generation = rank_based_wheel_selection(generation, matrix, ranks, max_rank)
#             # generation = choose_the_best(generation, matrix)
#
#             generation.append(tmp_route)
#
#             available_parents = [x for x in range(0, len(generation))]
#
#             while available_parents:
#
#                 parent1_index = random.choice(available_parents)
#                 available_parents.remove(parent1_index)
#
#                 parent2_index = random.choice(available_parents)
#                 available_parents.remove(parent2_index)
#
#                 chance = random.randint(1, 10)
#                 if chance <= 10:
#                     tmp1, tmp2 = ox(generation[parent1_index], generation[parent2_index])
#                 else:
#                     tmp1, tmp2 = pmx(generation[parent1_index], generation[parent2_index])
#
#                 generation.append(tmp1)
#                 generation.append(tmp2)
#
#             generation = inversion_mutation(generation)
#             generation = simple_mutation(generation)
#
#             if time.time() - start_time >= 120:
#                 # print(time.time() - start_time)
#                 break
#         print(f'GA: {tmp_distance}')
#     print('END')
#

if __name__ == '__main__':
    # genetic_algorithm()
    print(create_ranks(50, 2))
