####################################################################
# Name - Budh Parkash
# ID   - C0966035
# Project - BookWise: Library Management System with GUI and Database
#####################################################################

# ============== DATABASE.PY ==============
# This file handles all SQLite database operations
# ===========================================

import sqlite3
from classes import Member, Book

class Database:
    """Database class to handle all SQLite operations"""
    
    def __init__(self, db_name="library.db"):
        """Constructor - creates database connection and tables"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def commit(self):
        """Commit changes to the database"""
        if self.conn:
            self.conn.commit()
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        
        books_table = """
        CREATE TABLE IF NOT EXISTS books (
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_available INTEGER DEFAULT 1
        )
        """
        
        members_table = """
        CREATE TABLE IF NOT EXISTS members (
            member_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            books_issued TEXT DEFAULT ''
        )
        """
        
        issued_table = """
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT NOT NULL,
            member_id TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
        """
        
        try:
            self.cursor.execute(books_table)
            self.cursor.execute(members_table)
            self.cursor.execute(issued_table)
            self.commit()
            print("All tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
    
    # ========== BOOK OPERATIONS ==========
    
    def add_book(self, book):
        """Add a new book to the database"""
        try:
            query = "INSERT INTO books (book_id, title, author, is_available) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (book.book_id, book.title, book.author, 1))
            self.commit()
            print(f"Book '{book.title}' added successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return False
    
    def get_all_books(self):
        """Retrieve all books from the database"""
        try:
            self.cursor.execute("SELECT * FROM books ORDER BY title")
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error fetching books: {e}")
            return []
    
    def search_book_by_id(self, book_id):
        """Search for a book by its ID"""
        try:
            self.cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error searching book: {e}")
            return None
    
    def search_book_by_title(self, title):
        """Search for books by title (partial match)"""
        try:
            query = "SELECT * FROM books WHERE title LIKE ?"
            self.cursor.execute(query, (f"%{title}%",))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error searching book: {e}")
            return []
    
    def is_book_available(self, book_id):
        """Check if a book is available for issue"""
        try:
            self.cursor.execute("SELECT is_available FROM books WHERE book_id = ?", (book_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0] == 1
            return False
        except sqlite3.Error as e:
            print(f"Error checking book availability: {e}")
            return False
    
    def update_book_availability(self, book_id, is_available):
        """Update book availability status"""
        try:
            query = "UPDATE books SET is_available = ? WHERE book_id = ?"
            self.cursor.execute(query, (1 if is_available else 0, book_id))
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
            return False
    
    def delete_book(self, book_id):
        """Delete a book from the database"""
        try:
            self.cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting book: {e}")
            return False
    
    # ========== MEMBER OPERATIONS ==========
    
    def add_member(self, member):
        """Add a new member to the database"""
        try:
            books_str = ",".join(member.books_issued) if member.books_issued else ""
            query = "INSERT INTO members (member_id, name, phone, books_issued) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (member.member_id, member.name, member.phone, books_str))
            self.commit()
            print(f"Member '{member.name}' added successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error adding member: {e}")
            return False
    
    def get_all_members(self):
        """Retrieve all members from the database"""
        try:
            self.cursor.execute("SELECT * FROM members ORDER BY name")
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error fetching members: {e}")
            return []
    
    def search_member_by_id(self, member_id):
        """Search for a member by ID"""
        try:
            self.cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error searching member: {e}")
            return None
    
    def search_member_by_name(self, name):
        """Search for members by name (partial match)"""
        try:
            query = "SELECT * FROM members WHERE name LIKE ?"
            self.cursor.execute(query, (f"%{name}%",))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error searching member: {e}")
            return []
    
    def update_member_books(self, member_id, books_list):
        """Update the books_issued list for a member"""
        try:
            books_str = ",".join(books_list) if books_list else ""
            query = "UPDATE members SET books_issued = ? WHERE member_id = ?"
            self.cursor.execute(query, (books_str, member_id))
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating member: {e}")
            return False
    
    def delete_member(self, member_id):
        """Delete a member from the database"""
        try:
            self.cursor.execute("DELETE FROM members WHERE member_id = ?", (member_id,))
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting member: {e}")
            return False
    
    # ========== ISSUE/RETURN OPERATIONS ==========
    
    def issue_book_to_member(self, book_id, member_id, issue_date):
        """Issue a book to a member - WITH SPECIFIC ERROR MESSAGES"""
        try:
          # Step 1: Check if book exists
          self.cursor.execute("SELECT title, is_available FROM books WHERE book_id = ?", (book_id,))
          book_result = self.cursor.fetchone()
        
          if not book_result:
            print(f"Error: Book ID '{book_id}' does not exist")
            return False, "Book ID does not exist"
        
          book_title, is_available = book_result
        
          # Step 2: Check if book is available
          if is_available == 0:
            print(f"Error: Book '{book_title}' (ID: {book_id}) is already issued")
            return False, f"Book '{book_title}' is already issued to someone else"
        
          # Step 3: Check if member exists
          self.cursor.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
          member_result = self.cursor.fetchone()
        
          if not member_result:
             print(f"Error: Member ID '{member_id}' does not exist")
             return False, "Member ID does not exist"
        
          member_name = member_result[0]
        
          # Step 4: Insert into issued_books table
          query = "INSERT INTO issued_books (book_id, member_id, issue_date) VALUES (?, ?, ?)"
          self.cursor.execute(query, (book_id, member_id, issue_date))
        
          # Step 5: Update book availability to False (issued)
          self.update_book_availability(book_id, False)
        
          # Step 6: Update member's books_issued list
          self.cursor.execute("SELECT books_issued FROM members WHERE member_id = ?", (member_id,))
          result = self.cursor.fetchone()
        
          current_books = result[0] if result and result[0] else ""
        
          if current_books:
            new_books_list = current_books + "," + book_id
          else:
             new_books_list = book_id
        
          self.cursor.execute("UPDATE members SET books_issued = ? WHERE member_id = ?", 
                    (new_books_list, member_id))
        
          self.commit()
          print(f"Success: Book {book_id} issued to {member_name}")
          return True, f"Book '{book_title}' issued to {member_name}"
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False, f"Database error: {e}"
    
    def return_book(self, book_id, return_date):
        """Return a book to the library"""
        try:
            # Step 1: Get member_id for this book
            self.cursor.execute("SELECT member_id FROM issued_books WHERE book_id = ? AND return_date IS NULL", (book_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"Book {book_id} is not issued to anyone")
                return False
            
            member_id = result[0]
            
            # Step 2: Update return date in issued_books table
            query = "UPDATE issued_books SET return_date = ? WHERE book_id = ? AND return_date IS NULL"
            self.cursor.execute(query, (return_date, book_id))
            
            # Step 3: Update book availability to True (available)
            self.update_book_availability(book_id, True)
            
            # Step 4: Get current books_issued list for the member
            self.cursor.execute("SELECT books_issued FROM members WHERE member_id = ?", (member_id,))
            member_result = self.cursor.fetchone()
            
            current_books = member_result[0] if member_result and member_result[0] else ""
            
            # Step 5: Remove book from the list
            if current_books:
                books_list = current_books.split(',')
                if book_id in books_list:
                    books_list.remove(book_id)
                new_books_list = ','.join(books_list) if books_list else ""
            else:
                new_books_list = ""
            
            # Step 6: Update member's books_issued list
            self.cursor.execute("UPDATE members SET books_issued = ? WHERE member_id = ?", 
                               (new_books_list, member_id))
            
            self.commit()
            print(f"Book {book_id} returned successfully by {member_id}")
            return True
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")
            return False
    
    def get_issued_books(self):
        """Get all currently issued books"""
        try:
            query = """
            SELECT ib.issue_id, b.title, m.name, ib.issue_date 
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.book_id
            JOIN members m ON ib.member_id = m.member_id
            WHERE ib.return_date IS NULL
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error fetching issued books: {e}")
            return []