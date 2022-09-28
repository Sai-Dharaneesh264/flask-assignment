from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_required
)

from models.book import BookModel

class Author(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('image',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('author',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('minutes',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('reads',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('status',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    
    @jwt_required()
    def get(self, author):
        all_books = BookModel.find_by_author(author)
        books = [book.json() for book in all_books]
        if books:
            return {'books': books}, 200

        return {'message': "Book with author not found"}
    
    @jwt_required()
    def delete(self, author):
        all_books = BookModel.find_by_author(author)
        # print(type(book))
        if all_books:
            [book.delete_from_db() for book in all_books]
            return {'msg': f'delete book with author {author}'}
        else:
            return {'message': "book with author is not present"}

    

class BookId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('image',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('author',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('minutes',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('reads',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('status',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    
    @jwt_required()
    def get(self, _id):
        book = BookModel.find_by_id(_id)
        print('id = ', id)
        print('book =', book)
        if book:
            return book.json()
        return {'message': "Book with id not found"}
    
    @jwt_required()
    def delete(self, _id):
        book = BookModel.find_by_id(_id)
        print(type(book))
        if book:
            book.delete_from_db()
            return {'msg': f'deleted book with id {_id}'}
        else:
            return {'message': "book with id is not present"}

    @jwt_required()
    def put(self, _id):
        book = BookModel.find_by_id(_id)
        
        data = BookId.parser.parse_args()
        print('data =', data)
       
        if book:
            if data['title']:
                book.title = data['title']
            if data['image']:    
                book.image = data['image']
            if data['minutes']:    
                book.minutes = data['minutes']
            if data['reads']:    
                book.reads = data['reads']
            if data['type']:    
                book.type = data['type']
            if data['status']:    
                book.status = data['status']
            if data['author']:
                book.author = data['author']   
            book.commit_db()
            return book.json()
        else:
            return {'msg': f'A book with id {_id} does not exists'}




class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('image',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('author',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('minutes',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('reads',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    @jwt_required()
    def post(self):
        data = Book.parser.parse_args()
        book = BookModel(**data)
        try:
            book.save_to_db()
        except:
            return {'message': "An error occured inserting the item."}, 500
        return book.json(), 201

    


class BookList(Resource):
    @jwt_required()
    def get(self):
        books = [book.json() for book in BookModel.find_all()]
        if books:
            return {'books': books}, 200