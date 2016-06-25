import os
import time
import math
import csv
from user import User
from interface import Interface
from ratings import Ratings
from validity import Validity
from dict_builder import DictBuilder
from show import Interface
from tracks import Tracks
from movie import Movie
from top_picks import TopPicks
from utilities import sorter


def main():
    Interface.clear()

    # TODO - delete this print_title_bar?
    Interface.print_title_bar(Interface.greeting)
    movie_ratings_dict, movie_dict, id_to_title, user_ratings_dict, user_dict = DictBuilder.build_dictionaries()

    while True:
        # Interface.print_title_bar(Interface.greeting)
        track_choice = Tracks.get_track_choice()
        if track_choice == 1:
            Interface.clear()
            # Info Track
            Tracks.show_info_track(id_to_title, movie_dict, user_dict)
        elif track_choice == 2:
            # Top movies
            Tracks.show_top_movies()
        else:
            Interface.show_quit()
            break
    Interface.clear()


if __name__ == '__main__':
    main()
