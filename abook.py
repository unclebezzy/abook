#!/usr/bin/python3

"""
ABook

A simple, searchable CLI address book written in
Python 3. Utilizes a SQLite database to store contacts.
"""

# Imports
import os
import sys
import getopt
import sqlite3
from lib.abook_db import ABook_DB

def main(argv):
    """ Process command line arguments and control
    program flow
    
    Arguments:
        argv - list - Command line arguments that were passed
    """
    
    # Attempt to process command line arguments
    try:
        opts, args = getopt.getopt(argv, "hvs:a:m:d:", ("help", "version", "search=", "add=", "modify=", "delete="))
    except getopt.GetoptError as err:
        # Display an error message and exit
        print("[E] Error processing arguments: {}!".format(err))
        exit(1)
        
    # Set default values
    action = None
    query = None
    new_entry = None
    entry_id = None
        
    # Process arguments individually
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display the help message and exit
            print("USAGE:")
            print("\t{} [-h] [-v] [-s FIELD:QUERY] [-a FIRST NAME] [-m ID] [-d ID]".format(sys.argv[0]))
            print("")
            print("A simple CLI based address book software")
            print("")
            print("ARGUMENTS")
            print("\t-h, --help\tDisplay the help message")
            print("\t-v, --version\tDisplay the version message")
            print("\t-s, --search FIELD:QUERY\tSearch the address book")
            print("\t\tFIELD can be name, phone, or email")
            print("\t-a, --add FIRST NAME\tAdd an entry to the address book")
            print("\t-m, --modify ID\tModify an entry based on their entry number")
            print("\t-d, --delete ID\tDelete an entry based on their entry number")
            exit(0)
            
        elif opt in ("-v", "--version"):
            # Display the version message and exit
            print("ABook")
            print("Version 0.2")
            print("By Uncle Bezzy")
            exit(0)
            
        elif opt in ("-s", "--search"):
            action = "search"
            query = arg
            
        elif opt in ("-a", "--add"):
            action = "add"
            new_entry = arg
            
        elif opt in ("-m", "--modify"):
            action = "modify"
            entry_id = int(arg)
            
        elif opt in ("-d", "--delete"):
            action = "delete"
            entry_id = int(arg)
            
    # Specify the database file
    db_file = "rsc/abook.db"
            
    # Connect to the database
    db_handler = ABook_DB(db_file)
    
    # Search the database
    if action == "search":
        search_result = db_handler.search(query)
        
        # Display the results nicely
        try:
            result_tuple = search_result[0]
            print("Contact ID: {}".format(result_tuple[0]))
            print("First Name: {}".format(result_tuple[1]))
            print("Last Name: {}".format(result_tuple[2]))
            print("Date of Birth: {}".format(result_tuple[3]))
            print("Home Phone: {}".format(result_tuple[4]))
            print("Cell Phone: {}".format(result_tuple[5]))
            print("Email: {}".format(result_tuple[6]))
            print("Address: {}".format(result_tuple[7]))
        except:
            print("Contact not found")
        
    # Add a contact
    elif action == "add":
        first_name = new_entry
        last_name = input("Last Name: ")
        dob = input("Date of Birth: ")
        home_phone = input("Home Phone: ")
        cell_phone = input("Cell Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        
        db_handler.add_entry(first_name, last_name, dob, home_phone, cell_phone, email, address)
        print("Added contact {0} {1}".format(first_name, last_name))
        
    # Modify a contact
    elif action == "modify":
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        dob = input("Date of Birth: ")
        home_phone = input("Home Phone: ")
        cell_phone = input("Cell Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        
        db_handler.modify_entry(entry_id, first_name, last_name, dob, home_phone, cell_phone, email, address)
        print("Modified contact {0} {1}".format(first_name, last_name))
        
    elif action == "delete":
        db_handler.delete_entry(entry_id)
        print("Deleted contact")
        
# Run the script
if __name__ == "__main__":
    main(sys.argv[1:])