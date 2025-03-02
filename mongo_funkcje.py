from pprint import pprint
import logging 
import traceback

import pymongo
from pymongo import MongoClient
from nltk.metrics.distance import edit_distance

import sys
sys.path.insert(1, "MongoDB_terraristic")

from documents import Document, Gatunek, Okaz
from DocsAdder import GatunekAdder, OkazAdder, StanAdder

db='hodowla'
uri="mongodb://localhost:27017/"

CUSTOM_INFO = 25
logging.addLevelName(CUSTOM_INFO, "CUSTOM")
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

handler_file = logging.FileHandler("logs/main.log")
handler_file.setLevel(logging.DEBUG)

formatter_file = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler_file.setFormatter(formatter_file)

handler_stream = logging.StreamHandler()
handler_stream.setLevel(logging.DEBUG)
formatter_stream = logging.Formatter("%(levelname)s: %(message)s")
handler_stream.setFormatter(formatter_stream)

logger.addHandler(handler_stream)
logger.addHandler(handler_file)

def creating_collection(collection_name: str, client: MongoClient, db_name:str="hodowla"):
    
    """Creating collection in existing db
    
    Parameters
    ----------
    collection_name : str
        New collection's name
    client: MongoClient
    db_name : str, optional
        Dtabase's name, where will be created new collection, by default "hodowla"

    Raises
    ------
    Exception
        Alternative error info
    """

    try:
        
        collection_name = input("Podaj nazwę nowej kolekcji")
        names = database.list_collection_names()
        
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
            
            database = client[db_name]
            database.create_collection(name=collection_name)
            print(f'Kolekcja "{collection_name}" została utworzona w bazie "{db_name}"')
        
    except Exception as e:
        
        raise Exception(
            f"Pojawił się wyjątek: {e}"
        )


def drop_collection(collection_name: str, client: MongoClient, db_name="hodowla"):
    
    """Dropping existance colletion

    Parameters
    ----------
    collection_name : str
        Collection's name which user want to drop
    client: MongoClient
    db_name : str, optional
        Name of db where should be collection to drop, by default "hodowla"
    """
    
    print("dropping")
    success = 1
                
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
        Object from class document, which will be added to db
    """
    
    a = input("Czesc, podaj, jaki dokument chcesz dodać (gatunek/okaz): ")
    
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
        
        if edit_distance(inp, "gatunek")<=2:

            inp = "gatunek"
        
        elif edit_distance(inp, "okaz")<=2:

            inp = "okaz"
            
        elif edit_distance(inp, "inny")<=2:

            inp = "inny"
            
        else:
            
            print("Nie rozpoznano kolekcji.")
            inp = input("Podaj ją jeszcze raz: ")
            inp =_transforming_input(inp)
            
            
        return inp   
    
    
    docs = {
        'G':[],
        'O':[],
        'I':[],
        }
    run = 1
    
    while run == 1:
        
        a = _transforming_input(a)    
        
        match a:
            
            case "gatunek":
                
                docs['P'].append(Gatunek().pola)
                
            case "okaz":
                
                docs['O'].append(Okaz().pola)
                
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


def prepare_new_docs_ffile():
    
    """Preparing new documents, which will added to db

    Returns
    -------
    Document
        Object from class document, which will be added to db
    """
    
    a = input("Cześć, podaj, jaki dokument chcesz dodać (gatunek/okaz/stan/inny): ")
    
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
        
        if edit_distance(inp, "gatunek")<=2:

            inp = "gatunek"
        
        elif edit_distance(inp, "stan")<=2:

            inp = "stan"
        
        elif edit_distance(inp, "okaz")<=2:

            inp = "okaz"
            
        else:
            
            print("Nie rozpoznano typu dokumentu. ")
            inp = input("Podaj go jeszcze raz: ")
            inp =_transforming_input(inp)
            
        return inp   
    
    docs = {
        'G':[],
        'O':[],
        'S':[],
        }
            
    a = _transforming_input(a)    
    path = input("Podaj ścieżkę do dokumentu/dokumentów: ")
    
    if path.endswith('.json'):

        many = False
        
    else:
        
        many = True
        
    match a:
        
        case "gatunek":
            
            adder = GatunekAdder(path=path, many=many)
            
        case "okaz":
            
            adder = OkazAdder(path=path, many=many)
            
        case "stan":
            
            adder = StanAdder(path=path, many=many)
        case _:
            
            print("Nie rozpoznano wartości")
            
            pass

    adder.add_to_db()
    
    return docs
                
                
def add_docs_to_db(docs: list, client: MongoClient, db='hodowla'):
    
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

    db = client[db]
    gatunki = db['Gatunki']
    okazy = db['okazy']
    
    for i in docs.keys():
        
        match i:
            
            case 'G':
                
                if len(docs['G'])>0:
                    
                    gatunki.insert_many(docs['G'])
                
                else:
                    
                    print("Brak gatunków do dodania")
                
            case 'O':
                
                if len(docs['O'])>0:
                    
                    okazy.insert_many(docs['O'])
                    
                else:
                    
                    print("Brak okazów do dodania")
                
            case 'I':
                
                def nowa_kolekcja():
                    
                    nowa = input("Czy chcesz utworzyć nową kolekcję? (y/n) ")
                    
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
                        
                if len(docs['I']) > 0:
                    
                    nowa_kolekcja()
                    
                else:
                    
                    print("Brak innych dokumentów do dodania")
                        
                        
def colections_names(db):
    
    pprint(db.list_collection_names())

    
def find(client: MongoClient, db='hodowla'):
    
    print("Wybierz nazwę kolekcji z podanych poniżej: ")
    
    db = client[db]
    colections_names(db)
    col = input()
    collection = db[col]
    
    query = eval(input("Podaj query wyszukiwania: "))
    
    result = collection.find(query)
    
    for f in result:  
        
        pprint(f)
    

def update_stan(gatunek, client: MongoClient, plec: str, stadium: str, ilosc: int):
    
        
    stan = clietn['hodowla']["Stan"]
    gat_col = clietn['hodowla']["Gatunek"]
    
    if stan.count_documents({"gatunek":gatunek}) == 0:
        
        dodawanie = input("Tego gatunku nie ma chyba w bazie. Czy chcesz go dodać? (y/n) ")
        
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
                dodawanie = input("Czy chcesz dodać ten gatunek do bazy? (y/n) ")
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
            
def delete_docs(client, collection, conditions, db='hodowla'):
    
    coll = client[db][collection]
    r = coll.delete_many(conditions)
    return r

def cond_find_gat(gatunek):
    
    cond = {"$or":
        [{"gatunek_lac":gatunek},
        {"gatunek_pl":gatunek}]
    }
    
    return cond


def delete_gat(gatunek, client: MongoClient):
                                    
    res = client['hodowla']['Gatunki'].find({})
                
    cond = cond_find_gat(gatunek)
    result = delete_docs(client=client, collection="Gatunki", conditions=cond)
    result = result.deleted_count

    if result == 0:
        
        # wykaz = []
        
        raise Exception("Nie odnaleziono takiego gatunku Upewnij się że podałeś odpowiednią nazwę i spróbuj jeszcze raz. ")
        
        # for i in res:
            
        #     n=i['gatunek_lac']
        #     print(n)
        #     wykaz.append(n)


def delete_stan(gatunek, client: MongoClient):
    
    try:
        
        gat = client['hodowla']['Gatunki']        
        cond_gat = cond_find_gat(gatunek)
        id_gat = gat.find_one(cond_gat)
        id_gat = id_gat['_id']
        cond_stan = {"gatunek" : id_gat}
        delete_docs(client, "Stan", cond_stan)
            
        print(f"Usunięto stan gatunku {gatunek}")
        
    except:
        
        raise
    
def delete_okaz(imie: str, client: MongoClient):
    
    try:            
        okaz = client['hodowla']['Okazy']
        res = okaz.find({"imię" : imie})
        
        plec = res['plec']
        stadium = res['stadium']
        gatunek = res['gatunek']
        gat = client['hodowla']['Gatunki']
        gatunek = gat.find(cond_find_gat(gatunek))['gatunek_lac']
        
        update_stan(gatunek=gatunek, plec=plec, stadium=stadium, ilosc=-1)
    
    except:
        
        raise
    
def usuwanie_dokumentow(client):
    
    run = 1
            
    while run == 1:
        dokument = input("Jaki dokument chcesz usunąć (gatunek, stan, okaz). Wyjście do menu głównego (q). ")
        dokument = dokument.lower()
        
        match dokument:
            
            case "gatunek":
                
                try:
                    
                    gat = input("Podaj nazwę gatunku")
                    delete_gat(gat, client)
                    
                    run = 0
                        
                except Exception as e:
                    
                    print(f"Pojawił się błąd {e}. \n Spróbuj ponownie")
                    
            case "okaz":
                
                try:
                    
                    imie = input("Podaj imię usuwanego okazu: ")
                    delete_okaz(imie, client)
                    
                    run = 0
                    
                except Exception as e:
                    
                    print(f"Pojawił się błąd {e}. \n Spróbuj ponownie")
                    
            case "stan":
                
                try:
                    
                    gat = input("Podaj nazwę gatunku")
                    delete_stan(gat, client)
                    
                    run = 0
                        
                except Exception as e:
                    
                    print(f"Pojawił się błąd {e}. \n Spróbuj ponownie")
            
            case 'q':
                
                run = 0
                
            case _:
                
                print("Nie rozpoznao polecenia. Spróbuj ponownie")
                    
                    
def choose_action(client):
    
    action = input(
        "\n \
        1 - Wyszukiwanie.\n \
        2 - Aktualizacja danych \n \
        3 - Stworzenie nowej kolekcji \n \
        4 - Dodanie dokumentu z palca\n \
        5 - Dodanie dokumentu z plików\n \
        6 - Wylinka\n \
        7 - Śmierć\Sprzedaż\n \
        8 - Kupno\Klucie\n \
        9 - Usuń dokument\n \
        10 - Wyjście z bazy\n")
    
    match action:
        
        case "1": 
            
            find(client=client)
            
        case "2": 
            
            print("Brak funkcjonalności")
            
        case "3": 
            
            creating_collection(client=client)
            
        case "4": 
            
            docs = prepare_new_docs()
            add_docs_to_db(docs, client)
            
        case "5": 
            
            docs = prepare_new_docs_ffile()
            
        case "6": 
            #TO DO: sprawdzenie, czy gatunek jest w bazie powinno rzucać info od razu, nie dopiero po podaniu reszty informacji

            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj ilosc: ")
            new_stad = str(int(stad[1:])+ 1)
            
            ret = update_stan(gat, client, plec, new_stad, il)
            
            if ret is None:
                
                ret = update_stan(gat, client, plec, stad, -il)
                
            if ret is not None:
                
                print("Coś poszło nie tak, póniej się tym zajmę")
                
                return ret
            # Tutaj pomysł, żeby stworzć pipline zmian - ilość starego stadium zmniejszyć o ilość
            # a nowego zwiększyć (jeśli istnieje - dodać sprawdzenie - poczytać o $push i $pull, update aktualizuje dokument, a nie pole)
            
        case "7":
        
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj poprzednie ilosc: ")
            
            update_stan(gat, client, plec, stad, -il)
            
        case "8":
        
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj ilosc: ")
            
            update_stan(gat, client, plec, stad, il)
            
        case "9": 
            
            usuwanie_dokumentow(client)
            
        case "10": return 0
        
        case _: print("Nie zrozumiano polecenia. Spróbuj ponownie")

        
if __name__ == "__main__":
    
    logger.info("Program uruchomił się")
    print("Witaj oto baza danych hodowli. Podaj numer akcji, jaką chcesz wykonać: ")
        
    flag = 1
    while flag != 0:
        try:
            with MongoClient() as client:
                
                flag = choose_action(client)
                
        except:
            
            logger.error("Pojawił się nieznany bład")
            raise
        
    print("Dzięki za współpracę. Na razie!")
    logger.info("Program zakończył działanie")
    