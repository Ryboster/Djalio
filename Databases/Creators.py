###
### This class stores database "template" creation queries.
### They're used when the user creates a new database (a.k.a. log).
###
class DatabaseCreationQueries:
    def __init__(self):
        
        self.REGISTRY_DB_CREATOR = """
            CREATE TABLE IF NOT EXISTS All_Logs (
                Log_ID INTEGER PRIMARY KEY NOT NULL,
                Filename TEXT NOT NULL CHECK(typeof(Filename) = 'text'),
                Name TEXT NOT NULL CHECK(typeof(Name) = 'text'),
                Template TEXT NOT NULL CHECK(typeof(Template) = 'text')
            );
            """
        
        self.DIARY_DB_CREATOR = """
            CREATE TABLE IF NOT EXISTS All_Categories(
                Category_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Category TEXT NOT NULL CHECK(typeof(Category) = 'text')
            );

            CREATE TABLE IF NOT EXISTS All_Activities (
                Activity_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Category_ID INTEGER NOT NULL,
                Activity TEXT NOT NULL CHECK(typeof(Activity) = 'text'),
                Color TEXT NOT NULL CHECK(typeof(Color) = 'text'),
                FOREIGN KEY (Category_ID) REFERENCES All_Categories(Category_ID)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS All_Moods (
                Mood_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Mood TEXT NOT NULL CHECK(typeof(Mood) = 'text'),
                Score INTEGER NOT NULL CHECK(typeof(Score) = 'integer'),
                Color TEXT NOT NULL CHECK(typeof(Color) = 'text')
            );

            CREATE TABLE IF NOT EXISTS Entries (
                Entry_ID INTEGER PRIMARY KEY NOT NULL,
                Description TEXT NOT NULL CHECK(typeof(Description) = 'text')
            );

            CREATE TABLE IF NOT EXISTS Mood_Records (
                Entry_ID INTEGER NOT NULL CHECK(typeof(Entry_ID) = 'integer'),
                Mood_ID INTEGER,
                FOREIGN KEY (Entry_ID) REFERENCES Entries(Entry_ID)
                    ON DELETE CASCADE,
                FOREIGN KEY (Mood_ID) REFERENCES All_Moods(Mood_ID)
            );

            CREATE TABLE IF NOT EXISTS Activity_Records (
                Entry_ID INTEGER NOT NULL,
                Activity_ID INTEGER NOT NULL,
                FOREIGN KEY (Entry_ID) REFERENCES Entries(ENTRY_ID)
                    ON DELETE CASCADE,
                FOREIGN KEY (Activity_ID) REFERENCES All_Activities(Activity_ID)
                    ON DELETE CASCADE
            );
        """
        
        self.EVENTS_DB_CREATOR = """    
            CREATE TABLE IF NOT EXISTS Groups (
                Group_ID INTEGER PRIMARY KEY NOT NULL,
                Name TEXT NOT NULL CHECK(typeof(Name) = 'text'),
                Color TEXT NOT NULL CHECK(typeof(Color) = 'text')
            );

            CREATE TABLE IF NOT EXISTS Entries (
                Entry_ID INTEGER PRIMARY KEY NOT NULL,
                Description TEXT NOT NULL CHECK(typeof(Description) = 'text'),
                Group_ID INTEGER,
                FOREIGN KEY (Group_ID) REFERENCES Groups(Group_ID)
            );
        """
        
        self.DIET_DB_CREATOR = """
            CREATE TABLE IF NOT EXISTS Entries (
                Entry_ID INTEGER PRIMARY KEY NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Diet_Tags (
                Tag_ID INTEGER PRIMARY KEY NOT NULL,
                Tag TEXT NOT NULL CHECK(typeof(Tag) = 'text'),
                Color TEXT NOT NULL CHECK(typeof(Color) = 'text')
            );

            CREATE TABLE IF NOT EXISTS Nutrition_Records (
                Entry_ID INTEGER NOT NULL CHECK(typeof(Entry_ID) = 'integer'),
                Table TEXT NOT NULL CHECK(typeof(Table) = 'text'),
                FOREIGN KEY (Entry_ID) REFERENCES Entries(Entry_ID)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Tag_Records (
                Entry_ID INTEGER NOT NULL CHECK(typeof(Entry_ID) = 'integer'),
                Tag_ID INTEGER NOT NULL CHECK(typeof(Tag_ID) = 'integer'),
                FOREIGN KEY (Entry_ID) REFERENCES Entries(Entry_ID)
                    ON DELETE CASCADE,
                FOREIGN KEY (Tag_ID) REFERENCES Diet_Tags(Tag_ID)
                    ON DELETE CASCADE
            );
        """