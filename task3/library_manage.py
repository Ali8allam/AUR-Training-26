from enum import Enum
from abc import ABC, abstractmethod
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(SCRIPT_DIR, "database.txt")
class ItemStatus(Enum): 
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    LOST = "lost"

class LibraryItem(ABC): #abstract class

    _data = {} #records new item types


    # def __init__(self, title):
    #     self.title = title
    #     self.__status = ItemStatus.AVAILABLE #make it private access

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._data[cls.__name__] = cls

    def __init__(self, title, status=ItemStatus.AVAILABLE):
        self.title = title
        # pass string status when loading from database
        if isinstance(status, str):
            self.__status = ItemStatus(status.lower())
        else:
            self.__status = status


            
    def __str__(self):
        status = self.__status.value.replace("_", " ").title()
        return f"{self.title} ({self.__class__.__name__}) — {status}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, status={self.__status.name})"
    
    def __lt__(self, other): # for sorting library items by title
        return self.title.lower() < other.title.lower()

    
    @abstractmethod # decorator for subclasses
    def loan_period(self):
        pass

    def checkout(self):
        if self.__status != ItemStatus.AVAILABLE:
            raise ValueError("Item cannot be checked out.")
        
        self.__status = ItemStatus.CHECKED_OUT



    def return_item(self):
        if self.__status != ItemStatus.CHECKED_OUT:
            raise ValueError("Item cannot be returned.")

        self.__status = ItemStatus.AVAILABLE

    def lost_item(self):
        if self.__status == ItemStatus.LOST:
            raise ValueError("Item is already lost.")

        self.__status = ItemStatus.LOST

    def GetStatus(self): 
        return self.__status.name

    @classmethod
    def from_dict(cls, data): #deserialize object from dictionary
        item_type = data.pop('type')
        if item_type in cls._data:
            return cls._data[item_type](**data)
        raise ValueError(f"Unknown item type: {item_type}")
        
    def to_dict(self):# serialize object to dictionary 
        data = {"type": self.__class__.__name__, "title": self.title, "status": self.GetStatus()}
        # Add subclass specific attributes by checking __dict__
        for key, value in self.__dict__.items():
            if not key.startswith('_'): # Skip private/protected attributes
                data[key] = value
        return data


class Book(LibraryItem): #subclass1 of LibraryItem
    def __init__(self, title, author, isbn, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.author = author
        self.isbn = isbn

    @staticmethod
    def validate_isbn(isbn): #validates ISBN-13 checksum
        clean_isbn = isbn.replace("-", "").replace(" ", "")
        if len(clean_isbn) != 13 or not clean_isbn.isdigit():
            return False
        total = sum(int(num) * (1 if i % 2 == 0 else 3) for i, num in enumerate(clean_isbn))
        return total % 10 == 0

    def loan_period(self):
        return 21


class DVD(LibraryItem): #subclass2 of LibraryItem

    def __init__(self, title, director, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.director = director

    def loan_period(self):
        return 5


class Magazine(LibraryItem): #subclass3 of LibraryItem
    def __init__(self, title, issue, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.issue = issue
    def loan_period(self):
        return 14

class Database:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename=DEFAULT_DB_PATH):
        if not hasattr(self, 'initialized'):
            self.filename = filename
            self.initialized = True
            if not os.path.exists(self.filename):
                open(self.filename, 'a').close()

    def load_items(self):
        items = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    # Parse pipe-delimited string to dictionary
                    parts = line.split('|')
                    data_dict = dict(part.split('=', 1) for part in parts)
                    items.append(LibraryItem.from_dict(data_dict))
        except FileNotFoundError:
            pass
        return items

    def save_items(self, items):
        with open(self.filename, 'w') as f:
            for item in items:
                d = item.to_dict()
                line = "|".join(f"{k}={v}" for k, v in d.items())
                f.write(line + "\n")


class Library:
    
    def __init__(self):
        self.db = Database()
        self.items = self.db.load_items()

    def add_item(self, item):
        self.items.append(item)
        self.items.sort() 
        self.db.save_items(self.items)

    def find_by_title(self, title):
        for item in self.items:
            if item.title.lower() == title.lower():
                return item
        return None

    def checkout_item(self, title):
        item = next(
            (
                library_item
                for library_item in self.items
                if library_item.title.lower() == title.lower()
                and library_item.GetStatus() == "AVAILABLE"
            ),
            None,
        )
        if item:
            item.checkout()
            self.db.save_items(self.items)
            print(f"Success: Checked out '{item.title}'.")
        else:
            print("Item not found.")
            
    def list_available(self):
        for item in self.items:
            if item.GetStatus() == "AVAILABLE":
                print(item)  
#///////////
# for testing purposes  
# book = Book("Dune")

# print(book)
# print(repr(book))

# items = [
#     Book("Harry Potter"),
#     DVD("Avatar"),
#     Magazine("Science Weekly"),
#     Book("Dune")
# ]

# for item in sorted(items):
#     print(item)
# if __name__ == "__main__":
#     # Initialize the library (this will automatically load from database.txt)
#     my_library = Library()
#     my_library.add_item(DVD("Matrix", "Wachowskis"))
#     my_library.add_item(Magazine("Tech Monthly", "2026-09"))
#     for item in my_library.items:
#         print(item) # Tests __str__

#     print("\n=== TEST 3: Encapsulation & Status Transitions ===")
#     target_title = "Matrix"
#     print(f"Trying to check out '{target_title}'...")
#     my_library.checkout_item(target_title)

#     # print(" Initial Available Items (Sorted Automatically) ")
#     # my_library.list_available()

#     print("\n Testing Checkout")
#     my_library.checkout_item("Inception") # Should check out successfully
    
#     print("\n Testing ISBN Validation Static Method")
#     valid_isbn = "9780441013593"
#     print(f"Is ISBN {valid_isbn} valid?: {Book.validate_isbn(valid_isbn)}")