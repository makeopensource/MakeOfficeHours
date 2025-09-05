import os


def cardSwipe():
    while True:
        line = input("Swipe card now!!! \n")
        try:
            name = line.split("/^")[1][14:22]
            print(name)
        except Exception:
            pass
cardSwipe()