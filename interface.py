import os
import time


class Interface():
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
        Interface.check_number_to_show(number_to_show, total_ratings, text)

    @staticmethod
    def show_filtered(
        option, movie_dict, top_picks, top_picks_for_user, id_to_title,
        top_rated_overall_message, filtered, number_to_show
    ):
        if Interface.is_valid_three_track_input(option):
            Interface.show_refined(
                movie_dict, top_picks, top_picks_for_user, id_to_title,
                top_rated_overall_message, filtered, number_to_show
            )
        else:
            Interface.clear()
            Interface.print_title_bar(Interface.top_rated_overall_message)
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
            Interface.show_top_unseen(
                movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, filtered, number_to_show
            )
        elif int(option) == 3:
            Interface.clear()
            Interface.print_title_bar("Hello Again!")
            return ''

    def show_top_unseen(
        movie_dict, top_picks, top_picks_for_user, id_to_title,
        top_rated_overall_message, filtered, number_to_show
    ):
        Interface.clear()
        Interface.change_filtered(
            movie_dict, top_picks, top_picks_for_user, id_to_title,
            top_rated_overall_message, filtered, number_to_show, filtered
        )
        if filtered is False:
            filtered = True
        else:
            filtered = False
        Interface.print_title_bar(
            "These are the top rated movies you haven't seen yet!"
        )
        Ratings.display_top_rated_movies(
            movie_dict, top_picks, top_picks_for_user, id_to_title,
            top_rated_overall_message, filtered, number_to_show
        )

    @staticmethod
    def show_quit():
        Interface.clear()
        print('\n\n')
        Interface.print_title_bar("Bye! Come back soon!")
        time.sleep(2.5)

    @staticmethod
    def get_user_id(user_dict, greeting):
        user_id = input("Please input your User ID:\n>")
        Interface.clear()
        if Interface.is_valid_user_id_input(user_dict, user_id):
            return int(user_id)
        else:
            Interface.print_title_bar(greeting)
            print(("*" * 25) + '\n' + "Enter a valid User ID.\n" + ("*" * 25) + '\n')
            return Interface.get_user_id(user_dict, greeting)

    @staticmethod
    def ask_for_track_choice(track_choice_message):
        track = input("Please select from the following options:\n\n1) Browse movie and rating information\n2) Get movie recommendations\n3) Quit\n\n>")

        if Interface.is_valid_three_track_input(track):
            return int(track)
        else:
            Interface.clear()
            Interface.print_title_bar(track_choice_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Interface.ask_for_track_choice(track_choice_message)

    @staticmethod
    def ask_for_movie_or_user_track(movie_or_user_info_message):
        track = input("Please select from the following options:\n\n1) Browse movie information\n2) Browse user information\n\n>")
        Interface.clear()
        if Interface.is_valid_two_track_input(track):
            return int(track)
        else:
            Interface.print_title_bar(movie_or_user_info_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Interface.ask_for_movie_or_user_track(
                movie_or_user_info_message
            )

    @staticmethod
    def does_know_id(movie_or_user_info_message):
        knows = input("Do you know the ID of the movie you want to check? Don't worry if you don't - we'll help you find it!\nJust enter 'Y' for yes or 'N' for no.\n>")
        Interface.clear()
        if Interface.check_knows(knows, movie_or_user_info_message):
            if knows.lower() == 'y':
                return True
            else:
                return False
        else:
            Interface.print_title_bar(movie_or_user_info_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Interface.does_know_id(movie_or_user_info_message)

    @staticmethod
    def get_movie_id(lets_find_your_movie_message):
        movie_id = input("Please enter the numeric ID for the movie you want to access. If you need to go back to search for the code, enter 0.\n>")
        Interface.clear()
        if Interface.is_valid_movie_id(movie_id, lets_find_your_movie_message):
            return int(movie_id)
        else:
            Interface.print_title_bar(lets_find_your_movie_message)
            print(("*" * 25) + '\n' + "Enter a valid Movie ID.\n" + ("*" * 25) + '\n')
            return Interface.get_movie_id(lets_find_your_movie_message)

    @staticmethod
    def find_how_many(movie_dict):
        Interface.clear()
        Interface.print_title_bar("How many are we looking for?")
        number_to_show = Interface.get_number_to_show(
            len(movie_dict), "The list"
        )
        return number_to_show

    @staticmethod
    def check_number_to_show(number_to_show, total_ratings, text):
        if Interface.is_valid_number_entry(number_to_show, total_ratings):
            Interface.clear()
            Interface.print_title_bar(text)
            return int(number_to_show)
        else:
            Interface.invalid_choice(text)
            return Interface.get_number_to_show(total_ratings, text)

    @staticmethod
    def is_valid_number_entry(number_to_show, total_ratings):
        try:
            int(number_to_show)
        except:
            print("is_valid_number_entry returned FALSE - INT() failed")
            return False
        if int(number_to_show) < 1 or int(number_to_show) > total_ratings:
            print("is_valid_number_entry returned FALSE - RANGE")
            return False
        return True

    @staticmethod
    def is_valid_movie_id(movie_id, text):
        try:
            int(movie_id)
        except:
            return False
        if int(movie_id) < 0 or int(movie_id) > 1682:
            return False
        return True

    @staticmethod
    def check_knows(knows, movie_info_message):
        if not knows.isalpha():
            return False
        elif knows.lower() != 'y' and knows.lower() != 'n':
            return False

        return True

    @staticmethod
    def invalid_choice(text):
        Interface.clear()
        Interface.print_title_bar(text)
        print(
            ("*" * 25) + '\n' + "Enter a valid option.\n" + ("*" * 25) + '\n'
        )

    @staticmethod
    def is_valid_user_id_input(user_dict, user_id):
        try:
            int(user_id)
        except:
            return False
        if int(user_id) not in user_dict.keys():
            return False
        return True

    @staticmethod
    def is_valid_two_track_input(track):
        try:
            int(track)
        except:
            return False
        if int(track) != 1 and int(track) != 2:
            return False

        return True

    @staticmethod
    def is_valid_three_track_input(track):
        try:
            int(track)
        except:
            return False
        if int(track) != 1 and int(track) != 2 and int(track) != 3:
            return False

        return True
