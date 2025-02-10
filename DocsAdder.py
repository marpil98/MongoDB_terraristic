import os 
import json

from pymongo import MongoClient

from documents import Stan 


class DocsAdder():
    
    def __init__(self, path, collection, format, many=False):
        
        self.path = path
        self.collection = collection
        self.format = format  
        self.many = many
        
        if many:
            
            files = []
            
            for file in os.listdir():
                
                if file.endswith(".json"):
                    
                    with open(os.path.join(self.path,".json"), 'r') as file:
                        
                        files.append(json.loads(file))
                    
            self.files = files
            
        else:
            
            with open(self.path, 'r') as file:
                        
                self.files = [json.loads(file)]
            
    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        
        with MongoClient(uri) as client:
            
            col = client[db][self.collection]
            col.insert_many(self.files)
            
class GatunekAdder(DocsAdder):
    
    def __init__(self, path, format, many=False):
        
        collection="Gatunki"
        super().__init__(path, collection, format, many)    

    def add_to_db(self, db='hodowla', uri="mongodb://localhost:27017/"):
        return super().add_to_db(db, uri)
    
class OkazAdder(DocsAdder):
    
    def __init__(self, path, format, many=False):
        
        collection="Okazy"
        super().__init__(path, collection, format, many)  
    
    def _update_stan(self):
        
        for i in self.files:
            
            # Znaleźć nazwę gatunku w pliku
            # Sprawdzić czy już jest stan tego gatunku podany
            # Jeśli tak:
            #   zaktualizować
            # w przeciwnym wypadku:
            #   stworzyć nowy   
               
class StanAdder(DocsAdder):
    
    def __init__(self, path, format, many=False):
        
        collection="Stan"
        super().__init__(path, collection, format, many)
            
            
        
        
        
        