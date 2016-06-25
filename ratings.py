# import math
from interface import Interface
# # from utilities import Utilities
# from validity import Validity


class Ratings():
    @staticmethod
    def get_common_user_ratings(user_dict, user1, user2):
        a = set([i[0] for i in user_dict[user1].ratings])
        b = set([i[0] for i in user_dict[user2].ratings])
        common = a & b
        return sorted(common)

    @staticmethod
    def get_ratings_for_common_list(user_dict, user, movies_both_rated):
        a = []
        for i in movies_both_rated:
            for r in user_dict[user].ratings:
                if r[0] == i:
                    a.append(r[1])
        return a

    @staticmethod
    def euclidean_distance(user_dict, user, user2, movies_both_rated):
        """Given two lists, give the Euclidean distance between them on a scale
        of 0 to 1. 1 means the two lists are identical.
        """
        if len(movies_both_rated) < 5:
            return 0
        a = Ratings.get_ratings_for_common_list(
            user_dict, user, movies_both_rated
        )
        b = Ratings.get_ratings_for_common_list(
            user_dict, user2, movies_both_rated
        )
        # Note that this is the same as vector subtraction.
        differences = [a[idx] - b[idx] for idx in range(
            len(movies_both_rated)
        )]
        squares = [diff ** 2 for diff in differences]
        sum_of_squares = sum(squares)

        return float("%.2f" % (1 / (1 + math.sqrt(sum_of_squares))))

    @staticmethod
    def find_highest_rated_by_similar_users(user_dict, similarity_list, user):
        highest_rated_movies = []
        for i in similarity_list[:25]:
            count = 0
            common = Ratings.get_common_user_ratings(user_dict, user, i[0])
            for r in user_dict[i[0]].ratings[:10]:
                if r[0] not in common:
                    count += 1
                    highest_rated_movies.append((r[0], r[1] * i[1]))
        return sorted(
            highest_rated_movies[:10], key=Utilities.sorter, reverse=True
        )

    @staticmethod
    def get_similarity_list(user_dict, user):
        similarity_list = []
        for userID in user_dict:
            common = Ratings.get_common_user_ratings(user_dict, user, userID)
            sim = Ratings.euclidean_distance(user_dict, user, userID, common)
            similarity_list.append((userID, sim))
        return sorted(similarity_list, key=Utilities.sorter, reverse=True)

    @staticmethod
    def print_similar_recommendations(id_to_title, recommendation_list):
        for i, item in enumerate(recommendation_list):
            print("{}. {}".format(i + 1, id_to_title[item[0]]))

    @staticmethod
    def get_top_or_recommend(recommendations_track_message):
        choice = input("Would you like to:\n1) See the highest rated movies\n2) Get personalized recommendations\n>")

        if Interface.is_valid_two_track_input(choice):
            Interface.clear()
            if int(choice) == 1:
                return 1
            else:
                return 2
        else:
            Interface.clear()
            Interface.print_title_bar(recommendations_track_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Ratings.get_top_or_recommend(recommendations_track_message)

    @staticmethod
    def show_recommendations(
        id_to_title, recommendation_list, recommended_movies_message,
        number_to_show=10
    ):
        print("These are the top 10 movies that similar uses have rated highly:\n")
        Interface.print_similar_recommendations(id_to_title, recommendation_list)

        input("\nPress any key to return to the main menu\n>")
        print('\n' + '*' * 30)

        Interface.clear()
        Interface.print_title_bar("Hello Again!")
        return ''
