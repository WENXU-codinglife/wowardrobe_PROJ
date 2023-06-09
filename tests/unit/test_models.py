from models import UsersModel, WardrobesModel, ItemsModel, ImagesModel

def test_new_user():
    new_user_info = {
        "user_id": "853fc94565724731826185d5485961c5",
        "user_name": "Jack Doe",
        "user_email": "jackdoe@gmail.com",
        "user_password": "123456"
    }
    user = UsersModel(**new_user_info)
    assert user.__tablename__ == 'users'
    assert user.user_email == "jackdoe@gmail.com"
    assert user.user_name == "Jack Doe"
    assert user.user_password == "123456"

def test_new_wardrobe():
    new_wardrobe_info = {
        "wardrobe_id": "22d8bb84f2784d0e95f25ba92ee6ad38",
        "wardrobe_description": "Given by my best friend",
        "wardrobe_name": "White Wardrobe", 
        "wardrobe_image": "url_white_wardrobe",
        "user_id": "853fc94565724731826185d5485961c5"
    }
    wardrobe = WardrobesModel(**new_wardrobe_info)
    assert wardrobe.__tablename__ == 'wardrobes'
    assert wardrobe.wardrobe_id == "22d8bb84f2784d0e95f25ba92ee6ad38"
    assert wardrobe.wardrobe_description == "Given by my best friend"
    assert wardrobe.wardrobe_name == "White Wardrobe"
    assert wardrobe.wardrobe_image == "url_white_wardrobe"
    assert wardrobe.user_id == "853fc94565724731826185d5485961c5"

def test_new_item():
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
    assert item.__tablename__ == "items"
    assert item.item_id == "a81a416d2ed94e42a5ec6e99a1922e79"
    assert item.item_color == "green"
    assert item.item_category == "gloves"
    assert item.item_suitability == "skiing"
    assert item.item_price == 29.99
    assert item.item_time == "2023-05-29 00:00:00"
    assert item.item_season == "winter"
    assert item.wardrobe_id == "22d8bb84f2784d0e95f25ba92ee6ad38"    

def test_new_image():
    new_image_info = {
        "image_id": "2189d3461811455a9bf8264e3a0d7734",
        "url": "image_url"
    }
    image = ImagesModel(**new_image_info)
    assert image.__tablename__ == "images"
    assert image.image_id == "2189d3461811455a9bf8264e3a0d7734"
    assert image. url == "image_url"