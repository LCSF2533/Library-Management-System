####################################################################
# Name - Budh Parkash
# ID   - C0966035
# Project - BookWise: Library Management System with GUI and Database
#####################################################################

# ============== MAIN.PY ==============
# This file contains the GUI for Library Management System
# Concepts used: GUI (tkinter), Event Handling, Loops
# ===========================================



import tkinter as tk
from tkinter import ttk, messagebox
from classes import Member, Book
from database import Database
from datetime import datetime

class LibraryManagementSystem:
    """Main GUI class for Library Management System"""
    
    def __init__(self):
        """Constructor - Creates main window and sets up GUI"""
        self.db = Database()
        self.current_librarian = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("BookWise - Library Management System")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Setup GUI
        self.setup_menu()
        self.setup_main_frame()
        
        # Start the application
        self.root.mainloop()
    
    def setup_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_main_frame(self):
        """Setup the main frame with all sections"""
        # Title
        title_label = tk.Label(self.root, text="BOOKWISE LIBRARY SYSTEM", 
                               font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_books_tab()
        self.create_members_tab()
        self.create_transactions_tab()
        self.create_search_tab()
    
    # ========== BOOKS TAB ==========
    
    def create_books_tab(self):
        """Create the Books tab"""
        books_frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(books_frame, text="Books")
        
        # Add Book Section
        add_frame = tk.LabelFrame(books_frame, text="Add New Book", font=("Arial", 12, "bold"), 
                                   bg='#f9f9f9', fg='#2c3e50', padx=10, pady=10)
        add_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(add_frame, text="Book ID:", bg='#f9f9f9').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.book_id_entry = tk.Entry(add_frame, width=15)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Title:", bg='#f9f9f9').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.book_title_entry = tk.Entry(add_frame, width=25)
        self.book_title_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_frame, text="Author:", bg='#f9f9f9').grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.book_author_entry = tk.Entry(add_frame, width=20)
        self.book_author_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(add_frame, text="Add Book", command=self.add_book, 
                  bg='#27ae60', fg='white', padx=10).grid(row=0, column=6, padx=10, pady=5)
        
        # Books List Section
        list_frame = tk.LabelFrame(books_frame, text="Books List", font=("Arial", 12, "bold"),
                                    bg='#f9f9f9', padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for books
        columns = ('ID', 'Title', 'Author', 'Status')
        self.books_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)
        
        self.books_tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.books_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        btn_frame = tk.Frame(list_frame, bg='#f9f9f9')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh Books", command=self.refresh_books,
                  bg='#3498db', fg='white', padx=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Book", command=self.delete_book,
                  bg='#e74c3c', fg='white', padx=10).pack(side='left', padx=5)
        
        # Refresh books list
        self.refresh_books()
    
    # ========== MEMBERS TAB ==========
    
    def create_members_tab(self):
        """Create the Members tab"""
        members_frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(members_frame, text="Members")
        
        # Add Member Section
        add_frame = tk.LabelFrame(members_frame, text="Add New Member", font=("Arial", 12, "bold"),
                                   bg='#f9f9f9', fg='#2c3e50', padx=10, pady=10)
        add_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(add_frame, text="Member ID:", bg='#f9f9f9').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.member_id_entry = tk.Entry(add_frame, width=15)
        self.member_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Name:", bg='#f9f9f9').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.member_name_entry = tk.Entry(add_frame, width=25)
        self.member_name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_frame, text="Phone:", bg='#f9f9f9').grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.member_phone_entry = tk.Entry(add_frame, width=15)
        self.member_phone_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(add_frame, text="Add Member", command=self.add_member,
                  bg='#27ae60', fg='white', padx=10).grid(row=0, column=6, padx=10, pady=5)
        
        # Members List Section
        list_frame = tk.LabelFrame(members_frame, text="Members List", font=("Arial", 12, "bold"),
                                    bg='#f9f9f9', padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for members
        columns = ('ID', 'Name', 'Phone', 'Books Issued')
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=150)
        
        self.members_tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.members_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        btn_frame = tk.Frame(list_frame, bg='#f9f9f9')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh Members", command=self.refresh_members,
                  bg='#3498db', fg='white', padx=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Member", command=self.delete_member,
                  bg='#e74c3c', fg='white', padx=10).pack(side='left', padx=5)
        
        # Refresh members list
        self.refresh_members()
    
    # ========== TRANSACTIONS TAB ==========
    
    def create_transactions_tab(self):
        """Create the Transactions tab"""
        trans_frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(trans_frame, text="Transactions")
        
        # Issue Book Section
        issue_frame = tk.LabelFrame(trans_frame, text="Issue Book", font=("Arial", 12, "bold"),
                                     bg='#f9f9f9', fg='#2c3e50', padx=10, pady=10)
        issue_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(issue_frame, text="Book ID:", bg='#f9f9f9').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.issue_book_id = tk.Entry(issue_frame, width=15)
        self.issue_book_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(issue_frame, text="Member ID:", bg='#f9f9f9').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.issue_member_id = tk.Entry(issue_frame, width=15)
        self.issue_member_id.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(issue_frame, text="Issue Book", command=self.issue_book,
                  bg='#e67e22', fg='white', padx=10).grid(row=0, column=4, padx=10, pady=5)
        
        # Return Book Section
        return_frame = tk.LabelFrame(trans_frame, text="Return Book", font=("Arial", 12, "bold"),
                                      bg='#f9f9f9', fg='#2c3e50', padx=10, pady=10)
        return_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(return_frame, text="Book ID:", bg='#f9f9f9').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.return_book_id = tk.Entry(return_frame, width=15)
        self.return_book_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(return_frame, text="Return Book", command=self.return_book,
                  bg='#2ecc71', fg='white', padx=10).grid(row=0, column=2, padx=10, pady=5)
        
        # Issued Books List Section
        issued_frame = tk.LabelFrame(trans_frame, text="Currently Issued Books", font=("Arial", 12, "bold"),
                                      bg='#f9f9f9', padx=10, pady=10)
        
        issued_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Issue ID', 'Book Title', 'Member Name', 'Issue Date')
        self.issued_tree = ttk.Treeview(issued_frame, columns=columns, show='headings')
        
        for col in columns:
            self.issued_tree.heading(col, text=col)
            self.issued_tree.column(col, width=180)
        
        self.issued_tree.pack(fill='both', expand=True)
        
        tk.Button(issued_frame, text="Refresh Issued Books", command=self.refresh_issued_books,
                  bg='#3498db', fg='white', padx=10).pack(pady=5)
        
        self.refresh_issued_books()
    
    # ========== SEARCH TAB ==========
    
    def create_search_tab(self):
        """Create the Search tab"""
        search_frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(search_frame, text="Search")
        
        # Search by Title
        title_frame = tk.LabelFrame(search_frame, text="Search Book by Title", font=("Arial", 12, "bold"),
                                     bg='#f9f9f9', padx=10, pady=10)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(title_frame, text="Enter Title:", bg='#f9f9f9').pack(side='left', padx=5)
        self.search_title_entry = tk.Entry(title_frame, width=30)
        self.search_title_entry.pack(side='left', padx=5)
        tk.Button(title_frame, text="Search", command=self.search_book_by_title,
                  bg='#3498db', fg='white', padx=10).pack(side='left', padx=5)
        
        # Search by Member Name
        member_frame = tk.LabelFrame(search_frame, text="Search Member by Name", font=("Arial", 12, "bold"),
                                      bg='#f9f9f9', padx=10, pady=10)
        member_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(member_frame, text="Enter Name:", bg='#f9f9f9').pack(side='left', padx=5)
        self.search_member_entry = tk.Entry(member_frame, width=30)
        self.search_member_entry.pack(side='left', padx=5)
        tk.Button(member_frame, text="Search", command=self.search_member_by_name,
                  bg='#3498db', fg='white', padx=10).pack(side='left', padx=5)
        
        # Search Results
        results_frame = tk.LabelFrame(search_frame, text="Search Results", font=("Arial", 12, "bold"),
                                       bg='#f9f9f9', padx=10, pady=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.search_results_text = tk.Text(results_frame, height=10, width=80)
        self.search_results_text.pack(fill='both', expand=True)
    
    # ========== DATABASE OPERATIONS ==========
    
    def add_book(self):
        """Add a new book to database"""
        book_id = self.book_id_entry.get().strip()
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        
        if not book_id or not title or not author:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        book = Book(book_id, title, author)
        if self.db.add_book(book):
            messagebox.showinfo("Success", f"Book '{title}' added successfully")
            self.book_id_entry.delete(0, tk.END)
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
            self.refresh_books()
        else:
            messagebox.showerror("Error", "Failed to add book. Book ID may already exist.")
    
    def refresh_books(self):
        """Refresh the books list in GUI"""
        # Clear existing items
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Get books from database
        books = self.db.get_all_books()
        
        for book in books:
            book_id, title, author, is_available = book
            status = "Available" if is_available == 1 else "Issued"
            self.books_tree.insert('', 'end', values=(book_id, title, author, status))
    
    def delete_book(self):
        """Delete selected book from database"""
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a book to delete")
            return
        
        book_id = self.books_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete book {book_id}?"):
            if self.db.delete_book(book_id):
                messagebox.showinfo("Success", "Book deleted successfully")
                self.refresh_books()
            else:
                messagebox.showerror("Error", "Failed to delete book")
    
    def add_member(self):
        """Add a new member to database"""
        member_id = self.member_id_entry.get().strip()
        name = self.member_name_entry.get().strip()
        phone = self.member_phone_entry.get().strip()
        
        if not member_id or not name or not phone:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        member = Member(name, phone, member_id)
        if self.db.add_member(member):
            messagebox.showinfo("Success", f"Member '{name}' added successfully")
            self.member_id_entry.delete(0, tk.END)
            self.member_name_entry.delete(0, tk.END)
            self.member_phone_entry.delete(0, tk.END)
            self.refresh_members()
        else:
            messagebox.showerror("Error", "Failed to add member. Member ID may already exist.")
    
    def refresh_members(self):
        """Refresh the members list in GUI"""
        # Clear existing items
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        # Get members from database
        members = self.db.get_all_members()
        
        for member in members:
            member_id, name, phone, books_issued = member
            books_count = len(books_issued.split(',')) if books_issued else 0
            self.members_tree.insert('', 'end', values=(member_id, name, phone, books_count))
    
    def delete_member(self):
        """Delete selected member from database"""
        selected = self.members_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a member to delete")
            return
        
        member_id = self.members_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete member {member_id}?"):
            if self.db.delete_member(member_id):
                messagebox.showinfo("Success", "Member deleted successfully")
                self.refresh_members()
            else:
                messagebox.showerror("Error", "Failed to delete member")
    
    def issue_book(self):
        """Issue a book to a member"""
        book_id = self.issue_book_id.get().strip()
        member_id = self.issue_member_id.get().strip()
    
        if not book_id or not member_id:
           messagebox.showerror("Error", "Please enter both Book ID and Member ID")
           return
    
        # First check if book exists and is available
        book = self.db.search_book_by_id(book_id)
        if not book:
           messagebox.showerror("Error", f"Book ID '{book_id}' does not exist")
           return
    
        # Check if book is available
        if book[3] == 0:  # is_available = 0 means issued
           # Get who has this book
           issued_books = self.db.get_issued_books()
           for issued in issued_books:
             if issued[1] == book[1]:  # Book title match
                messagebox.showerror("Error", f"Book '{book[1]}' (ID: {book_id}) is already issued to another member. Please return it first.")
                return
    
        # Check if member exists
        member = self.db.search_member_by_id(member_id)
        if not member:
           messagebox.showerror("Error", f"Member ID '{member_id}' does not exist")
           return
    
        issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        if self.db.issue_book_to_member(book_id, member_id, issue_date):
           messagebox.showinfo("Success", f"Book {book_id} issued to member {member_id}")
           self.issue_book_id.delete(0, tk.END)
           self.issue_member_id.delete(0, tk.END)
           self.refresh_books()
           self.refresh_members()
           self.refresh_issued_books()
        else:
        # Database method already prints specific error
          messagebox.showerror("Error", "Failed to issue book. Book may be already issued or invalid IDs.")

    def return_book(self):
        """Return a book to the library"""
        book_id = self.return_book_id.get().strip()
        
        if not book_id:
            messagebox.showerror("Error", "Please enter Book ID")
            return
        
        return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.db.return_book(book_id, return_date):
            messagebox.showinfo("Success", f"Book {book_id} returned successfully")
            self.return_book_id.delete(0, tk.END)
            self.refresh_books()
            self.refresh_issued_books()
        else:
            messagebox.showerror("Error", "Failed to return book. Check if Book ID is valid.")
    
    def refresh_issued_books(self):
        """Refresh the issued books list"""
        # Clear existing items
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        
        # Get issued books from database
        issued_books = self.db.get_issued_books()
        
        for book in issued_books:
            issue_id, title, name, issue_date = book
            self.issued_tree.insert('', 'end', values=(issue_id, title, name, issue_date))
    
    def search_book_by_title(self):
        """Search for a book by title and display results"""
        title = self.search_title_entry.get().strip()
        
        if not title:
            messagebox.showerror("Error", "Please enter a title to search")
            return
        
        results = self.db.search_book_by_title(title)
        
        self.search_results_text.delete(1.0, tk.END)
        
        if results:
            self.search_results_text.insert(tk.END, "SEARCH RESULTS FOR BOOKS:\n")
            self.search_results_text.insert(tk.END, "=" * 50 + "\n")
            for book in results:
                book_id, title, author, is_available = book
                status = "Available" if is_available == 1 else "Issued"
                self.search_results_text.insert(tk.END, f"ID: {book_id} | {title} by {author} [{status}]\n")
        else:
            self.search_results_text.insert(tk.END, f"No books found with title containing '{title}'")
    
    def search_member_by_name(self):
      """Search for a member by name and display results"""
      name = self.search_member_entry.get().strip()
    
      if not name:
        messagebox.showerror("Error", "Please enter a name to search")
        return
    
      results = self.db.search_member_by_name(name)
    
      self.search_results_text.delete(1.0, tk.END)
    
      if results:
        self.search_results_text.insert(tk.END, "SEARCH RESULTS FOR MEMBERS:\n")
        self.search_results_text.insert(tk.END, "=" * 50 + "\n")
        for member in results:
            member_id, name, phone, books_issued = member
            books_count = len(books_issued.split(',')) if books_issued else 0
            self.search_results_text.insert(tk.END, f"ID: {member_id} | {name} | Phone: {phone} | Books: {books_count}\n")
      else:
        self.search_results_text.insert(tk.END, f"No members found with name containing '{name}'")

    def show_about(self):
      """Show about dialog"""
      about_text = """BookWise - Library Management System Version 1.0

    A Python-based Library Management System using:
    - Object Oriented Programming (OOP)
    - Tkinter GUI
    - SQLite Database

    Created for Python Course Project"""
      messagebox.showinfo("About", about_text)

#==============MAIN ENTRY POINT================
if __name__=="__main__":
    app = LibraryManagementSystem()