"""SQLite3 library"""
import sqlite3

class SQLApi:
    """"SQLite3 class"""

    CREATE_TABLE_CATEGORIES = """ CREATE TABLE IF NOT EXISTS categories
                                    (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        category_name TEXT NOT NULL UNIQUE
                                    );
                               """

    CREATE_TABLE_CITIES = """ CREATE TABLE IF NOT EXISTS cities
                                (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    city_name TEXT NOT NULL UNIQUE
                                );
                                """

    CREATE_TABLE_STORES = """ CREATE TABLE IF NOT EXISTS stores                               
                                 (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    street_name TEXT NOT NULL UNIQUE,
                                    phone_number TEXT NOT NULL UNIQUE,
                                    city_id INT NOT NULL,
                                    CONSTRAINT fk_cities FOREIGN KEY(city_id) REFERENCES cities(id)
                                  );      
                                 """

    CREATE_TABLE_PRODUCTS = """ CREATE TABLE IF NOT EXISTS products
                                (
                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      retrieved_time DATE DEFAULT (datetime('now','localtime')),
                                      url TEXT NOT NULL,
                                      stores_id INT NOT NULL,
                                      categories_id INT NOT NULL,
                                      CONSTRAINT fk_stores FOREIGN KEY(stores_id) REFERENCES stores(id),
                                      CONSTRAINT fk_categories FOREIGN KEY(categories_id) REFERENCES categories(id)
                                );
                                """

    CREATE_TABLE_USERS = """ CREATE TABLE IF NOT EXISTS users
                                (
                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      username TEXT NOT NULL UNIQUE,
                                      data_post DATE
                                );
                        """
    DATABASE = 'post_vk.db'
    IMAGE_DIR = 'img'
    GET_URLS = "SELECT url FROM products  WHERE stores_id = (SELECT id FROM stores WHERE street_name = ? ) AND categories_id =  (SELECT id FROM categories WHERE category_name = ?)"
    GET_PHONE = "SELECT phone_number FROM stores WHERE street_name = ?"

    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        """Create connection to database"""
        conn = None
        try:
            conn = sqlite3.connect(self.DATABASE)
            cur = conn.cursor()
            cur.execute(self.CREATE_TABLE_CATEGORIES)
            cur.execute(self.CREATE_TABLE_CITIES)
            cur.execute(self.CREATE_TABLE_STORES)
            cur.execute(self.CREATE_TABLE_PRODUCTS)
            cur.execute(self.CREATE_TABLE_USERS)
        except Exception as e:
            print(f'ERROR: {e}')
        return conn

    def get_url(self, filials, categoriess):
        conn = self.conn.cursor()
        urls = conn.execute(self.GET_URLS, (filials, categoriess)).fetchone()
        return urls[0]

    def get_phone(self, filials):
        conn = self.conn.cursor()
        urls = conn.execute(self.GET_PHONE, [filials]).fetchone()
        return urls[0]

    def authorization_user(self, username):
        conn = self.conn.cursor()
        info = conn.execute('SELECT * FROM users WHERE username=?', (username,))
        if info.fetchone() is None:
            return False
        else:
             return True

