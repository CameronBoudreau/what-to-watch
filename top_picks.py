# from utilities import sorter
# from show import Show


class TopPicks():
    @staticmethod
    def find_top_picks(movie_dict, number_of_ratings=25):
        top_picks = []
        for i in movie_dict:
            if movie_dict[i].number_of_ratings >= number_of_ratings:
                top_picks.append((i, movie_dict[i].average))

        return sorted(top_picks, key=sorter, reverse=True)

    @staticmethod
    def find_top_picks_for_user(user_dict, top_picks, user):
        user = user_dict[user]
        user_top_picks = top_picks

        for pick in top_picks:
            for i in user.ratings:
                if i[0] == pick[0]:
                    user_top_picks.remove(pick)
        return user_top_picks

    @staticmethod
    def show_top_picks_with_title(
        movie_dict, top_picks, id_to_title, number_to_show=20
    ):
        count = 1
        for i in top_picks:
            if count > number_to_show:
                return ''
            print("{}. {}: {}".format(count, id_to_title[i[0]], i[1]))
            count += 1

    @staticmethod
    def display_top_rated_movies(
        movie_dict, top_picks, top_picks_for_user, id_to_title,
        top_rated_overall_message, filtered=False, number_to_show=10
    ):
        print("Out of the {} movies in the database, these are the top {}.\n".format(len(movie_dict), number_to_show))

        Show.show_top_picks_with_title_filtered
        if filtered:
            TopPicks.show_top_picks_with_title(
                movie_dict, top_picks_for_user, id_to_title, number_to_show
            )
        else:
            TopPicks.show_top_picks_with_title(
                movie_dict, top_picks, id_to_title, number_to_show
            )
        print('\n' + '*' * 30)

        option = input("\nFrom here, you can:\n\n1) Shows more movies\n2) Filter/Unfilter movies you have already seen\n3) Return to the main menu\n>")

        Show.show_filtered(
            option, movie_dict, top_picks, top_picks_for_user, id_to_title,
            top_rated_overall_message, filtered, number_to_show
        )
