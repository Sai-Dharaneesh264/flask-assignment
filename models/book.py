from ast import Delete
from db import db
from sqlalchemy import select, insert, update, delete

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    image = db.Column(db.String(80))
    author = db.Column(db.String(80))
    minutes = db.Column(db.String(80))
    reads = db.Column(db.String(80))
    type = db.Column(db.String(80))
    status = db.Column(db.String(80))

    def __init__(self, title, image, author, minutes, reads, type, status):
        self.title = title
        self.image = image
        self.author = author
        self.minutes = minutes
        self.reads = reads
        self.type = type
        self.status = status
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image,
            'author': self.author,
            'minutes': self.minutes,
            'reads': self.reads,
            'type': self.type,
            'status': self.status
        }

    @classmethod
    def find_by_author(self, author):
        return self.query.filter_by(author=author).all()

    @classmethod    
    def find_all(self):
        return self.query.all()

    @classmethod
    def find_by_id(self, _id):
        return self.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def commit_db(self):
        db.session.commit()
        