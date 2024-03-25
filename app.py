from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Book:
    def __init__(self, title, author, bookId):
        self.title = title
        self.author = author
        self.bookId = bookId

    def display(self):
        return f"{self.title} ({self.bookId}) by {self.author}"

class EBook(Book):
    def __init__(self, title, author, file_format, bookId):
        super().__init__(title, author, bookId)
        self.file_format = file_format

    def display(self):
        return f"{super().display()} - Format: {self.file_format}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_all_books(self):
        return [book.display() for book in self.books]

    def search_book_by_title(self, title):
                return [book.display() for book in self.books]
    
library = Library()

# Flask API
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    file_format = data.get('file_format')
    bookId = data.get('bookId')

    if title and author:
        if file_format:
            new_book = EBook(title, author, file_format, bookId)
        else:
            new_book = Book(title, author)

        library.add_book(new_book)
        return jsonify({"message": "Book added successfully"})
    else:
        return jsonify({"error": "Invalid data"})

@app.route('/list_books', methods=['GET'])
def list_books():
    return jsonify({"books": library.display_all_books()})

@app.route('/delete_book', methods=['DELETE'])
def delete_book():
    data = request.get_json()
    title_to_delete = data.get('title')

    if title_to_delete:
        for book in library.books:
            if book.title == title_to_delete:
                library.books.remove(book)
                return jsonify({"message": "Book deleted successfully"})
        return jsonify({"error": "Book not found"})
    else:
        return jsonify({"error": "Invalid data"})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/search_books', methods=['GET'])
def search_books():
    print("Request received for /search_books")
    query = request.args.get('query', '')
    print('Query:', query)
    app.logger.info('Query: %s', query)
    if query:
        search_results = library.search_book_by_title(query)
        return jsonify({"results": search_results})
    else:
        return jsonify({"error2": "Invalid query"})