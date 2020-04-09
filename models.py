import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=True)
    isbn = db.Column(db.String, nullable=True)
    year = db.Column(db.String, nullable=True)
    details = db.Column(db.String, nullable=True)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)

