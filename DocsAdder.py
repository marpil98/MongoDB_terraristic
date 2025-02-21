import os 
import json
import shutil

from pymongo import MongoClient

from pprint import pprint

from documents import Stan 

# Below classes will be using to adding documents from files
class DocsAdder():
    
    def __init__(self, path, collection, many=False):
        
        self.path = path
        self.collection = collection
        self.many = many
        self.filenames = []
        
        if many:
            
            files = []
            
            for file in os.listdir(path):
                
                if file.endswith(".json"):
                    
                    with open(os.path.join(self.path, file), 'r', encoding="utf-8") as f:
                        
                        doc = json.load(f)
                        self._clean_doc(doc)
                        files.append(doc)

                    self.filenames.append(file)    

            self.files = files
            
        else:
            
            with open(self.path, 'r', encoding="utf-8") as f:
                
                self.files = [json.load(f)]
                
    def _clean_doc(self, doc):
        
        keys = list(doc.keys())
        for i in keys:
            
            if doc[i] in ["", " "]:
                
                doc.pop(i)
        
    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        
        try:
            
            with MongoClient(uri) as client:
                
                col = client[db][self.collection]
                col.insert_many(self.files)

            for i in self.filenames:
                
                self._move_file(i)
                
        except Exception as e:
            
            print(e)
            return 0
        
    def _move_file(self, name):
        
        dest_folder = os.path.join(self.path, 'dodane')
                
        if not os.path.exists(dest_folder):
            
            os.mkdir(path=dest_folder)
            
        source = os.path.join(self.path, name)
        dest = os.path.join(dest_folder, name)
        
        shutil.move(source, dest)
        
class GatunekAdder(DocsAdder):
    
    def __init__(self, path, many=False):
        
        collection="Gatunki"
        super().__init__(path, collection, many)    
        
    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        # Trzeba sprawdzić, czy gatunek już istnieje w bazie
        juz_istnieja = {}
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            to_pop = []
            added_names = []
            for i in range(len(self.files)):
                
                name = self.files[i]["gatunek_lac"]
                count = col.count_documents({"gatunek_lac":name})
                
                if (count > 0) or name in added_names:
                    
                    juz_istnieja[self.files[i]["gatunek_lac"]] = self.files[i] 
                    to_pop.append(i)
                    self._move_file(self.filenames[i])
                    
                added_names.append(name)
                    
            for i in range(len(to_pop)):
                
                self.files.pop(to_pop[i])
                
                # Indeksy do usunięcia dodają się po kolei, czyli wcześniejszy indeks jest zawsze mniejszy od następnych.
                # Usunięcie elementu z listy powoduje, że indeksy wszystkich następnych elementów zmniejszają się o 1
                # Wykoanując na raz usunięcie pliku z listy i zmniejszenie o 1 wartości indeksów wszystkich plików do usunięcia,
                # przy iterajcynym przechodzeniu w pętli przez każdy kolejny element listy to_pop (po to jest range(len), a nie po prostu lista)
                # zapewnia usunięcie elementów o odpowiednim indeksie.
                
                to_pop = list(map(lambda x: x-1, to_pop))
                    
        print("Poniższe gatunki nie zostały dodane ze względu na fakt, że karty tych gatunków istnieją już w bazie:")

        for i in juz_istnieja.keys():
            
            print(f"\t{i}")  
        
        if len(self.files) > 0:
            
            return super().add_to_db(db, uri)
    
class OkazAdder(DocsAdder):
    
    def __init__(self, path, many=False):
        
        collection="Okazy"
        
        super().__init__(path, collection, many)  
    
    def _check_gat(file, existance_species=[], nonexistance_species=[], db='hodowla', uri="mongodb://localhost:27017/"):

        
        with MongoClient(uri) as client:
            
            gat = client[db]["Gatunek"]    
            count = gat.count_documents({"gatunek_lac":file["gatunek_lac"]})
            plec = file['plec']
            stadium = file['stadium']
                
                
    def _update_stan(self):
        
        gatunki = []
        
        for i in self.files:
            
            # Znaleźć nazwę gatunku w pliku
            gatunki.append(i['gatunek_lac'])
            # Sprawdzić czy już jest stan tego gatunku podany
            # Jeśli tak:
            #   zaktualizować
            # w przeciwnym wypadku:
            #   stworzyć nowy gatunek
            #   stworzyć nowy stan
            pass
class StanAdder(DocsAdder):
    
    def __init__(self, path, many=False):
        
        collection="Stan"
        
        super().__init__(path, collection, many)  
    
    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        
        juz_istnieja = {}
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            to_pop = []
            added_names = []
            nonexistance_gat = []
            
            for i in range(len(self.files)):
                
                name = self.files[i]["gatunek"]
                gat = client[db]['Gatunki']
                
                count_gat = gat.count_documents({"$or":[{"gatunek_lac":name}, {"gatunek_pl":name}]})
                
                if count_gat != 0:
                    
                    gatunek_id = gat.find_one({"$or":[{"gatunek_lac":name}, {"gatunek_pl":name}]})['_id']
                    count = col.count_documents({"gatunek":gatunek_id})
                    
                    self.files[i]["gatunek"] = gatunek_id
                    
                    if (count > 0) or name in added_names:
                        
                        juz_istnieja[self.files[i]["gatunek"]] = self.files[i] 
                        to_pop.append(i)
                        self._move_file(self.filenames[i])
                        
                    added_names.append(name)
                
                else:
                    
                    nonexistance_gat.append(name)
                    
            for i in range(len(to_pop)):
                
                self.files.pop(to_pop[i])
                
                # Indeksy do usunięcia dodają się po kolei, czyli wcześniejszy indeks jest zawsze mniejszy od następnych.
                # Usunięcie elementu z listy powoduje, że indeksy wszystkich następnych elementów zmniejszają się o 1
                # Wykoanując na raz usunięcie pliku z listy i zmniejszenie o 1 wartości indeksów wszystkich plików do usunięcia,
                # przy iterajcynym przechodzeniu w pętli przez każdy kolejny element listy to_pop (po to jest range(len), a nie po prostu lista)
                # zapewnia usunięcie elementów o odpowiednim indeksie.
                
                to_pop = list(map(lambda x: x-1, to_pop))
        
        if len(added_names) > 0:      
        
            print("Stany poniższych gatunków już są w bazie. Jeśli chcesz je zmienić użyj innej opcji.")

            for i in juz_istnieja.keys():
                
                print(f"\t{i}")  
                
        if len(nonexistance_gat) > 0:      
        
            print('Poniższych gatunków nie ma jeszcze w bazie. Aby dodać ich stany uzupełnij wpierw kolekcję "Gatunki"')

            for i in nonexistance_gat:
                
                print(f"\t{i}")  
                
        if len(self.files) > 0:
                
            return super().add_to_db(db, uri)
                
                
    
class StanActualizer():
    
    def __init__(self, id_gat, count, client, file, quantity):
        
        self.id_gat = id_gat
        self.count = count
        self.client = client
        self.file = file
        self.quantity = quantity
        self.plec = file['płeć']
        self.stadium = file['stadium']
        self._actualization() # Być może ta funkcja nie powinna być wywoływana w tym miejscu, a raczej być publiczną i zostać wywaołana po utworzeniu isntacji klasy
        
    def actualize(self):
        
        if self.count > 0:
                            
            stan = self.client['hodowla']["Stan"]  
            
            if self.count > 0:
                print("Dodać aktualizację stanu")
                # aktualizuj stan
            else:

                values = self._create_vals()
                st = Stan(values)
                self.client['hodowla']['Stan'].insert_one(st.pola)
                
    def _create_vals(self):
        
        match self.plec:
                
            case "samiec":
                
                values = [self.id_gat, {self.stadium : self.quantity}, {}, {}]
                
            case "samica":
                
                values = [self.id_gat, {}, {self.stadium : self.quantity}, {}]
            
            case "nosex":
        
                values = [self.id_gat, {}, {}, {self.stadium : self.quantity}]
            
            case _:
                
                pass  
            
        return values 
    
    def _actualization(self):
        
        values = self._create_vals()
        klucze = ["gatunek", "samce", "samice", "nosex"]
        act_dict = dict(zip(klucze, values))
        act_dict.pop('gatunek')
        print(act_dict)
        good_act_dict = {}
        for i in act_dict:
            
            if len(act_dict[i]) > 0:
                
                for k in act_dict[i]:
                    
                    good_act_dict['.'.join([i,k])] = act_dict[i][k]
        id_gat = self.id_gat
        self.client['hodowla']['Stan'].update_one(
            {"gatunek" : id_gat},
            {"$inc": good_act_dict}
        )

