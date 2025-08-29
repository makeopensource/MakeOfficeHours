import os


def polling():
    #file = open('hardware.txt', 'r')
    #read = file.readlines()
    #while len(read) == 0:
        #file = open('hardware.txt', 'r')
        #read = file.readlines()

    #print('stuff')
    file = open('hardware.txt', 'r')
    read = file.readlines()
    size = len(read)

    while size == 0:
        file.close()
        file = open('hardware.txt', 'r')
        read = file.readlines()
        size = len(read)


    print("full")


polling()
