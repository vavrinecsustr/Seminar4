#!/usr/bin/env python3

'''
Lod a odvozene tridy pro vesmirny souboj
'''

class Lod:
    '''
    Zakladni trida reprezentujici lod
    '''

    def __init__(self, jmeno, trup, utok, stit, kostka):
        self._jmeno = jmeno
        self._trup = trup
        self._max_trup = trup
        self._utok = utok
        self._stit = stit
        self._kostka = kostka
        self._zprava = ''

    def __str__(self):
        return str(self._jmeno)

    def je_operacni(self):
        return self._trup > 0
    
    def graficky_ukazatel(self, aktualni, maximalni):
        celkem = 20
        pocet = int(aktualni / maximalni * celkem)
        if pocet == 0 and self.je_operacni:
            pocet = 1
        return f"[{'#'*pocet}{' '*(celkem-pocet)}]"

    def graficky_trup(self):
        return self.graficky_ukazatel(self._trup, self._max_trup)
        
    def utoc(self, souper):
        uder = self._utok + self._kostka.hod()
        zprava = f'{self._jmeno} pali kanony za {uder}hp.'
        self.nastav_zpravu(zprava)
        souper.bran_se(uder)

    def bran_se(self, uder):
        poskozeni = uder - (self._stit + self._kostka.hod())
        if poskozeni > 0:
            zprava = f'{self._jmeno} utrpela zasah o sile {poskozeni} hp.'
            self._trup -= poskozeni
            if self._trup < 0:
                self._trup = 0
                zprava = f'{zprava[:-1]} a byla znicena.'
        else:
            zprava = f'{self._jmeno} odrazil utok stity.'
        self.nastav_zpravu(zprava)

    def nastav_zpravu(self, zprava):
        self._zprava = zprava

    def vypis_zpravu(self):
        return self._zprava

class Karen(Lod):
    """
    Odvozena trida, ktera pridava energii pro laserovy vyvoj
    Demonstruje dedicnost, polymorfismus a pretizeni metody
    """

    def __init__(self, jmeno, trup, utok, stit, kostka, energie, laserovy_utok):
        super().__init__(jmeno, trup, utok, stit, kostka)
        self._energie = energie
        self._max_energie = energie
        self._laserovy_utok = laserovy_utok

    def utoc(self, souper):
        if self._energie < self._max_energie:
            self._energie = min(self._max_energie, self._energie + 10)
            super().utoc(souper)
        else:
            uder = self._laserovy_utok + self._kostka.hod()
            self.nastav_zpravu(f'{self._jmeno} utoci laserem o sile{uder} hp.')
            self._energie = 0
            souper.bran_se(uder)

    def graficka_energie(self):
        return self.graficky_ukazatel(self._energie, self._max_energie)

class Babeta(Lod):
    """
    Odvozena trida, ktera ma vetsi stitovou obranu
    """
    def bran_se(self, uder):
        poskozeni = uder - (self._stit + self._kostka.hod() + 2)
        if poskozeni > 0:
            zprava = f'{self._jmeno} utrpela zasah o sile {poskozeni} hp.'
            self._trup -= poskozeni
            if self._trup < 0:
                self._trup = 0
                self.nastav_zpravu(f'{self._jmeno} a byla znicena.')
        else:
            self.nastav_zpravu(f'{self._jmeno} zcela pohltila utok adaptivnimi stity.')