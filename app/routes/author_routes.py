from flask import Blueprint, abort, make_response, request, Response
from app.models.author import Author
from app.models.book import Book
from .route_utilities import validate_model, create_model
from ..db import db
# from app.models.book import books

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

# Define endpoint methods here

# def validate_author_by_name(author_name): 
#     query = db.select(Author).where(Author.name == author_name)
#     author = db.session.scalar(query)

#     if not author:
#         response = {"message": f"{author_name} not found"}
#         abort(make_response(response, 404))
#     return author_name

@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

@bp.get("")
def get_all_authors():
    query = db.select(Author)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Author.title.ilike(f"%{name_param}%"))

    query = query.order_by(Author.id)
    authors = db.session.scalars(query)

    authors_response = []
    for author in authors:
        authors_response.append(author.to_dict())
    return authors_response

@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    request_body["author_id"] = author.id
    return create_model(Book, request_body)


# @bp.get("/<author_id>/books")
# def get_books_by_author(author_id):
#     author = validate_model(Author, author_id)
#     response = [book.to_dict() for book in author.books]
#     return response


# @bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_model(Book, book_id)

#     return book.to_dict()

# @bp.put("/<book_id>")
# def update_book(book_id):
#     book = validate_model(Book, book_id)
#     request_body = request.get_json()

#     book.title = request_body["title"]
#     book.description = request_body["description"]
#     db.session.commit()

#     return Response(status = 200, mimetype = "application/json" )

# @bp.delete("/<book_id>")
# def delete_book(book_id):
#     book = validate_model(Book, book_id)
#     db.session.delete(book)
#     db.session.commit()

#     return Response(status = 200, mimetype = "application/json")