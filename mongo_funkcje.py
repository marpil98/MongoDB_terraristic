from pprint import pprint

import pymongo
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from nltk.metrics.distance import edit_distance

import sys
sys.path.insert(1, "MongoDB_terraristic")
from documents import Document, Owad, Pajeczak, Gatunek

db='hodowla'
uri="mongodb://localhost:27017/"


def creating_collection(db_name:str="hodowla", uri:str="mongodb://localhost:27017/"):
    
    """Creating collection in existance db
    
    
    Parameters
    ----------
    collection_name : str
        New collection's name
    db_name : str, optional
        Dtabase's name, where will be created new collection, by default "hodowla"
    uri : _type_, optional
        uri to mongo server, by default "mongodb://localhost:27017/"

    Raises
    ------
    Exception
        Alternative error info
    """
    print(__name__)
    try:
        collection_name = input("Podaj nazwę nowej kolekcji")
        
        with MongoClient(uri) as client:
                
            database = client[db_name]
            names = database.list_collection_names()
            database.create_collection(name=collection_name)
            print(f'Kolekcja "{collection_name}" została utworzona w bazie "{db_name}"')
        
        
        print('Zamknięto połączenie')
        
    
    except CollectionInvalid:
        
        print(names)
        
        if collection_name in names:
            
            def _exit(message="Kolekcja o podanejnazwi już istnieje."):
                
                print(message)
                new = input("Czy chcesz podać nazwę nowej kolekcji? (y/n)")
            
                if new == 'y':
                    
                    creating_collection()
                    
                elif new =='n':
                    
                    print("Do widzenia")
                    
                else:
                    
                    _exit("Nie rozpoznano polecenia")
        
            _exit()
        
        else:
            
            raise
                
        
    except Exception as e:
        
        raise Exception(
            f"Pojawił się wyjątek: {e}"
        )


def drop_collection(collection_name, db_name="hodowla", uri="mongodb://localhost:27017/"):
    
    """Dropping existance colletion

    Parameters
    ----------
    collection_name : str
        Collection's name which user want to drop
    db_name : str, optional
        Name of db where should be collection to drop, by default "hodowla"
    uri : str, optional
        URI to mongo, by default "mongodb://localhost:27017/"
    """
    
    print("dropping")
    success = 1
    
    with MongoClient(uri) as client:
                
            database = client[db_name]
            names = database.list_collection_names()
            
            if collection_name in names:
                
                database.drop_collection(collection_name)
                print(f"Poprawnie usunięto kolekcję '{collection_name}'")
                
            else:
                
                success = 0
                
    if not success:
        
        def _exit():
            
            print(f"Nie odnaleziono podanej kolekcji. Czy miałeś na myśli którąś z wymienionych: {names}")
            return input("Jeśli tak, podaj poprawną nazwę. W innym, wpisz 'q': ")
        
        exit = _exit()
        check_name = lambda x: x in names
        
        print(exit)
        
        match exit:
            
            case 'q':
                
                print("Do widzenia")
                
            case exit if check_name(exit):
                
                drop_collection(exit)
                
            case _:
                
                _exit()
                
                
        
            
            
            
def prepare_new_docs():
    
    """Preparing new documents, which will added to db

    Returns
    -------
    Document
        Object from class document, whch will be added to db
    """
    
    a = input("Czesc, podaj, jaki typ zwierzaka się pojawił w hodowli (pajeczak/owad/inny): ")
    
    def _transforming_input(inp):
        
        """Helping function which transform input to knowing form, or force the user to 
        give corect name of collection

        Parameters
        ----------
        inp : str
            Name of collection

        Returns
        -------
        str
            "Normalized" name
        """
        
        inp = inp.lower().replace('ą','a').replace('ę','e')
        
        if inp == 'inne':
            
            inp = 'inny'
            
        print(edit_distance(inp, "inny"))
        
        if edit_distance(inp, "pajeczak")<=2:

            inp = "pajeczak"
        
        elif edit_distance(inp, "owad")<=2:

            inp = "owad"
            
        elif edit_distance(inp, "inny")<=2:

            inp = "inny"
            
        else:
            
            print("Nie rozpoznano kolekcji.")
            inp = input("Podaj ją jeszcze raz: ")
            inp =_transforming_input(inp)
            
            
        return inp   
    
    
    docs = {
        'P':[],
        'O':[],
        'I':[],
        }
    run = 1
    
    while run == 1:
        
        a = _transforming_input(a)    
        
        match a:
            
            case "pajeczak":
                
                docs['P'].append(Pajeczak().pola)
                
            case "owad":
                
                docs['O'].append(Owad().pola)
                
            case "inny":
                
                docs['I'].append(Document().pola)
            
            case _:
                
                print("Nie rozpoznano wartości")
                
                pass
            
        a = input("Jeśli chcesz dodać kolejny dokument wpisz typ zwierzaka. W przeciwnym razie wpisz 'q': ")
        
        if a == 'q':
            
            run = 0
            
    print("Dokumenty, które zostaną dodane do bazy danych:")
    pprint(docs)
    
    return docs
   
                
def add_docs_to_db(docs, db='hodowla', uri="mongodb://localhost:27017/"):
    
    """Adding new documents to collection

    Parameters
    ----------
    docs : list
        List of documents
    db : str, optional
        DB name, by default 'hodowla'
    uri : str, optional
        URI to mongo, by default "mongodb://localhost:27017/"
    """
    
    with MongoClient(uri) as client:
        
        db = client[db]
        pajeczaki = db['pajeczaki']
        owady = db['owady']
        for i in docs.keys():
            
            match i:
                
                case 'P':
                    
                    if len(docs['P'])>0:
                        
                        pajeczaki.insert_many(docs['P'])
                    
                    else:
                        
                        print("Brak pajeczakow do dodania")
                    
                case 'O':
                    
                    if len(docs['O'])>0:
                        
                        owady.insert_many(docs['O'])
                        
                    else:
                        
                        print("Brak owadów do dodania")
                    
                case 'I':
                    
                    def nowa_kolekcja():
                        
                        nowa = input("Czy chcesz utworzyć nową kolekcję? (y/n)")
                        
                        if nowa == 'y':
                            
                            nazwa = input("Podaj nazwę nowej kolekcji")
                            creating_collection(nazwa)
                            new_coll = db[nazwa]
                            new_coll.insert_many(docs['I'])
                        
                        elif nowa == 'n':
                            
                            print("To po cholerę dodajesz te dokumenty? Kończę pracę.")
                            
                        else:
                            
                            print("Nie wiem co chcesz zrobić")
                            nowa_kolekcja()
                            
                    if len(docs['I'])>0:
                        
                        nowa_kolekcja()
                        
                    else:
                        
                        print("Brak innych dokumentów do dodania")
                        
                        
def colections_names(db):
    
    pprint(db.list_collection_names())
 
    
def find(db='hodowla', uri="mongodb://localhost:27017/"):
    
    print("Wybierz nazwę kolekcji z podanych poniżej: ")
    
    with MongoClient(uri) as client:
        
        db = client[db]
        colections_names(db)
        col = input()
        collection = db[col]
        
        query = eval(input("Podaj query wyszukiwania: "))
        
        result = collection.find(query)
        
        for f in result:  
            
            pprint(f)
        

def update_stan(gatunek, plec, stadium, ilosc):
    
    with MongoClient("mongodb://localhost:27017/") as clietn:
        
        stan = clietn['hodowla']["Stan"]
        gat_col = clietn['hodowla']["Gatunek"]
        
        if stan.count_documents({"gatunek":gatunek}) == 0:
            
            dodawanie = input("Tego gatunku nie ma chyba w bazie. Czy chcesz go dodać? (y/n)")
            
            def _dodawnie(dodawanie):
                
                if dodawanie == 'y':
                    
                    gat = Gatunek() # W tym momencie tworzy się również nowy dokument stanu
                    gat_col.insert_one(gat.pola)
                    return 1
                
                elif dodawanie == 'n':
                    
                    print("ok. to nie.")
                    return 0
                    
                else:
                    
                    print("Nie rozpoznano polecenia")
                    dodawanie = input("Czy chcesz dodać ten gatunek do bazy? (y/n)")
                    _dodawnie(dodawanie)
            
            czy_gat_w_db = _dodawnie(dodawanie)
        
        else:
            
            czy_gat_w_db = 1    
                    
        if czy_gat_w_db:
            
            id_gat = gat_col.find_one({"$or" : [{"gat_lac" : gatunek}, {"gat_pl" : gatunek}]})
            
            stan.update_one(
                {"gatunek":id_gat}, 
                    {
                        '$inc' : {
                            '.'.join([plec, stadium]) : ilosc
                            }
                        }
                    )
        else:
            
            return 1
            
            
def choose_action():
    
    
    action = input(
        "1 - Wyszukiwanie.\n \
        2 - Aktualizacja danych \n \
        3 - Stworzenie nowej kolekcji \n \
        4 - Dodanie nowych dokumentów\n \
        5 - Wylinka\n \
        6 - Śmierć\Sprzedaż\n \
        7 - Kupno\Klucie\n \
        8 - Wyjście z bazy\n")
    
    match action:
        
        case "1": find()
        case "2": print("Brak funkcjonalności")
        case "3": creating_collection()
        case "4": 
            
            docs = prepare_new_docs()
            add_docs_to_db(docs)
            
        case "5": 

            gat = input("Podaj gatunek: ")
            print(gat)
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj ilosc: ")
            new_stad = str(int(stad[1:])+ 1)
            
            ret = update_stan(gat, plec, new_stad, il)
            
            if ret is None:
                
                ret = update_stan(gat, plec, stad, -il)
                
            if ret is not None:
                
                print("Coś poszło nei tak, póniej się tym zajmę")
                
                return ret
            # Tutaj pomysł, żeby stworzć pipline zmian - ilość starego stadium zmniejszyć o ilość
            # a nowego zwiększyć (jeśli istnieje - dodać sprawdzenie - poczytać o $push i $pull, update aktualizuje dokument, a nie pole)
            
        case "6":
        
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj poprzednie ilosc: ")
            
            update_stan(gat, plec, stad, -il)
            
        case "7":
        
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj ilosc: ")
            
            update_stan(gat, plec, stad, il)
            
        case "8": return 0
        
        case _: print("Nie zrozumiano polecenia. Spróbuj ponownie")

        
        
if __name__ == "__main__":
    
    print("Witaj oto baza danych hodowli. Podaj numer akcji, jaką chcesz wykonać: ")
        
    flag = 1

    while flag != 0:
        
        flag = choose_action()
        
    print("Dzięki za współpracę. Na razie!")
    