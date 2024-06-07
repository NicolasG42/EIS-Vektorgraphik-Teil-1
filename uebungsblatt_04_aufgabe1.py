from abc import ABC, abstractmethod

class Datum(ABC):
    def __init__(self, tag: int, monat: int, jahr: int):
        self.tag = tag
        self.monat = monat
        self.jahr = jahr

    @abstractmethod
    def print_date(self) -> str:
        pass

    @abstractmethod
    def print_date_short(self) -> str:
        pass

class DatumDE(Datum):
    def print_date(self) -> str:
        monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        return f"{self.tag}. {monate[self.monat - 1]} {self.jahr}"

    def print_date_short(self) -> str:
        return f"{self.tag:02d}.{self.monat:02d}.{self.jahr % 100:02d}"

class DatumUS(Datum):
    def print_date(self) -> str:
        monate = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return f"{monate[self.monat - 1]} {self.tag} {self.jahr}"

    def print_date_short(self) -> str:
        return f"{self.monat:02d}/{self.tag:02d}/{self.jahr % 100:02d}"

if __name__ == "__main__":
    datumDE = DatumDE(7, 6, 2024)
    datumUS = DatumUS(7, 6, 2024)

    print("Deutsch ausfuehrlich: " + datumDE.print_date())
    print("Deutsch kurz: " + datumDE.print_date_short())
    print("US ausfuehrlich: " + datumUS.print_date())
    print("US kurz: " + datumUS.print_date_short())
