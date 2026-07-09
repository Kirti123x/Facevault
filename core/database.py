import sqlite3
import pickle
from datetime import datetime



DATABASE_NAME = "facevault.db"

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_NAME
        )

        self.create_tables()



    def create_tables(self):

        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS people(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT UNIQUE,

                created_at TEXT
            )
            """
        )



        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS photos(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                path TEXT UNIQUE,

                thumbnail TEXT,

                created_at TEXT
            )
            """
        )



        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS faces(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                photo_id INTEGER,

                person_id INTEGER,

                encoding BLOB,
                thumbnail TEXT,

                FOREIGN KEY(photo_id)
                REFERENCES photos(id),

                FOREIGN KEY(person_id)
                REFERENCES people(id)
            )
            """
        )
        self.connection.commit()



    # ---------------------------
    # PEOPLE
    # ---------------------------


    def add_person(self,name):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO people
                (name,created_at)

                VALUES (?,?)

                """,
                (
                    name,
                    datetime.now().isoformat()
                )
            )


            self.connection.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            return self.get_person_id(name)



    def get_person_id(self, name):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM people
            WHERE name=?

            """,
            (name,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return None




    def get_people(self):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM people
            """
        )

        return cursor.fetchall()


    # ---------------------------
    # PHOTOS
    # ---------------------------


    def add_photo(self, path, thumbnail=None):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO photos
            (path,thumbnail,created_at)
            VALUES (?,?,?)
            """,
            (
                path,
                thumbnail,
                datetime.now().isoformat()
            )
        )
        self.connection.commit()

        cursor.execute(
            """
            SELECT id
            FROM photos
            WHERE path=?
            """,
            (path,)
        )
        return cursor.fetchone()[0]

    def get_photos(self):
        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT *
            FROM photos
            """
        )
        return cursor.fetchall()

    # ---------------------------
    # FACE ENCODINGS
    # ---------------------------


    def add_face(
        self,
        photo_id,
        person_id,
        encoding,
        thumbnail
    ):

        cursor = self.connection.cursor()

        binary_encoding = pickle.dumps(
            encoding
        )

        cursor.execute(
            """
            INSERT INTO faces
            (
                photo_id,
                person_id,
                encoding,
                thumbnail
            )
            VALUES (?,?,?,?)
            """,
            (
                photo_id,
                person_id,
                binary_encoding,
                thumbnail
            )
        )

        self.connection.commit()

    def get_person_faces(self, person_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT encoding
            FROM faces
            WHERE person_id=?
            """,(person_id,)

        )

        rows = cursor.fetchall()

        return [
            pickle.loads(row[0])
            for row in rows
        ]
    
    # ---------------------------
    # GALLERY QUERIES
    # ---------------------------


    def get_person_photos(self, person_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT DISTINCT
                photos.path,
                faces.thumbnail
            FROM faces
            JOIN photos
            ON photos.id = faces.photo_id
            WHERE faces.person_id = ?
            """,
            (person_id,)
        )

        return cursor.fetchall()



    def get_person_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM people
            WHERE name = ?
            """,
            (name,)
        )
        return cursor.fetchone()