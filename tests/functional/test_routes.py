from email import header
from typing import Dict, List

TEST_USER = {
    'USER_ID': '853fc94565724731826185d5485961c5',
    'USER_EMAIL': 'tester1@gmail.com',
    'USER_NAME': 'Jane Doe',
    'WARDROBE': {
        'WARDROBE_DESCRIPTION': "my first wordrobe. it's super large.",
        'WARDROBE_ID': "22d8bb84f2784d0e95f25ba92ee6ad38",
        'WARDROBE_IMAGE': "url_Large",
        'WARDROBE_NAME': "Large Wardrobe"
    }
}
TEST_USER_UNEXISTING_ID = '066ce054ec62440296f495091934ce5b'

access_code = ''
'''
in Python, if you assign a value to a variable within a function scope, 
it creates a new local variable instead of modifying the global variable 
with the same name.
'''


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Thank you for coming. The server is awake." in response.data

def test_home_page_post(test_client):
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Method Not Allowed" in response.data

def test_user_creation(test_client):
    new_user_info = {
        "user_name":"July Doe",
        "user_email":"testerJuly@gmail.com",
        "user_password":"12345678"
    }
    response = test_client.post(
        '/register',
        json = new_user_info,
    )
    assert response.status_code == 409
    assert b"A user with that email already exists." in response.data
    # assert response.status_code == 201
    # assert response.data.user_email == "testerJuly@gmail.com"
    # assert response.data.user_name == "July Doe"
    # assert response.data.user_id
    # assert len(response.data.wardrobe) == 0

def test_user_login(test_client):
    global access_code
    user_info = {
        "user_email":"testerJuly@gmail.com",
        "user_password":"12345678"
    }
    response = test_client.post(
        '/login',
        json = user_info
    )
    access_code = response.json['access_token']
    print(f'1. access_code = {access_code}')
    assert response.status_code == 200
    assert response.json['access_token']

def test_get_a_user(test_client):
    response = test_client.get(
        f'/user/{TEST_USER["USER_ID"]}'
    )
    assert response.status_code == 200
    assert response.json['user_email'] == TEST_USER['USER_EMAIL']
    assert response.json['user_id'] == TEST_USER['USER_ID']
    assert response.json['user_name'] == TEST_USER['USER_NAME']
    assert isinstance(response.json['wardrobes'], List)

def test_get_an_unexisting_user(test_client):
    response = test_client.get(
        f'/user/{TEST_USER_UNEXISTING_ID}'
    )
    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_get_wardrobes(test_client):
    response = test_client.get(
        '/wardrobesList'
    )
    assert response.status_code == 200
    assert isinstance(response.json, List)

def test_get_a_wardrobe(test_client):
    global access_code
    response = test_client.get(
        f'/wardrobe/{TEST_USER["WARDROBE"]["WARDROBE_ID"]}',
        headers = {'Authorization': f'Bearer {access_code}'}
    )
    print(f'2. access_code = {access_code}')
    assert response.status_code == 200
    assert response.json['wardrobe_description'] == TEST_USER['WARDROBE']['WARDROBE_DESCRIPTION']
    assert response.json['wardrobe_id'] == TEST_USER['WARDROBE']['WARDROBE_ID']
    assert response.json['wardrobe_image'] == TEST_USER['WARDROBE']['WARDROBE_IMAGE']
    assert response.json['wardrobe_name'] == TEST_USER['WARDROBE']['WARDROBE_NAME']
    assert isinstance(response.json['items'], List)
    assert isinstance(response.json['user'], Dict)

