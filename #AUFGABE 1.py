#AUFGABE 1
from abc import ABC, abstractmethod; 

class Datum(ABC):
    
    def __init__(self, Tag:int, Monat:int,Jahr:int):
        self._Tag:int=Tag
        self._Monat:int=Monat
        self._Jahr:int=Jahr

    @abstractmethod
    def print_date(self):
        pass


    def print_date_short(self):
        pass
        

class DatumUS(Datum):
    def __init__(self, Tag:int, Monat:int, Jahr:int):
        super().__init__(Monat, Tag, Jahr)
        self._Liste=["January","Febuary","March","April","May","June","July","August","September","October","November","Dezember"]

    def print_date(self):
        print(self._Liste[self._Monat-1] , self._Tag, self._Jahr)

    def print_date_short(self):
        print(self._Monat,"/",self._Tag,"/",self._Jahr)


class DatumDE(Datum):
    def __init__(self, Tag:int, Monat:int, Jahr:int):
        super().__init__(Tag, Monat, Jahr)
        self._Liste=["Januar","Febuar","März","April","Mai","Juni","July","August","September","October","November","Dezember"]

    def print_date(self):
        Monat_String=self._Liste[self._Monat-1]
        print(self._Tag, Monat_String , self._Jahr)

    def print_date_short(self):
        print(self._Tag,"/",self._Monat,"/",self._Jahr)


#!!! DATENEINGABE IMMER IM DEUTSCHEN SYSTEM (tag,monat,jahr)

test=DatumUS(20,10,2003)
test.print_date()
test.print_date_short()

kartoffeltest=DatumDE(20,10,2000)
kartoffeltest.print_date()
kartoffeltest.print_date_short()