import sqlite3

class ABook_DB(object):
    """ Manage the SQLite database
    
    Methods:
        __init__() - Connect to the database
        search() - Search the database
        add_entry() - Add an entry
        modify_entry() - Modify an entry
        delete_entry() - Delete an entry
    """
    
    def __init__(self, db_file):
        """ Connect to the database
        
        Arguments:
            self - object - This object
            db_exists - boolean - Specifies if the database exists
        """
        
        # Attempt to connect to the database
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            
        except sqlite3.Error as err:
            # Display an error message and exit
            print("[E] Error connecting to database: {}".format(err))
            exit(1)
            
        # Check if the table contacts exists and create if it doesn't
        self.cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='contacts' """)
        
        if self.cursor.fetchone()[0] == 0:
            # Create the contacts table
            self.cursor.execute("""CREATE TABLE contacts (
                id integer PRIMARY KEY,
                first_name text,
                last_name text,
                dob text,
                home_phone text,
                cell_phone text,
                email text,
                address text
            )""")
                
            self.conn.commit()
        
    def search(self, query):
        """ Search the database based on user query
        
        Arguments:
            self - object - This object
            query - string - The user specified search query
        """
        
        # Determine what field to search and construct the coresponding query
        search_field, query = query.split(":")
        
        if search_field == "name":
            sql_query = """ SELECT * FROM contacts WHERE first_name=? OR last_name=?; """
            query_data = (query, query)
            
        elif search_field == "phone":
            sql_query = """ SELECT * FROM contacts WHERE home_phone=? OR cell_phone=?; """
            query_data = (query, query)
            
        elif search_field == "email":
            sql_query = """ SELECT * FROM contacts WHERE email=?; """
            query_data = (query)
            
        # Execute the search query and return the results
        self.cursor.execute(sql_query, query_data)
        results = self.cursor.fetchall()
        
        return results
        
    def add_entry(self, first_name, last_name, dob, home_phone, cell_phone, email, address):
        """ Add an entry to the database. Arguments should be type checked, and if the user
        did not specify a value it should be Nonetype
        
        Arguments:
            self - object - This object
            first_name - string - Contacts first name
            last_name - string - Contacts last name
            dob - string - Contacts date of birth
            home_phone - string - Contacts home phone
            cell_phone - string - Contacts cell phone
            email - string - Contacts email address
            address - string - Contacts address
        """
        
        # Create the SQL query to insert data and execute
        sql_query = """ INSERT INTO contacts (
            first_name,
            last_name,
            dob,
            home_phone,
            cell_phone,
            email,
            address
        ) VALUES (?,?,?,?,?,?,?)"""
        query_data = (first_name, last_name, dob, home_phone, cell_phone, email, address,)
        
        try:
            self.cursor.execute(sql_query, query_data)
            self.conn.commit()
        except sqlite3.Error as err:
            # Display an error message and exit
            print("[E] Error adding contact: {}".format(err))
            exit(1)
    
    def modify_entry(self, entry_id, first_name, last_name, dob, home_phone, cell_phone, email, address):
        """ Modify an entry
        
        Arguments:
            self - object - This object
            entry_id - integer - The contact to modify
            first_name - string - Contacts first name
            last_name - string - Contacts last name
            dob - string - Contacts date of birth
            home_phone - string - Contacts home phone
            cell_phone - string - Contacts cell phone
            email - string - Contacts email address
            address - string - Contacts address
        """
        
        # Create the query
        sql_query = """ UPDATE contacts SET 
            first_name=?,
            last_name=?,
            dob=?,
            home_phone=?,
            cell_phone=?,
            email=?,
            address=? WHERE id=?; """
        query_data = (first_name, last_name, dob, home_phone, cell_phone, email, address, entry_id)
        
        # Attempt to run the query
        try:
            self.cursor.execute(sql_query, query_data)
            self.conn.commit()
        except sqlite3.Error as err:
            print("[E] Error modifying contact: {}".format(err))
            exit(1)
            
    def delete_entry(self, entry_id):
        """ Delete an entry
        
        Arguments:
            self - object - This object
            entry_id - integer - The contact to delete
        """
        
        # Create tge query
        sql_query = """ DELETE FROM contacts WHERE id=?; """
        query_data = (entry_id,)
        
        # Attempt to run the query
        try:
            self.cursor.execute(sql_query, query_data)
            self.conn.commit()
        except sqlite3.Error as err:
            print("[E] Error deleting contact: {}".format(err))
            exit(1)