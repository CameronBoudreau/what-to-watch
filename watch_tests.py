from what_to_watch import *

movie_ratings_dict = get_movie_ratings_dict()
movie_dict = get_movie_dict(movie_ratings_dict)
id_to_title = set_ids_to_titles(movie_dict)
user_ratings_dict = get_user_ratings_dict()
user_dict = get_user_dict(user_ratings_dict)


def test_get_movie_ratings():
    assert movie_ratings_dict[16][:3] == [(10, 4), (181, 1), (268, 3)]

def test_average_ratings():
    assert (movie_dict[44].average) == 3.34


def test_find_movie_by_id():
    assert id_to_title[2] == 'GoldenEye (1995)'


def test_get_user_ratings():
    assert user_ratings_dict[2][:3] == [(292, 4), (251, 5), (50, 5)]


def test_find_ratings_in_user_object():
    assert user_dict[356].ratings[:3] == [(313, 5), (937, 2), (689, 5)]
