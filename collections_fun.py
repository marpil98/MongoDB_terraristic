import logging
from pprint import pprint

import pymongo
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from nltk.metrics.distance import edit_distance

import sys
sys.path.insert(1, "MongoDB_terraristic")

from documents import Document, Gatunek, Okaz
from DocsAdder import GatunekAdder, OkazAdder, StanAdder
from loggers import db_conn_logger

db='hodowla'
uri="mongodb://localhost:27017/"

conn_loger = db_conn_logger()

def creating_collection(db_name:str="hodowla", uri:str="mongodb://localhost:27017/"):
    
    """Creating collection in existing db
    
    
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
    try:
        collection_name = input("Podaj nazwę nowej kolekcji: ")
        
        if collection_name != 'q':
            
            
            with MongoClient(uri) as client:
                    
                    
                conn_loger.info("Polaczono z baza")
                database = client[db_name]
                names = database.list_collection_names()
                database.create_collection(name=collection_name)
                print(f'Kolekcja "{collection_name}" została utworzona w bazie "{db_name}"')
                
            conn_loger.info("Rozlaczenie bazy")

        
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
                
            conn_loger.info("Polaczono z baza")
            database = client[db_name]
            names = database.list_collection_names()
            
            if collection_name in names:
                
                database.drop_collection(collection_name)
                print(f"Poprawnie usunięto kolekcję '{collection_name}'")
                
            else:
                
                success = 0
    
    conn_loger.info("Rozlaczenie bazy")
            
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
                        
def colections_names(db):
    
    pprint(db.list_collection_names())

    
def find(db='hodowla', uri="mongodb://localhost:27017/"):
    
    print("Wybierz nazwę kolekcji z podanych poniżej: ")
    
    try:
        
        with MongoClient(uri) as client:
            
            conn_loger.info("Polaczono z baza")
            db = client[db]
            colections_names(db)
            col = input()
            
            if col == "q":
                
                print("exit")
                pass
            
            else:
                
                collection = db[col]
                
                query = eval(input("Podaj query wyszukiwania: "))
                    
                result = collection.find(query)
                
                for f in result:  
                    
                    pprint(f)
                    
        conn_loger.info("Rozlaczenie bazy")
        
    except NameError as e: 
        
        print("Podano złą nazwę kolekcji, lub błędne query")
        find()

def update_stan(gatunek, plec, stadium, ilosc):
    
    with MongoClient("mongodb://localhost:27017/") as clietn:
        
        conn_loger.info("Polaczono z baza")
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
    
    conn_loger.info("Rozlaczenie bazy")
    
    
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


def delete_gat(gatunek):
    
    with MongoClient() as client:
                                
        conn_loger.info("Polaczono z baza")
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

    conn_loger.info("Rozlaczenie bazy")
    

def delete_stan(gatunek):
    
    try:
        
        with MongoClient(uri) as client:
            
            conn_loger.info("Polaczono z baza")
            gat = client['hodowla']['Gatunki']
            stan = client['hodowla']['Stan']
            
            cond_gat = cond_find_gat(gatunek)
            
            id_gat = gat.find_one(cond_gat)
            
            id_gat = id_gat['_id']
            
            cond_stan = {"gatunek" : id_gat}
            delete_docs(client, "Stan", cond_stan)
            
        conn_loger.info("Rozlaczenie bazy")
        print(f"Usunięto stan gatunku {gatunek}")
        
    except:
        
        raise
    
def delete_okaz(imie):
    
    try:
        
        with MongoClient(uri) as client:
            
            conn_loger.info("Polaczono z baza")
            okaz = client['hodowla']['Okazy']
            res = okaz.find({"imię" : imie})
            
            plec = res['plec']
            stadium = res['stadium']
            gatunek = res['gatunek']
            gat = client['hodowla']['Gatunki']
            gatunek = gat.find(cond_find_gat(gatunek))['gatunek_lac']
        
        conn_loger.info("Rozlaczenie bazy")
        update_stan(gatunek=gatunek, plec=plec, stadium=stadium, ilosc=-1)
    
    except:
        
        raise
    


        

    