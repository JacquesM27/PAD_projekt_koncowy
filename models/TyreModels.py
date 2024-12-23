class TyreSize:
    """
    Klasa reprezentująca pojedynczy rozmiar opony.
    """
    def __init__(self, szerokosc: int, profil: int, srednica: int):
        """
        Konstruktor klasy TyreSize.

        :param szerokosc: Szerokość opony (np. 205)
        :param profil: Profil opony (np. 55)
        :param srednica: Średnica opony (np. 16)
        """
        self.szerokosc = szerokosc
        self.profil = profil
        self.srednica = srednica

    def __str__(self):
        """
        Zwraca reprezentację tekstową rozmiaru opony w formacie "205/55R16".
        """
        return f"{self.szerokosc}/{self.profil}R{self.srednica}"

    def to_safe_filename(self):
        return f"{self.szerokosc}_{self.profil}R{self.srednica}"

    def to_dict(self):
        """
        Zwraca słownikową reprezentację rozmiaru.
        """
        return {
            "szerokość": self.szerokosc,
            "profil": self.profil,
            "średnica": self.srednica
        }

class TyreSizeData:
    """
    Klasa przechowująca listę i słownik popularnych rozmiarów opon.
    """
    # Statyczna lista z obiektami TyreSize
    TYRE_DATA = [
        TyreSize(185, 50, 16),
        TyreSize(185, 55, 16),
        TyreSize(185, 60, 16),

        TyreSize(195, 45, 16),
        TyreSize(195, 50, 16),
        TyreSize(195, 60, 16),
        TyreSize(195, 65, 16),

        TyreSize(205, 45, 16),
        TyreSize(205, 50, 16),
        TyreSize(205, 55, 16),
        TyreSize(205, 60, 16),
        TyreSize(205, 65, 16),

        TyreSize(215, 45, 16),
        TyreSize(215, 50, 16),
        TyreSize(215, 55, 16),
        TyreSize(215, 60, 16),
        TyreSize(215, 65, 16),

        TyreSize(225, 50, 16),
        TyreSize(225, 55, 16),
        TyreSize(225, 60, 16),
        TyreSize(225, 65, 16),
        TyreSize(225, 70, 16),
        TyreSize(225, 75, 16),


        TyreSize(205, 40, 17),
        TyreSize(205, 45, 17),
        TyreSize(205, 50, 17),
        TyreSize(205, 55, 17),

        TyreSize(215, 40, 17),
        TyreSize(215, 45, 17),
        TyreSize(215, 50, 17),
        TyreSize(215, 55, 17),
        TyreSize(215, 60, 17),
        TyreSize(215, 65, 17),

        TyreSize(225, 45, 17),
        TyreSize(225, 50, 17),
        TyreSize(225, 55, 17),
        TyreSize(225, 60, 17),
        TyreSize(225, 65, 17),

        TyreSize(235, 40, 17),
        TyreSize(235, 45, 17),
        TyreSize(235, 50, 17),
        TyreSize(235, 55, 17),
        TyreSize(235, 60, 17),
        TyreSize(235, 65, 17),

        TyreSize(245, 40, 17),
        TyreSize(245, 45, 17),
        TyreSize(245, 55, 17),
        TyreSize(245, 65, 17),

        TyreSize(255, 40, 17),
        TyreSize(255, 45, 17),
        TyreSize(255, 50, 17),
        TyreSize(255, 55, 17),
        TyreSize(255, 60, 17),
        TyreSize(255, 65, 17),


        TyreSize(215, 35, 18),
        TyreSize(215, 40, 18),
        TyreSize(215, 45, 18),
        TyreSize(215, 50, 18),
        TyreSize(215, 55, 18),

        TyreSize(225, 35, 18),
        TyreSize(225, 40, 18),
        TyreSize(225, 45, 18),
        TyreSize(225, 50, 18),
        TyreSize(225, 55, 18),
        TyreSize(225, 60, 18),

        TyreSize(235, 40, 18),
        TyreSize(235, 45, 18),
        TyreSize(235, 50, 18),
        TyreSize(235, 55, 18),
        TyreSize(235, 60, 18),
        TyreSize(235, 65, 18),

        TyreSize(245, 35, 18),
        TyreSize(245, 40, 18),
        TyreSize(245, 45, 18),
        TyreSize(245, 50, 18),
        TyreSize(245, 55, 18),
        TyreSize(245, 60, 18),

        TyreSize(255, 35, 18),
        TyreSize(255, 40, 18),
        TyreSize(255, 45, 18),
        TyreSize(255, 50, 18),
        TyreSize(255, 55, 18),
        TyreSize(255, 60, 18),

        TyreSize(265, 35, 18),
        TyreSize(265, 40, 18),
        TyreSize(265, 45, 18),

        TyreSize(275, 35, 18),
        TyreSize(275, 40, 18),
        TyreSize(275, 45, 18),


        TyreSize(225, 35, 19),
        TyreSize(225, 40, 19),
        TyreSize(225, 45, 19),
        TyreSize(225, 50, 19),
        TyreSize(225, 55, 19),

        TyreSize(235, 35, 19),
        TyreSize(235, 40, 19),
        TyreSize(235, 45, 19),
        TyreSize(235, 50, 19),
        TyreSize(235, 55, 19),
        TyreSize(235, 60, 19),

        TyreSize(245, 35, 19),
        TyreSize(245, 40, 19),
        TyreSize(245, 45, 19),
        TyreSize(245, 50, 19),
        TyreSize(245, 55, 19),

        TyreSize(255, 30, 19),
        TyreSize(255, 35, 19),
        TyreSize(255, 40, 19),
        TyreSize(255, 45, 19),
        TyreSize(255, 50, 19),
        TyreSize(255, 55, 19),

        TyreSize(265, 30, 19),
        TyreSize(265, 35, 19),
        TyreSize(265, 40, 19),
        TyreSize(265, 45, 19),
        TyreSize(265, 50, 19),
        TyreSize(265, 55, 19),

        TyreSize(275, 30, 19),
        TyreSize(275, 35, 19),
        TyreSize(275, 40, 19),
        TyreSize(275, 45, 19),
        TyreSize(275, 50, 19),
        TyreSize(275, 55, 19),

        TyreSize(285, 30, 19),
        TyreSize(285, 35, 19),
        TyreSize(285, 40, 19),
        TyreSize(285, 45, 19),

        TyreSize(295, 30, 19),
        TyreSize(295, 35, 19),
        TyreSize(295, 40, 19),
        TyreSize(295, 45, 19),
    ]

    # Słownik generowany dynamicznie na podstawie listy TYRE_DATA
    SIZES = [str(tyre) for tyre in TYRE_DATA]

    @staticmethod
    def display_sizes():
        """
        Wyświetla wszystkie rozmiary opon w formacie klucz - wartość.
        """
        for size, obj in TyreSizeData.SIZES.items():
            print(f"{size} -> {obj}")

    @staticmethod
    def get_tyre_by_size(size: str):
        """
        Zwraca obiekt TyreSize na podstawie podanego klucza (rozmiaru).
        """
        return TyreSizeData.SIZES.get(size, None)