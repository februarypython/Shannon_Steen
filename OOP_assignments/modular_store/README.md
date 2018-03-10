Learning Python OOP - Week 9 - Assignment 10 - Modular Store
Rebuild your store:
• Use your code from the previous optional assignment, Store, to start things off. You should have a single document called store.py

• Create two new documents called product.py and manage.py.

• Divide your code. All of the code for your Product class should be moved to the document product.py. Your product and store documents should contain only the code for their respective classes. Create a few instances of product and store in those documents, but wrap them in your conditional check for __name__ == "__main__".

• Import both classes into manage.py. Now you can create objects of both type and those objects can interact in a third environment, or namespace.