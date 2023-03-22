from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

error404 = str("The kid is not registered in Santa's list :(")

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Santa's List! Add your kids' name, and let Santa know if they should recieve any presents"}

def test_read_kid():
    response = client.get("/kids/Joanet")
    assert response.status_code == 200
    assert response.json() == {
        "name" : "Joanet", "age": 6, "description" : "He sticks his chewing gum under the tables in class", "behaviour" : 3
    }

def test_read_inexistent_kid():
    response = client.get("/kids/Duna")
    assert response.status_code == 404
    assert response.json() == {
        "detail": error404
    }

def test_create_kid():
    response = client.post("/new_kid/", json={"name" : "Nil", "age": 7, "description" : "He still pees in his bed, but he is the best kid in class", "behaviour" : 9})
    assert response.status_code == 200
    assert response.json() == {
        "name" : "Nil", "age": 7, "description" : "He still pees in his bed, but he is the best kid in class", "behaviour" : 9
    }

def test_create_existing_kid():
    response = client.post("/new_kid/", json={"name" : "Laura", "age": 11, "description" : "She helps with house duties, but she doesn't pay attention sometimes", "behaviour" : 7})
    assert response.status_code == 403
    assert response.json() == {
        "detail": "The kid is already in Santa's List"
    }

def test_update_kid():
    response =client.put("/update_kid/Laura", json={"name" : "Laura", "age": 11, "description" : "She has made an improvement this weekend", "behaviour" : 8})
    assert response.status_code == 200
    assert response.json() == {
        "name" : "Laura", "age": 11, "description" : "She has made an improvement this weekend", "behaviour" : 8
    }

def test_update_inexisting_kid():
    response =client.put("/update_kid/Duna", json={"name" : "Duna", "age": 22, "description" : "She is too old for Christmas", "behaviour" : 5})
    assert response.status_code == 404
    assert response.json() == {
        "detail": error404
    }

def test_delete_kid():
    response = client.delete("/delete_kid/Tina")
    assert response.status_code == 200
    assert response.json() == str("The kid has been deleted from Santa's list, he won't get presents anymore")


def test_delete_inexisting_kid():
    response = client.delete("/delete_kid/Duna")
    assert response.status_code == 404
    assert response.json() == {
        "detail": error404
    }