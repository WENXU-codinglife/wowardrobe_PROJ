def test_new_user_with_fixture(new_user):
    assert new_user.__tablename__ == 'users'
    assert new_user.user_email == "jackdoe@gmail.com"
    assert new_user.user_name == "Jack Doe"
    assert new_user.user_password == "123456"

def test_new_wardrobe_with_fixture(new_wardrobe):
    assert new_wardrobe.__tablename__ == 'wardrobes'
    assert new_wardrobe.wardrobe_id == "22d8bb84f2784d0e95f25ba92ee6ad38"
    assert new_wardrobe.wardrobe_description == "Given by my best friend"
    assert new_wardrobe.wardrobe_name == "White Wardrobe"
    assert new_wardrobe.wardrobe_image == "url_white_wardrobe"
    assert new_wardrobe.user_id == "853fc94565724731826185d5485961c5"

def test_new_item_with_fixture(new_item):
    assert new_item.__tablename__ == "items"
    assert new_item.item_id == "a81a416d2ed94e42a5ec6e99a1922e79"
    assert new_item.item_color == "green"
    assert new_item.item_category == "gloves"
    assert new_item.item_suitability == "skiing"
    assert new_item.item_price == 29.99
    assert new_item.item_time == "2023-05-29 00:00:00"
    assert new_item.item_season == "winter"
    assert new_item.wardrobe_id == "22d8bb84f2784d0e95f25ba92ee6ad38"    

def test_new_image_with_fixture(new_image):
    assert new_image.__tablename__ == "images"
    assert new_image.image_id == "2189d3461811455a9bf8264e3a0d7734"
    assert new_image. url == "image_url"