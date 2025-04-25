import json

class JS_file:
    def __init__(self, file):
        self.file = file
        with open(self.file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.database = None
        self.collection = None
        
    def start(self):
        if self.database not in self.data:
            self.data[self.database] = {}
        if self.collection not in self.data[self.database]:
            self.data[self.database][self.collection] = []
                
    def find(self, data, option):
        
        if option == "all" and not data:
            return self.data[self.database][self.collection]
        
        data_file = [datas for datas in self.data[self.database][self.collection] for k, v in data.items() if datas[k] == v]
        if not data_file:
            return None
        
        if option == "one":
            data_find = data_file[0]
        elif option == "all":
            data_find = data_file
        return data_find
    
    def delete(self, data, option):

        data_file = [datas for datas in self.data[self.database][self.collection] for k, v in data.items() if datas[k] == v]
        if option == "one":
            self.data[self.database][self.collection].remove(data_file[0])
        elif option == "all":
            if not data:
                self.data[self.database][self.collection].clear()
            else:
                for x in data_file:
                    self.data[self.database][self.collection].remove(x)
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        return
        

    def insert(self, data):
        self.data[self.database][self.collection].append(data)
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def delete_collection(self, collection):

        databases = self.data[self.database]
        if collection in databases:
            del databases[collection]
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        else:
            return 
        
    def delete_database(self, database):

        if database in self.data:
            del self.data[database]
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        else:
            return 
    
    def update(self, data, new_data, option):
        for datas in self.data[self.database][self.collection]:
            if all(datas[k] == v for k, v in data.items()):
                for k, v in new_data.items():
                    datas[k] = v
                    with open(self.file, "w", encoding="utf-8") as f:
                        json.dump(self.data, f, ensure_ascii=False, indent=2)
                if option == "one":
                    break
                elif option == "all":
                    pass
        return
    
    def get_database(self):
        
        return [x for x in self.data]
    
    def get_collection(self):
        
        return [x for x in self.data[self.database]]