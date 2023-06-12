import os
import pytest
from app import create_app
from models import UsersModel, WardrobesModel, ItemsModel, ImagesModel

@pytest.fixture(scope='module')
def new_user():
    new_user_info = {
        "user_id": "853fc94565724731826185d5485961c5",
        "user_name": "Jack Doe",
        "user_email": "jackdoe@gmail.com",
        "user_password": "123456"
    }
    user = UsersModel(**new_user_info)
    return user

@pytest.fixture(scope='module')
def new_wardrobe():
    new_wardrobe_info = {
        "wardrobe_id": "22d8bb84f2784d0e95f25ba92ee6ad38",
        "wardrobe_description": "Given by my best friend",
        "wardrobe_name": "White Wardrobe", 
        "wardrobe_image": "url_white_wardrobe",
        "user_id": "853fc94565724731826185d5485961c5"
    }
    wardrobe = WardrobesModel(**new_wardrobe_info)
    return wardrobe

@pytest.fixture(scope='module')
def new_item():
    new_item_info = {
        "item_id": "a81a416d2ed94e42a5ec6e99a1922e79",
        "item_color": "green",
        "item_category": "gloves",
        "item_suitability": "skiing",
        "item_price": 29.99,
        "item_time": "2023-05-29 00:00:00",
        "item_season": "winter",
        "wardrobe_id": "22d8bb84f2784d0e95f25ba92ee6ad38"
    }
    item = ItemsModel(**new_item_info)
    return item

@pytest.fixture(scope='module')
def new_image():
    new_image_info = {
        "image_id": "2189d3461811455a9bf8264e3a0d7734",
        "url": "image_url"
    }
    image = ImagesModel(**new_image_info)
    return image

@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!