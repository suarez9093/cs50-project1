import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=True)
    isbn = db.Column(db.String, nullable=True)
    year = db.Column(db.String, nullable=True)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def add_review(self, review):
        r = Review(review=review, book_id=self.id)
        db.session.add(r)
        db.session.commit()

    def add_rating(self, rating):
        r = Review(rating=rating, book_id=self.id)
        db.session.add(r)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.id"), nullable=False)
