import pytest
from fastapi import status
from sqlalchemy import select

from src.models import sellers, books


# Тест на ручку создания продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    new_seller_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "password": "strongpassword123"
    }

    response = await async_client.post("/api/v1/sellers/", json=new_seller_data)
    assert response.status_code == status.HTTP_201_CREATED

    created_seller_data = response.json()

    assert created_seller_data["first_name"] == new_seller_data["first_name"]
    assert created_seller_data["last_name"] == new_seller_data["last_name"]
    assert created_seller_data["email"] == new_seller_data["email"]


# Тест на получение инфы о продавце и его книгах
@pytest.mark.asyncio
async def test_get_seller(db_session, async_client):
    seller = sellers.Seller(first_name="Alice", last_name="Smith", email="alice_smith@example.com", password="securepassword")

    db_session.add(seller)
    await db_session.flush()

    book_1 = books.Book(author="Tolstoy", title="War and Peace", year=1869, count_pages=1225, seller_id=seller.id)
    book_2 = books.Book(author="Dostoevsky", title="Crime and Punishment", year=1866, count_pages=671, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")
    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    assert result_data["first_name"] == seller.first_name
    assert result_data["last_name"] == seller.last_name
    assert result_data["email"] == seller.email
    assert result_data["id"] == seller.id
    assert result_data["books"] == [
        {"id": book_1.id, "author": "Tolstoy", "title": "War and Peace", "year": 1869, "count_pages": 1225},
        {"id": book_2.id, "author": "Dostoevsky", "title": "Crime and Punishment", "year": 1866, "count_pages": 671}
    ]


# Тест на ручку получения списка всех продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = sellers.Seller(first_name="John", last_name="Doe", email="john_doe@example.com", password="securepassword1")
    seller_2 = sellers.Seller(first_name="Jane", last_name="Smith", email="jane_smith@example.com", password="securepassword2")

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    assert result_data == {
        "sellers": [
            {"first_name": "John", "last_name": "Doe", "email": "john_doe@example.com", "id": seller_1.id},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane_smith@example.com", "id": seller_2.id}
        ]
    }


# Тест на ручку обновления информации о продавце
@pytest.mark.asyncio
async def test_put_seller(db_session, async_client):
    seller = sellers.Seller(first_name="John", last_name="Doe", email="john_doe@example.com", password="securepassword1")

    db_session.add(seller)
    await db_session.flush()

    book_1 = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.put(f"/api/v1/sellers/{seller.id}",
                                      json={"first_name": "Jane", "last_name": "Smith", "email": "jane_smith@example.com"})

    assert response.status_code == status.HTTP_200_OK

    updated_seller = await db_session.get(sellers.Seller, seller.id)
    assert updated_seller.id == seller.id
    assert updated_seller.first_name == "Jane"
    assert updated_seller.last_name == "Smith"
    assert updated_seller.email == "jane_smith@example.com"


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = sellers.Seller(first_name="sadas", last_name="gfbf", email="dfbfdb@dfb.com", password="bbbb")

    db_session.add(seller)
    await db_session.flush()

    book_1 = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    seller = await db_session.execute(select(sellers.Seller, seller.id))
    res = seller.scalars().all()
    assert len(res) == 0

    for book_id in [book_1.id, book_2.id]:
        book = await db_session.execute(select(books.Book, book_id))
        res = book.scalars().all()
        assert len(res) == 0
