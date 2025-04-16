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
                        
def usuwanie_dokumentow():
    
    run = 1
            
    while run == 1:
        dokument = input("Jaki dokument chcesz usunąć (gatunek, stan, okaz). Wyjście do menu głównego (q). ")
        dokument = dokument.lower()
        
        match dokument:
            
            case "gatunek":
                
                try:
                    
                    gat = input("Podaj nazwę gatunku")
                    delete_gat(gat)
                    
                    run = 0
                        
                except Exception as e:
                    
                    print(f"Pojawił się błąd {e}. \n Spróbuj ponownie")
                    
            case "okaz":
                
                try:
                    
                    imie = input("Podaj imię usuwanego okazu: ")
                    delete_okaz(imie)
                    
                    run = 0
                    
                except Exception as e:
                    
                    print(f"Pojawił się błąd {e}. \n Spróbuj ponownie")
                    
            case "stan":
                
                try:
                    
                    gat = input("Podaj nazwę gatunku")
                    delete_stan(gat)
                    
                    run = 0
                        
                except Exception as e:
                    
                    print(f"Pojawił się błąd {e}. \n Spróbuj ponownie")
            
            case 'q':
                
                run = 0
                
            case _:
                
                print("Nie rozpoznao polecenia. Spróbuj ponownie")
                    
   