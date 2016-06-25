import os
import time
from interface import Interface
# from ratings import Ratings
from validity import Validity


class Show():
    greeting = "Welcome to Movie Heaven!"
    track_choice_message = "How would you like to explore the collection?"
    movie_or_user_info_message = "What information are you looking for?"
    movie_info_message = "Let's find a movie!"
    lets_find_your_movie_message = "Let's find your movie!"
    search_for_movie_message = "We can help you find what you're looking for!"
    find_user_message = "Whose ratings would you like to see?"
    user_look_up_message = "Here's what that user has rated!"
    recommendations_track_message = "Should we do the work for you?"
    top_rated_overall_message = "These are the cream of the crop!"
    recommended_movies_message = "Based on your ratings, we think you'll like these!"

    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def print_title_bar(text):
        print(("#" * (len(text) + 10)))
        print(("#" + ' ' * (len(text) + 8) + '#'))
        print("#    {}    #".format(text))
        print(("#" + ' ' * (len(text) + 8) + '#'))
        print(("#" * (len(text) + 10)) + '\n\n')

    @staticmethod
    def get_number_to_show(total_ratings, text):
        number_to_show = input(
            "How many items would you like to see? {} has {} to show.\n>".format(text, total_ratings)
        )
        Validity.check_number_to_show(number_to_show, total_ratings, text)

    @staticmethod
    def show_filtered(
        option, movie_dict, top_picks, top_picks_for_user, id_to_title,
        top_rated_overall_message, filtered, number_to_show
    ):
        if Validity.is_valid_three_track_input(option):
            Show.show_refined(
                movie_dict, top_picks, top_picks_for_user, id_to_title,
                top_rated_overall_message, filtered, number_to_show
            )
        else:
            Show.clear()
            Show.print_title_bar(Show.top_rated_overall_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Ratings.display_top_rated_movies(
                movie_dict, top_picks, top_picks_for_user, id_to_title,
                top_rated_overall_message, filtered, number_to_show
            )

    def show_refined(
        movie_dict, top_picks, top_picks_for_user, id_to_title,
        top_rated_overall_message, filtered, number_to_show, option
    ):
        if int(option) == 1:
            Interface.find_how_many(movie_dict)
            Ratings.display_top_rated_movies(
                movie_dict, top_picks, top_picks_for_user, id_to_title,
                top_rated_overall_message, filtered, number_to_show
            )
        elif int(option) == 2:
            Show.show_top_unseen(
                movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, filtered, number_to_show
            )
        elif int(option) == 3:
            Show.clear()
            Show.print_title_bar("Hello Again!")
            return ''

    def show_top_unseen(
        movie_dict, top_picks, top_picks_for_user, id_to_title,
        top_rated_overall_message, filtered, number_to_show
    ):
        Show.clear()
        Interface.change_filtered(
            movie_dict, top_picks, top_picks_for_user, id_to_title,
            top_rated_overall_message, filtered, number_to_show, filtered
        )
        if filtered is False:
            filtered = True
        else:
            filtered = False
        Show.print_title_bar(
            "These are the top rated movies you haven't seen yet!"
        )
        Ratings.display_top_rated_movies(
            movie_dict, top_picks, top_picks_for_user, id_to_title,
            top_rated_overall_message, filtered, number_to_show
        )

    @staticmethod
    def show_quit():
        Show.clear()
        print('\n\n')
        Show.print_title_bar("Bye! Come back soon!")
        time.sleep(2.5)
