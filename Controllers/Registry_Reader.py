import sqlite3
import os


class Registry_Reader():
    
    def __init__(self):
        pass
        
    def ReadRegistry(self):
        self.CONTEXT_REGISTRY = {}
        registry = self.ReadDB(self.REGISTRY_DB_FILENAME, "All_Logs")        
        for record in registry:
            self.CONTEXT_REGISTRY[record[0]] = {}
            self.CONTEXT_REGISTRY[record[0]]["Filename"] = record[1]
            self.CONTEXT_REGISTRY[record[0]]["Name"] = record[2]
            self.CONTEXT_REGISTRY[record[0]]["Template"] = record[3]