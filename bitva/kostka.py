#!/usr/bin/env python3

import random

class Kostka:
    def __init__(self, pocet_sten = 6):
        self.__pocet_sten = pocet_sten

    def hod(self):
        return random.randint(1,self.__pocet_sten)

    def __str__(self):
        return f'Toto je kostka s {self.__pocet_sten} stenami.'

    def getPocet_sten(self):
        return self.__pocet_sten

def main():
    k1 = Kostka()
    k2 = Kostka(120)
    print(k1.hod())
    print(k2.hod())

if __name__ == '__main__':
    main()
