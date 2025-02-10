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
            
            for file in os.listdir(path):
                
                if file.endswith(".json"):
                    
                    with open(os.path.join(self.path, file), 'r', encoding="utf-8") as f:
                        doc = json.load(f)
                        self._clean_doc(doc)
                        files.append(doc)
                        
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
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            col.insert_many(self.files)
            
class GatunekAdder(DocsAdder):
    
    def __init__(self, path, many=False):
        
        collection="Gatunki"
        super().__init__(path, collection, many)    
        pprint(self.files)
        
    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        # Trzeba sprawdzić, czy gatunek już istnieje w bazie
        juz_istnieja = {}
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            to_pop =[]
            for i in range(len(self.files)):
                
                count = col.count_documents({"gatunek_lac":self.files[i]["gatunek_lac"]})
                
                if count > 0:
                    
                    juz_istnieja[self.files[i]["gatunek_lac"]] = self.files[i] 
                    to_pop.append(i)
                    
            for i in to_pop:
                
                self.files.pop(i)
                map(lambda x: x-1, to_pop)
                    
        print("Poniższe gatunki nie zostały dodane ze względu na fakt, że karty tych gatunków istnieją już w bazie:")

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
            
            
adder = GatunekAdder(path="/home/marcinpielwski/MongoDB/MongoDB_terraristic/gat", many=True)

adder.add_to_db()