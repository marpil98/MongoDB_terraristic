import time

from loggers import main_logger
from collections_fun import find, creating_collection, update_stan
from documents_fun import prepare_new_docs, add_docs_to_db, prepare_new_docs_ffile
from documents_fun import usuwanie_dokumentow

m_log = main_logger()

def choose_action():
    
    action = input(
        "\n \
        1 - Wyszukiwanie.\n \
        2 - Aktualizacja danych \n \
        3 - Stworzenie nowej kolekcji \n \
        4 - Dodanie dokumentu z palca\n \
        5 - Dodanie dokumentu z plików\n \
        6 - Wylinka\n \
        7 - Śmierć\\Sprzedaż\n \
        8 - Kupno\\Klucie\n \
        9 - Usuń dokument\n \
        'q' - Wyjście z bazy\n")
    
    match action:
        
        case "1": 
            
            m_log.info("Wyszukiwanie")
            find()
            return 1
        
        case "2": 
            
            m_log.info("Aktualizacja danych")
            print("Brak funkcjonalności")
            
        case "3": 
            
            m_log.info("Stworzenie nowej kolekcji")
            creating_collection()
            
        case "4": 
            
            m_log.info("Dodanie dokumentu z palca")
            docs = prepare_new_docs()
            
            if docs != 0:
                
                add_docs_to_db(docs)
            
        case "5": 
            
            m_log.info("Dodanie dokumentu z plików")
            docs = prepare_new_docs_ffile()
            
        case "6": 
            #TO DO: sprawdzenie, czy gatunek jest w bazie powinno rzucać info od razu, nie dopiero po podaniu reszty informacji

            m_log.info("Wylinka")
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj ilosc: ")
            new_stad = str(int(stad[1:])+ 1)
            
            ret = update_stan(gat, plec, new_stad, il)
            
            if ret is None:
                
                ret = update_stan(gat, plec, stad, -il)
                
            if ret is not None:
                
                print("Coś poszło nie tak, póniej się tym zajmę")
                
                return ret
            # Tutaj pomysł, żeby stworzć pipline zmian - ilość starego stadium zmniejszyć o ilość
            # a nowego zwiększyć (jeśli istnieje - dodać sprawdzenie - poczytać o $push i $pull, update aktualizuje dokument, a nie pole)
            
        case "7":
        
            m_log.info("Śmierć\\Sprzedaż")
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj poprzednie ilosc: ")
            
            update_stan(gat, plec, stad, -il)
            
        case "8":
        
            m_log.info("Kupno\\Klucie")
            gat = input("Podaj gatunek: ")
            plec = input("Podaj plec: ")
            stad = input("Podaj poprzednie stadium: ")
            il = input("Podaj ilosc: ")
            
            update_stan(gat, plec, stad, il)
            
        case "9": 
            
            m_log.info("Usuń dokument")
            usuwanie_dokumentow()
            
        case "q": 
        
            m_log.info("Wyjście z bazy")
            return 0
        
        case _: print("Nie zrozumiano polecenia. Spróbuj ponownie")
        
if __name__ == "__main__":
    
        
        t0 = time.time()
        m_log.info("Uruchomienie aplikacji")
        print("Witaj oto baza danych hodowli. Podaj numer akcji, jaką chcesz wykonać: ")
            
        flag = 1

        while flag != 0:
            
            try:
                
                flag = choose_action()
            
            except Exception as e:
        
                m_log.error("Wystąpił błąd", exc_info=True)
            
        print("Dzięki za współpracę. Na razie!")
        t1 = time.time()
        t = t1 - t0
        m_log.info(f"Program zakończył działanie w czasie {t//60}min {t%60}s")
    
    
    