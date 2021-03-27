import os
import threading
import createdata
import visualitzation
import ga


while True:
    # file = createdata.choose_file(os.getcwd() + '\\instances')
    file = os.getcwd() + '\\instances\\berlin52.txt'
    if createdata.check_file(file):
        matrix = createdata.create_matrix(file)
        break
    else:
        print("Choose another file or use a generator.")
xd = ga.GA(matrix)
xdd = visualitzation.Simulation('berlin52.txt')
r = [27, 12, 13, 51, 10, 50, 32, 42, 9, 8, 7, 40, 18, 44, 2, 17, 30, 21, 0, 31, 48, 35, 34, 33, 38, 39, 36, 37, 47, 23, 4, 14, 5, 3, 24, 45, 43, 15, 49, 29, 1, 6, 41, 16, 20, 22, 19, 28, 46, 25, 26, 11]

t1 = threading.Thread(target=xdd.loop(r), args=[r])
t2 = threading.Thread(target=xd.run, args=())

# starting thread 1
t1.start()
t2.start()

# wait until thread 1 is completely executed
t1.join()
t2.join()

# both threads completely executed
print("Done!")