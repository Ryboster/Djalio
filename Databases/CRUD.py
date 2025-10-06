import sqlite3
from colorama import Fore, Back, Style
import hashlib
import os
from Databases.Creators import DatabaseCreationQueries
from Controllers.Registry_Reader import Registry_Reader
from django.shortcuts import redirect

###
### This class defines a range of methods used to interact with Databases
### used in this application.
###
class CRUD(DatabaseCreationQueries, Registry_Reader):
    def __init__(self):
        DatabaseCreationQueries.__init__(self)
        Registry_Reader.__init__(self)
        self.DB_EXTENSION = ".sqlite3"
        self.DATABASES_ROOT_DIR = "Databases"
        self.REGISTRY_DB_FILENAME = "Registry"
        self.CreateRegistry()
        self.ReadRegistry()
        
    def GetRegistry(self):
        self.ReadRegistry()
        return self.CONTEXT_REGISTRY

    def CreateInDB(self, database, table: str, values=(), columns=()):
        self.OpenConnection(database)
        if columns == ():
            secureQuery = f"INSERT INTO {table} VALUES ({self.GetValuesPlaceholder(values)})"
        else:
            # Format columns properly as (col1, col2, ...)
            columns_str = f"({', '.join(columns)})"
            secureQuery = f"INSERT INTO {table} {columns_str} VALUES ({self.GetValuesPlaceholder(values)})"
        
        self.ExecuteSecureQuery(secureQuery, values)
        self.CloseConnection()

    def ReadDB(self, database, table, selection="*", whereColumn=None, whereValue=None):
        self.OpenConnection(database)
        if whereColumn is None:
            self.cursor.execute(f"SELECT {selection} FROM {table}")
            result = self.cursor.fetchall()
        else:
            query = f"SELECT {selection} FROM {table} WHERE {whereColumn} = ?"
            self.cursor.execute(query, (whereValue,))
            result = self.cursor.fetchall()
        self.CloseConnection()
        return result
        
    def UpdateDB(self, database, table: str, columns, whereColumn: str, whereValue, values):
        self.OpenConnection(database)
        set_clause = ", ".join([f"{col} = ?" for col in columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {whereColumn} = ?"
        
        if isinstance(values, tuple):
            values = list(values)
        elif not isinstance(values, list):
            values = [values]
        parameters = values + [whereValue]
        
        self.ExecuteSecureQuery(query, parameters)
        self.CloseConnection()

    def DeleteInDB(self, database, table: str, whereColumn: str, whereValue):
        self.OpenConnection(database)
        query = f"DELETE FROM {table} WHERE {whereColumn} = ?"
        self.ExecuteSecureQuery(query, (whereValue,))
        self.CloseConnection()

    def GetValuesPlaceholder(self, values, placeholder="?"):
        for i in range(0, len(values) - 1):
            placeholder += ",?"
        return placeholder

    def ExecuteSecureQuery(self, query, params=()):
        ''' Handle execution in a safe way '''
        try:
            self.cursor.execute(query, params)
            print(f"attempting query: {query}")
            print(Fore.GREEN + "Secure query successful!" + Style.RESET_ALL)
        except sqlite3.Error as e:
            print(Fore.RED + f"Error while executing the following query: {query}\n{e}" + Style.RESET_ALL)
            return False
        return True
    
    def CreateNewDB(self, filename, name, template):
        print(f"creating {filename}/{name}/{template}")
        open(os.path.join(self.DATABASES_ROOT_DIR, filename) + self.DB_EXTENSION, "a")
        self.OpenConnection(filename)
        self.cursor.executescript(self.DIARY_DB_CREATOR)
        self.CloseConnection()
        self.OpenConnection(self.REGISTRY_DB_FILENAME)
        match template:
            case "Diary":
                print("creating new diary")
                self.cursor.executescript(self.DIARY_DB_CREATOR)
            case "Events":
                pass
            case "Diet":
                pass
        self.CloseConnection()
        self.CreateInDB(self.REGISTRY_DB_FILENAME, "All_Logs", (filename, name, template,), ("Filename", "Name", "Template",))
        

    def CreateRegistry(self):
        open(os.path.join(self.DATABASES_ROOT_DIR, self.REGISTRY_DB_FILENAME) + self.DB_EXTENSION, "a")
        self.OpenConnection(self.REGISTRY_DB_FILENAME)
        self.cursor.executescript(self.REGISTRY_DB_CREATOR)
        self.CloseConnection()

    def OpenConnection(self, db):
        ''' Open database connection '''
        self.connection = sqlite3.connect(os.path.join(self.DATABASES_ROOT_DIR, db + self.DB_EXTENSION))
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.connection.cursor()
    
    def CloseConnection(self):
        ''' Save and close database connection '''
        self.connection.commit()
        self.connection.close()
        
    def ClearContext(self, request):
        response = redirect("/")
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        return response