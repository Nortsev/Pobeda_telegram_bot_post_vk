"""SQLite3 library"""
import sqlite3
import shutil
import os


class SQLApi:
    """"SQLite3 class"""
    CREATE_SQL = """ CREATE TABLE IF NOT EXISTS top_items(
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              retrieved_time DATE DEFAULT (datetime('now','localtime')),
                              title TEXT NOT NULL,
                              price TEXT NOT NULL,
                              url TEXT NOT NULL,
                              url_photo TEXT NOT NULL,
                              photo BLOB NOT NULL);
                """
    CREATE_TABLE_FILIAL = """ CREATE TABLE IF NOT EXISTS filial(
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              retrieved_time DATE DEFAULT (datetime('now','localtime')),
                              sity TEXT NOT NULL,
                              filial TEXT NOT NULL,
                              categories TEXT NOT NULL,
                              url TEXT NOT NULL
                              );
                """
    INSERT_ITEMS_SQL = """INSERT INTO top_items(title,price,url,url_photo,photo)
                          VALUES(?, ?, ?, ?, ?)
                       """
    DELETE_SQL = """DELETE FROM top_items
                    WHERE id > 20
                 """
    TOP_ITEMS_SQL = """SELECT title , price , photo , url
                       FROM top_items
                       ORDER BY retrieved_time DESC LIMIT {img_count}
                    """
    DATABASE = 'post_vk.db'
    IMAGE_DIR = 'img'
    GET_URLS = "SELECT url FROM filial f WHERE sity = ? AND  filial = ? AND categories = ?"

    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        """Create connection to database"""
        conn = None
        try:
            conn = sqlite3.connect(self.DATABASE)
            cur = conn.cursor()
            cur.execute(self.CREATE_SQL)
            cur.execute(self.CREATE_TABLE_FILIAL)
        except Exception as e:
            print(f'ERROR: {e}')
        return conn

    def get_url(self, sity, filials, categoriess):
        conn = self.conn.cursor()
        urls = conn.execute(self.GET_URLS, (sity, filials, categoriess)).fetchone()
        return urls[0]

    def insert_products(self, products: list) -> bool:
        """Insert a list of products to database"""
        try:
            cur = self.conn.cursor()
            for product in products:
                cur.execute(self.INSERT_ITEMS_SQL, list(product.values()))
                self.conn.commit()
        except Exception as e:
            print(f'ERROR: {e}')
            return False
        return True

    def delete_base(self) -> None:
        """Delete last info in database"""
        try:
            cur = self.conn.cursor()
            cur.execute(self.DELETE_SQL)
            print("ok")
        except Exception as e:
            print('error delete base')

    def get_images(self, img_count=5) -> dict:
        """SELECT 5 most recent items"""
        result = []
        if os.path.exists(self.IMAGE_DIR):
            shutil.rmtree(self.IMAGE_DIR)

        os.mkdir(self.IMAGE_DIR)
        cur = self.conn.cursor()
        image_name = 1
        products_info = cur.execute(self.TOP_ITEMS_SQL.format(img_count=img_count))
        for product in products_info:
            image_path = f'{self.IMAGE_DIR}/{image_name}.jpg'
            write_image(image_path, product[2])
            result.append({'title': product[0],
                           'price': product[1],
                           'image': image_path,
                           'url': product[3]})
            image_name += 1
            print(type(result))
        return result


def write_image(file_name, img) -> bool:
    """Save image to jpg file"""
    try:
        with open(file_name, "wb") as f:
            f.write(img)
    except IOError as error:
        print(error)
        return False
    return True
