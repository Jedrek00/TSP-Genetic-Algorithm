import os
import createdata
import tsp


while True:
    file = createdata.choose_file(os.getcwd() + '\\instances')
    if createdata.check_file(file):
        matrix = createdata.create_matrix(file)
        break
    else:
        print("Choose another file or use a generator.")
tsp.genetic_algorithm(matrix)
