####################################################################
# Name - Budh Parkash
# ID   - C0966035
# Project - BookWise: Library Management System with GUI and Database
#####################################################################

# ============== CLASSES.PY ==============
# This file contains all the classes for the Library Management System
# Concepts used: Classes, Objects, Inheritance, Encapsulation
# =========================================

class Person:
    """BASE CLASS - Contains common attributes for all persons"""
    
    def __init__(self, name, phone):
        """Constructor method - initializes name and phone"""
        self.name = name        # Name of person
        self.phone = phone      # Phone number
    
    
    def display_info(self):
        """Returns basic person information"""
        return f"Name: {self.name}, Phone: {self.phone}"


# ------------------------------------------------

class Member(Person):
    """MEMBER CLASS - Inherits from Person class"""
    """Additional attributes: member_id, books_issued"""
    
    def __init__(self, name, phone, member_id):
        """Call parent class constructor using super()"""
        super().__init__(name, phone)   # Initialize name and phone from Person class
        self.member_id = member_id       # Unique ID for member
        self.books_issued = []           # List to store book IDs issued to this member
    
    def issue_book(self, book_id):
        """Add book to member's issued books list"""
        self.books_issued.append(book_id)
    
    def return_book(self, book_id):
        """Remove book from member's issued books list"""
        if book_id in self.books_issued:
            self.books_issued.remove(book_id)
    
    def display_member_info(self):
        """Display complete member information"""
        return f"Member ID: {self.member_id}, Name: {self.name}, Books: {len(self.books_issued)}"


# ------------------------------------------------

class Librarian(Person):
    """LIBRARIAN CLASS - Inherits from Person class"""
    """Additional attribute: employee_id"""
    
    def __init__(self, name, phone, emp_id):
        """Call parent class constructor using super()"""
        super().__init__(name, phone)
        self.emp_id = emp_id
    
    def display_librarian_info(self):
        """Display librarian information"""
        return f"Employee ID: {self.emp_id}, Name: {self.name}"


# ------------------------------------------------

class Book:
    """BOOK CLASS - Independent class (does not inherit from Person)"""
    
    def __init__(self, book_id, title, author):
        """Constructor method - initializes book details"""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True   # Boolean flag: True = available, False = issued
    
    def display_book_info(self):
        """Returns formatted book information with availability status"""
        status = "Available" if self.is_available else "Issued"
        return f"ID: {self.book_id} | {self.title} by {self.author} [{status}]"