from attacks.dictionary_attack.info import Info

username = "test"

info_list_hashmap = {
    "first_name": "Jeff",
    "last_name": "Henry",
    "birthday": "01/01/1990",
    "mother_name": "Jane",
    "father_name": "John",
    "pet_name": "Rex",
    "child_name": "Sally",
    "birthplace": "New York",
    "favorite_sport": "Basketball",
    "favorite_team": "Lakers",
    "favorite_movie": "Star Wars",
    "favorite_band": "The Beatles",
    "favorite_color": "Blue",
    "favorite_food": "Pizza",
    "favorite_drink": "Coke",
    "favorite_animal": "Dog",
    "favorite_number": "1234",
    "favorite_car": "Tesla",
    "favorite_book": "Harry Potter",
    "favorite_place": "Disneyland",
    "favorite_song": "Hey Jude",
    "favorite_school": "Harvard",
    "favorite_teacher": "Mr. Smith",
    "favorite_subject": "Math",
    "favorite_tv_show": "Friends",
    "favorite_vacation": "Hawaii",
    "favorite_holiday": "Christmas",
    "favorite_restaurant": "McDonalds",
    "favorite_store": "Walmart",
    "favorite_brand": "Apple",
    "favorite_thing": "Computer",
    "favorite_person": "Elon Musk",
    "favorite_athlete": "Lebron James",
    "favorite_artist": "Leonardo Da Vinci",
    "favorite_author": "J.K. Rowling",
    "favorite_celebrity": "Tom Cruise",
    "favorite_character": "Harry Potter",
    "favorite_game": "Fortnite",
    "favorite_app": "Instagram",
    "favorite_website": "Google",
    "favorite_social_media": "Facebook"
}

info_list_objects = [Info(key, value) for key, value in info_list_hashmap.items()]
keywords = ["Jeff", "Henry", "1234"]