import os 
import json

from pymongo import MongoClient

from pprint import pprint

from documents import Stan 


class DocsAdder():
    
    def __init__(self, path, collection, many=False):
        
        self.path = path
        self.collection = collection
        self.many = many
        
        if many:
            
            files = []
            
            for file in os.listdir():
                
                if file.endswith(".json"):
                    
                    with open(os.path.join(self.path,".json"), 'r', encoding="utf-8") as file:
                        f = json.load(file)
                        files.append(f)
                    
            self.files = files
            
        else:
            
            with open(self.path, 'r', encoding="utf-8") as file:
                
                f = json.load(file)
                pprint(f)
                self.files = [f]
            
    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            col.insert_many(self.files)
            
class GatunekAdder(DocsAdder):
    
    def __init__(self, path, many=False):
        
        collection="Gatunki"
        super().__init__(path, collection, many)    

    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        # Trzeba sprawdzić, czy gatunek już istnieje w bazie
        juz_istnieja = {}
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            for i in range(len(self.files)):
                
                count = col.count_documents({"gatunek_lac":self.files[i]["gatunek_lac"]})
                
                if count > 0:
                    
                    juz_istnieja[self.files[i]["gatunek_lac"]] = self.files[i] 
                    self.files.pop(i)
                    
        print("Poniższe gatunki nie zostały dodane ze względu na fakt, że karty tych gatunków istnieją już w bazie:")
        pprint(juz_istnieja)
        for i in juz_istnieja.keys():
            
            print(f"\t{i}")  
        
        if len(self.files) > 0:
            
            return super().add_to_db(db, uri)
    
class OkazAdder(DocsAdder):
    
    def __init__(self, path, many=False):
        
        collection="Okazy"
        super().__init__(path, collection, many)  
    
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
    
    def __init__(self, path, format, many=False):
        
        collection="Stan"
        super().__init__(path, collection, format, many)
            
            
adder = GatunekAdder(path="/home/marcinpielwski/MongoDB/MongoDB_terraristic/gtaunek_test.json")

adder.add_to_db()