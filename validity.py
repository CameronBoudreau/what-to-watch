# from interface import Interface


class Validity():
    @staticmethod
    def check_number_to_show(number_to_show, total_ratings, text):
        if Validity.is_valid_number_entry(number_to_show, total_ratings):
            Interface.clear()
            Interface.print_title_bar(text)
            return int(number_to_show)
        else:
            Validity.invalid_choice(text)
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
