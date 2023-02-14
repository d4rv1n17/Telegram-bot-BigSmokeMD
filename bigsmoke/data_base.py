import sqlite3

class SQLighter:

    def __init__(self, database):
        #connect to the database and save the connection cursor
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    

    def get_all_info(self):
        #getting menu from database
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'MENU'", ()).fetchall()


    def remove_product(self, id):
        #removing product database
        with self.connection:
            return self.cursor.execute("DELETE FROM 'MENU' WHERE id = ?", (id))


    def update_availability(self, id, availability):
        #updating product's availabilty
        with self.connection:
            return self.cursor.execute("UPDATE `MENU` SET `Availability` = ? WHERE id = ?", (availability, id))


    def update_model_name(self, id, model_name):
        #updating product's name
        with self.connection:
            return self.cursor.execute("UPDATE `MENU` SET `MODEL_NAME` = ? WHERE id = ?", (model_name, id))


    def update_model_flavor(self, id, model_flavor):
        #updating product's flavor
        with self.connection:
            return self.cursor.execute("UPDATE `MENU` SET `FLAVORS` = ? WHERE id = ?", (model_flavor, id))      


    def update_model_price(self, product_price, id):
        #updating product's price
        with self.connection:
            return self.cursor.execute("UPDATE `MENU` SET `PRICE` = ? WHERE id = ?", (product_price, id))


    def add(self, model_name, model_flavor, availability, product_price):
        #adding new model to db
        with self.connection:
            return self.cursor.execute("INSERT INTO 'MENU' ('MODEL_NAME', 'FLAVORS', 'Availability', 'PRICE') VALUES(?,?,?,?)", (model_name, model_flavor, availability, product_price))


    def add_to_cart(self, user_id, data1, data2):
        #adding user's choice to db
        with self.connection:
            return self.cursor.execute("INSERT INTO 'SHOPPING CART' ('USER_ID', 'MODEL', 'FLAVOR') VALUES(?,?,?)", (user_id, data1, data2))
  

    def update_cart(self, user_id, data1, data2):
        #updating cart
        with self.connection:
            return self.cursor.execute("DELETE FROM 'SHOPPING CART' WHERE USER_ID = ? AND MODEL = ? AND FLAVOR = ?", (user_id, data1, data2))


    def del_all_user_cart(self, user_id):
        #deleting all user cart after confirmation
        with self.connection:
            return self.cursor.execute("DELETE FROM 'SHOPPING CART' WHERE USER_ID = ?", (user_id,))


    def get_user_cart(self, user_id):
        #getting user's cart
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'SHOPPING CART' WHERE user_id = ?", (user_id,)).fetchall()

    
    def add_user(self, user_id, name):
        #adding user to db
        with self.connection:
            return self.cursor.execute("INSERT INTO 'USERS' ('USER_ID', 'NAME') VALUES(?,?)", (user_id, name))


    def get_users(self):
        #getting users from db
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'USERS'", ()).fetchall()


    def user_exists(self, user_id):
        #getting user from db
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'USERS' WHERE `user_id` = ?", (user_id,)).fetchall()  
            return bool(len(result))      


    def close(self):
        #closing connection with database
        self.connection.close()