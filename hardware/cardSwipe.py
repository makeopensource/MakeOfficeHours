import os


def cardSwipe():
    while True:
        line = input()
        try:
            name = line.split("/^")[1][14:22]
            print(name)
        except Exception:
            pass
cardSwipe()