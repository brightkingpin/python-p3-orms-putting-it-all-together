import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None  # Initialize id as None
        self.name = name
        self.breed = breed
    
    @staticmethod
    def create_table():
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @staticmethod
    def drop_table():
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid  # Set the id attribute after insertion
        CONN.commit()
    
    @staticmethod
    def create(name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @staticmethod
    def new_from_db(row):
        id, name, breed = row
        dog = Dog(name, breed)
        dog.id = id
        return dog
    
    @staticmethod
    def get_all():
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dog = Dog.new_from_db(row)
            dogs.append(dog)
        return dogs
    
    @staticmethod
    def find_by_name(name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return Dog.new_from_db(row)
        return None
    
    @staticmethod
    def find_by_id(id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return Dog.new_from_db(row)
        return None
    
    @staticmethod
    def find_or_create_by(name, breed):
        dog = Dog.find_by_name(name)
        if dog:
            return dog
        return Dog.create(name, breed)
    
    def update(self):
        if self.id is None:
            return  # Dog instance has no id, cannot update
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
