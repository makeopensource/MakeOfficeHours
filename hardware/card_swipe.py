import os


def decode_pn(raw):
    try:
        return raw.split("/^")[1][14:22]
    except Exception:
        return ""

def cardSwipe():
    while True:
        line = input("Swipe card now!!! \n")
        print(decode_pn)