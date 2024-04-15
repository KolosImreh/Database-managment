import sqlite3

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create the book table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        qty INTEGER
    )
''')

# Populate the table with initial values
initial_books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
]

cursor.executemany('INSERT OR IGNORE INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)', initial_books)

# Save changes to the database
conn.commit()

# Function to add a new book to the database
def add_book():
    try:
        title = input('Enter book title: ')
        author = input('Enter author name: ')
        qty = int(input('Enter quantity: '))

        cursor.execute('INSERT INTO book (title, author, qty) VALUES (?, ?, ?)', (title, author, qty))
        conn.commit()
        print('Book added successfully!')
    except ValueError:
        print('Invalid input for quantity. Please enter a valid number.')

# Function to update book information
def update_book():
    try:
        book_id = int(input('Enter the book ID to update: '))
        title = input('Enter new title (press Enter to keep the existing title): ')
        author = input('Enter new author (press Enter to keep the existing author): ')
        qty = input('Enter new quantity (press Enter to keep the existing quantity): ')

        update_query = 'UPDATE book SET '
        update_values = []

        if title:
            update_query += 'title=?, '
            update_values.append(title)

        if author:
            update_query += 'author=?, '
            update_values.append(author)

        if qty:
            update_query += 'qty=?, '
            update_values.append(int(qty))  # Convert qty to int

        # Remove the trailing comma and space from the query
        update_query = update_query.rstrip(', ')

        # Add the WHERE clause to update the specific book
        update_query += ' WHERE id=?'
        update_values.append(book_id)

        cursor.execute(update_query, update_values)
        conn.commit()
        print('Book updated successfully!')
    except ValueError:
        print('Invalid input for quantity. Please enter a valid number.')

# Function to delete a book from the database
def delete_book():
    try:
        book_id = int(input('Enter the book ID to delete: '))
        cursor.execute('DELETE FROM book WHERE id=?', (book_id,))
        conn.commit()
        print('Book deleted successfully!')
    except ValueError:
        print('Invalid input for book ID. Please enter a valid number.')

# Function to search for a specific book
def search_books():
    search_term = input('Enter the title or author to search: ')
    cursor.execute('SELECT * FROM book WHERE title LIKE ? OR author LIKE ?', (f'%{search_term}%', f'%{search_term}%'))
    books = cursor.fetchall()

    if books:
        print('Search results:')
        for book in books:
            print(book)
    else:
        print('No matching books found.')

# Main program loop
while True:
    print('\nMenu:')
    print('1. Enter book')
    print('2. Update book')
    print('3. Delete book')
    print('4. Search books')
    print('0. Exit')

    choice = input('Enter your choice: ')

    if choice == '1':
        add_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        print('Exiting program.')
        conn.close()  # Close the database connection before exiting
        break
    else:
        print('Invalid choice. Please enter a valid option.')