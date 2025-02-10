import pymongo
from pymongo import MongoClient
from pprint import pprint

# Żadna z poniższych klas nie tworzy
class Document():
    """
    Class generating document which be adding to DB
    """
    
    def __init__(self, kolekcja='', klucze=None, user=True, values=None):
        
        self.pola = {}
        
        def _pobierz_wartosc_user(i):
            
            a = input(f"Podaj {i}: ")
            
            if a == '':
                
                pass
            
            else:
                
                try:
                    
                    self.pola[i] = eval(a)
                
                except:
                
                    self.pola[i] = a

        if user:               
            
            for i in self._klucze(collection=kolekcja):

                    _pobierz_wartosc_user(i)
                            
            if klucze is not None:
                
                for i in klucze:
                    
                    if i not in self.pola.keys():
                        
                        _pobierz_wartosc_user(i)

                
                    
            a = self._czy_wyjsc()
            
            if a:
            
                def _unikalnosc_kluczy():
                    
                    keys  = input("Podaj po przecinku klucze: ").split(',')
                    
                    if len(keys) == len(set(keys)):
                        
                        keys = [i.removeprefix(' ').removesuffix(' ') for i in keys]
                        return keys
                    
                    else:
                        
                        print("Klucze nie są unikatowe, spróbuj ponownie")
                        _unikalnosc_kluczy()
                        
                        
                keys = _unikalnosc_kluczy()    
                
                
                def _zgodnosc_liczby_el(keys):
                    
                    values = input("Podaj po przecinku wartości: ").split(',')
                    
                    if len(keys) == len(values):
                        
                        values = [i.removeprefix(' ').removesuffix(' ') for i in values]
                        return values
                    
                    else:
                        
                        a = input("Liczba kluczy jest inna niż liczba wartości. \n Chcesz ponownie podać klucze ('k') czy wartosci ('w')?")
                        
                        if a == 'k':
                            
                            keys = _unikalnosc_kluczy()
                            return values
                            
                        else:
                            
                            return _zgodnosc_liczby_el(keys)
                        
                values = _zgodnosc_liczby_el(keys)
            
            pola = dict(zip(keys, values))
            
            try:
                
                for i in pola.keys():
                    
                    self.pola[i] = pola[i]
            
            except:   
                
                self.pola = pola
        else:
            
            if values is not None and keys is not None:
                
                self.pola = dict(zip(keys, values))
                
            else:
                
                self.pola = {}
                
        self.print_document()
        
        
    def print_document(self):
        
        """Method printing document
        """
        pprint(self.pola)
    
    def app(self, klucze, wartosci):
        
        self.pola = self.pola | dict(zip(klucze, wartosci))
        
    def _czy_wyjsc(self):
        
        """Method asking user if he added everything what he wanted
        Returns
        -------
        int
            Flag control exit from loop in constructor
        """
        
        r = input("Czy to już wszystko (y/n)? ")
        
        if r == 'y':
            
            return 0
        
        elif r == 'n':
            
            return 1
        
        else:
            
            print("Zła wartość, spróbuj jeszcze raz")
            self._czy_wyjsc()
    
    def _klucze(self, collection, db='hodowla', uri="mongodb://localhost:27017/"):
        """Method downloading keys existance in collection to which user trying add document.

        Parameters
        ----------
        collection : str
            Collection's name
        db : str, optional
            Database's name, by default 'hodowla'
        uri : str, optional
            Uri to mongo base, by default "mongodb://localhost:27017/"

        Returns
        -------
        set
            Set of keys using in collection
        """
        if collection == '':
            
            return []
        
        else:
            
            client = MongoClient(uri)
            db = client[db]
            col = db[collection]
            uniq_keys = set()
            
            for doc in col.find({},{"_id":0}):
                
                uniq_keys.update(doc.keys())
                
            return uniq_keys
    
# Below classes was primal concept how to collect information in database, but actuall idea is better - more flexible, more general and better stucturized than this
  
# class Owad(Document):
#     """A class inheriting from the Document class that creates a document that will represent the insect in the database
#     """
#     def __init__(self):
        
#         super().__init__(kolekcja="Owady")
    
#     def print_values(self):
        
#         return super().print_values()
    
    
# class Pajeczak(Document):
#     """A class inheriting from the Document class that creates a document that will represent the arachnid in the database
#     """
#     def __init__(self):
        
#         super().__init__(kolekcja="Pajęczaki")
        
#     def print_values(self):
        
#         return super().print_values()   
    
class Gatunek(Document):
    """"Create document about spieces

    Parameters
    ----------
    Document : Document
        Higher class for each doc creted manually via app running
        
    """
    def __init__(self):
        
        super().__init__(kolekcja="Gatunki", 
                         klucze=[
                             "rzad_lac", "rzad_pl", "podrzad_lac", "podrzad_pl",
                             "rodzina_lac", "rodzina_pl", "podrodzina_lac", "podrodzina_pl",
                             "rodzaj_lac", "rodzaj_pl","gatunek_lac","gatunek_pl",
                             "wystepowanie","opis_gatunku", "info_nt_hodowli"])
        
    def print_values(self):
        
        return super().print_values()   

class Okaz(Document):
    """Create document about especial example of species
    Parameters
    ----------
    Document : Document
        Higher class for each doc creted manually via app running
        
    """
    def __init__(self, species):
                
        with MongoClient() as client:
            
            gat = client['hodowla']['Gatunki']
            
            id_gat = gat.find_one(
                {
                    "$or":[
                        {"gatunek_pl":species},
                        {"gatunek_lac":species}
                    ]
                }
            )
            
            def _wybor(cecha, zbior_cech):
                
                c = input(f"Podaj {cecha} ({'/'.join(zbior_cech)})")
                
                if c not in zbior_cech:
                    
                    print("Nie rozpoznano cechy")
                    _wybor(cecha, zbior_cech)
                
                else: 
                    
                    return c
                
            plec = _wybor("płeć", ["samiec", "samica", "nosex"])
            self.pola['plec'] = plec
            
            stadium = _wybor("stadium", ["L_","adult", "jajo"])
            self.pola['stadium'] = stadium
            
            if id_gat is None:
                
                print("O proszę, widzę, że to nowy gatunek. Podaj trochę więcej informacji na jego temat")
                
                
                
                new_gat = Gatunek()
                gat.insert_one(new_gat.pola)

                id_gat = gat.find_one(new_gat.pola)['_id']
                

                match plec:
                    
                    case "samiec":
                        
                        values = [id_gat, {stadium : 1}, {}, {}]
                        
                    case "samica":
                        
                        values = [id_gat, {}, {stadium : 1}, {}]
                    
                    case "nosex":
                
                        values = [id_gat, {}, {}, {stadium : 1}]
                    
                    case _:
                        
                        pass
                    
                new_stan = Stan(id_gat=id_gat, values=values)
                
                stan = client['hodowla']['Stan']
                stan.insert_one(new_stan.pola)
                
                
            else:
                
                id_gat = id_gat['_id']
                
                def _czy_nowy():
                
                    czy_nowy = input("Czy to nowy egzemplarz w hodowli? (y/n)")
                    
                    if czy_nowy == 'y':
                        
                        stan.update_one(
                            {"gatunek":gatunek}, 
                                {
                                    '$inc' : {
                                        '.'.join([plec, stadium]) : 1
                                        }
                                    }
                                )
                        
                    elif czy_nowy == "n":
                        
                        pass
                    
                    else:
                        
                        print("Nie rozpoznano polecenia")
                    
                _czy_nowy()
        
        super().__init__(klucze=["imie","historia_rozwoju","historia_karmienia","odmiana"])        
        self.pola["gatunek"] = id_gat
        
                
            
    def print_values(self):
        
        return super().print_values()      
    
class Stan(Document):
    """Create document about state of breeding for given speciec

    Parameters
    ----------
    Document : Document
        Higher class for each doc creted manually via app running
        
    """
    def __init__(self, values, kolekcja='Stan', user=False, ):
        
        klucze = ["gatunek", "samce", "samice", "nosex"]
        
        super().__init__(kolekcja, klucze, user, values)
        
    def print_values(self):
        
        return super().print_values()   
    
    
#a = Okaz("Poecilotheria metalica")