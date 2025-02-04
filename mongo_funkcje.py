from nltk.metrics.distance import edit_distance
import pymongo
from pymongo import MongoClient
from pprint import pprint
from documents import Document, Owad, Pajeczak


def creating_collection(collection_name:str, db_name:str="hodowla", uri:str="mongodb://localhost:27017/"):
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
    try:
    
        with MongoClient(uri) as client:
                
            database = client[db_name]
            database.create_collection(name=collection_name)
            
            print(f'Kolekcja "{collection_name}" została utworzona w bazie "{db_name}"')
        
        
        print('Zamknięto połączenie')
        
    except Exception as e:
        
        raise Exception(
            f"Pojawił się wyjątek: {e}"
        )


def drop_collection(collection_name, db_name="hodowla", uri="mongodb://localhost:27017/"):
    
    with MongoClient(uri) as client:
                
            database = client[db_name]
            database.drop_collection(name=collection_name)
            
            print(f'The "{collection_name}" was dropped from data base "{db_name}"')
            
            
def prepare_new_docs():
    
    a = input("Czesc, podaj, jaki typ zwierzaka się pojawił w hodowli (pajeczak/owad/inny): ")
    
    def _transforming_input(inp):
        
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
            
            print("Nie rozpoznano patternu.")
            inp = input("Podaj go jeszcze raz: ")
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
                    
docs = prepare_new_docs()

try:
    
    add_docs_to_db(docs)
    
except Exception as e:
    
    print("Coś poszło nie tak")
    print(f"Błąd: {e}")