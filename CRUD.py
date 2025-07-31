import sqlite3
from colorama import Fore, Back, Style
import hashlib
import os

connection = sqlite3.connect("example.sqlite3")

DB_EXTENSION = ".sqlite3"

DATABASES_DICT = {
    "Entries": """
    CREATE TABLE IF NOT EXISTS entries (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Date TEXT NOT NULL CHECK(typeof(Date) = 'text'),
        Mood TEXT NOT NULL CHECK(typeof(Mood) = 'text'),
        Activities TEXT NOT NULL CHECK(typeof(Activities) = 'text'),
        Description TEXT NOT NULL CHECK(typeof(Description) = 'text')
    )
    """,

    "Categories": """
    CREATE TABLE IF NOT EXISTS categories (
        Category TEXT PRIMARY KEY NOT NULL CHECK(typeof(Category) = 'text')
    );

    CREATE TABLE IF NOT EXISTS activities (
        Activity TEXT NOT NULL CHECK(typeof(Activity) = 'text'),
        Color TEXT NOT NULL CHECK(typeof(Color) = 'text'),
        Category TEXT NOT NULL CHECK(typeof(Category) = 'text'),
        FOREIGN KEY (Category) REFERENCES categories(Category)
            ON DELETE CASCADE
    );
    """,

    "Moods": """
    CREATE TABLE IF NOT EXISTS moods (
        Score INTEGER PRIMARY KEY NOT NULL CHECK(typeof(Score) = 'integer'),
        Mood TEXT NOT NULL CHECK(typeof(Mood) = 'text'),
        Color TEXT NOT NULL CHECK(typeof(Color) = 'text')
    )
    """
}

class CRUD():
    def __init__(self):
        self.createDatabases()
        self.initializeDatabases()

    def createDatabases(self):
        for database, _ in DATABASES_DICT.items():
            open(database + DB_EXTENSION, "a")

    def initializeDatabases(self):
        for database, initQuery in DATABASES_DICT.items():
            self.openConnection(database + DB_EXTENSION)
            # Use executescript for multi-statement queries
            self.cursor.executescript(initQuery)
            self.closeConnection()

    def openConnection(self, db):
        ''' Open database connection '''
        self.connection = sqlite3.connect(db)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.connection.cursor()
    
    def closeConnection(self):
        ''' Save and close database connection '''
        self.connection.commit()
        self.connection.close()

    def create(self, database: str, table: str, values=(), columns=()):
        self.openConnection(database + DB_EXTENSION)
        if columns == ():
            secureQuery = f"INSERT INTO {table} VALUES ({self.GetValuesPlaceholder(values)})"
        else:
            # Format columns properly as (col1, col2, ...)
            columns_str = f"({', '.join(columns)})"
            secureQuery = f"INSERT INTO {table} {columns_str} VALUES ({self.GetValuesPlaceholder(values)})"
        
        self.ExecuteSecureQuery(secureQuery, values)
        self.closeConnection()

    def read(self, database: str, table: str):
        self.openConnection(database + DB_EXTENSION)
        self.cursor.execute(f"SELECT * FROM {table}")
        result = self.cursor.fetchall()
        self.closeConnection()
        return result

    def update(self, database: str, table: str, columns, whereColumn: str, whereValue, values):
        self.openConnection(database + DB_EXTENSION)
        set_clause = ", ".join([f"{col} = ?" for col in columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {whereColumn} = ?"
        
        # Fix: Convert values to list if needed, then concatenate
        if isinstance(values, tuple):
            values = list(values)
        elif not isinstance(values, list):
            values = [values]
        
        parameters = values + [whereValue]
        
        self.ExecuteSecureQuery(query, parameters)
        self.closeConnection()

    def delete(self, database: str, table: str, whereColumn: str, whereValue):
        self.openConnection(database + DB_EXTENSION)
        query = f"DELETE FROM {table} WHERE {whereColumn} = ?"
        self.ExecuteSecureQuery(query, (whereValue,))
        self.closeConnection()

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
    
    def generateSessionToken(self):
        randomBytes = os.urandom(32)
        sha256 = hashlib.sha256(randomBytes)
        return sha256.hexdigest()

    def generateHash(self, username: str, password: str):
        combinedBytes = str(username + password).encode("utf-8")
        hashedBytes = hashlib.sha256(combinedBytes)
        return hashedBytes.hexdigest()
    
    def areCredsValid(self, enteredHash):
        allUsers = self.read("users", "Users")
        for username, password, storedHash in allUsers:
            if (enteredHash == storedHash):
                return True
        return False
    
    def isSessionValid(self, request):
        activeSessions = self.read("sessions", "sessions")
        enteredID = request.COOKIES.get("ID")
        enteredSessionToken = request.COOKIES.get("SESH_TOKEN")
        for id, token, time in activeSessions:
            if id == enteredID and enteredSessionToken == token:
                return True
        return False