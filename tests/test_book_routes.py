import pytest


def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book_succeeds(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }

def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
    # Act
    data = {"title": "Desert book"}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
#     # Act
#     data = {"title": "Mountain book"}
#     response = client.get("books", query_string = data)
#     response_body = response.get_json()
#     # Assert
#     assert response.status_code == 200
#     assert len(response_body) == 1
#     assert response_body[0] == {
#         "id": 2,
#         "title": "Mountain Book",
#         "description": "i luv 2 climb rocks"
#     }

def test_get_one_book_missing_record(client, two_saved_books):
    # Act
    response = client.get("/books/300")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 300 not found"}

def test_get_one_book_invalid_id(client, two_saved_books):
# Act
    response = client.get("/books/tablet")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book tablet invalid"}

def test_create_one_book(client):
    # Act`
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }

def test_create_one_book_empty_title(client):
    # Act
    test_data = {"description": "The Best!"}
    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing title'}

def test_create_one_book_empty_description(client):
    # Act
    test_data = {"title": "Chess and massacre"}
    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing description'}

def test_create_one_book_extra_keys(client):
    # Act
    response = client.post("/books", json={
        "extra": "unknown",
        "key": "unknown",
        "title": "New Book",
        "description": "The Best!"
    })
    
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }

def test_update_book(client, two_saved_books):
    # Arrange
    test_data = {"title": "New Book", 
                "description": "Some new description"}
    
    # Act
    response = client.put("/books/1", json = test_data)

    # Assert
    assert response.status_code == 200

def test_update_book_extra_keys(client, two_saved_books):
    # Arrange
    test_data = {"extra": "Key",
                "title": "New Book", 
                "description": "Some new description", 
                "key": "Extra"}
    
    # Act
    response = client.put("/books/1", json = test_data)

    # Assert
    assert response.status_code == 200

def test_update_book_missing_data(client, two_saved_books):
    # Arrange
    test_data = {"title": "New Book", 
                "description": "Some new description"}
    
    # Act
    response = client.put("/books/3", json = test_data)

    # Assert
    assert response.status_code == 404

def test_update_book_invalid_id(client, two_saved_books):
    # Arrange
    test_data = {"title": "New Book", 
                "description": "Some new description"}
    
    # Act
    response = client.put("/books/tablet", json = test_data)

    # Assert
    assert response.status_code == 400

def test_delete_book(client, two_saved_books):
    # Act
    response = client.delete("/books/1")

    # Assert
    assert response.status_code == 200

def test_delete_book_missing_record(client, two_saved_books):
    # Act
    response = client.delete("/books/3")

    # Assert
    assert response.status_code == 404

def test_delete_book_invslid_id(client, two_saved_books):
    # Act
    response = client.delete("/books/tablet")

    # Assert
    assert response.status_code == 400