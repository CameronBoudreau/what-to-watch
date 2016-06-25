from show import Show
from interface import Interface
from movie import Movie
# from user import User
# from ratings import Ratings
# from top_picks import TopPicks


class Tracks():
    @staticmethod
    def get_track_choice():
        Show.print_title_bar(Show.track_choice_message)
        track_choice = Interface.ask_for_track_choice(
            Show.track_choice_message
        )
        return track_choice

    @staticmethod
    def show_info_track(id_to_title, movie_dict, user_dict):
        Show.print_title_bar(Show.movie_or_user_info_message)
        movie_or_user_track = Interface.ask_for_movie_or_user_track(
            Show.movie_or_user_info_message
        )
        if movie_or_user_track == 1:
            # """ Movie Track """
            Show.print_title_bar(Show.movie_info_message)
            if Interface.does_know_id(Show.movie_info_message):
                # """ Movie Info """
                Tracks.find_movie(id_to_title, movie_dict)

            else:
                # """ Search for Movies """
                Show.print_title_bar(Show.search_for_movie_message)
                movie_id = Movie.search_for_movies(
                    movie_dict, Show.search_for_movie_message
                )
                movie_title = id_to_title[movie_id]
                Show.print_title_bar(movie_title)
                Movie.display_movie_info(
                    movie_dict, movie_id, movie_title)
        elif movie_or_user_track == 2:
            # """ User Track """
            Show.clear()
            Show.print_title_bar(Show.find_user_message)
            user_id = User.get_user_to_look_up(
                user_dict, Show.find_user_message
            )
            Show.print_title_bar(Show.user_look_up_message)
            User.display_user_ratings(
                user_dict, user_id, id_to_title, Show.user_look_up_message
            )

    @staticmethod
    def find_movie(id_to_title, movie_dict):
        Show.print_title_bar(Show.lets_find_your_movie_message)
        movie_id = Interface.get_movie_id(
            Show.lets_find_your_movie_message
        )
        movie_title = id_to_title[movie_id]
        Show.print_title_bar(movie_title)
        Movie.display_movie_info(
            movie_dict, movie_id, movie_title)

    @staticmethod
    def show_top_movies(movie_dict, user_dict, id_to_title, top_picks, user):
        Show.clear()
        Show.print_title_bar(Show.recommendations_track_message)
        top_or_recommend = Ratings.get_top_or_recommend(
            Show.recommendations_track_message
        )
        if top_or_recommend == 1:
            # Top Rated Movies
            top_picks = TopPicks.find_top_picks(movie_dict)
            top_picks_for_user = TopPicks.find_top_picks_for_user(user_dict, top_picks, user)
            top_picks = TopPicks.find_top_picks(movie_dict)

            Show.print_title_bar(Show.top_rated_overall_message)
            TopPicks.display_top_rated_movies(
                movie_dict, top_picks, top_picks_for_user, id_to_title,
                Show.top_rated_overall_message, False
            )

            Show.print_title_bar(Show.top_rated_overall_message)
            TopPicks.show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title)
        else:
            # Recommendations
            Show.print_title_bar(Show.recommended_movies_message)
            similarity_list = Ratings.get_similarity_list(user_dict, user)
            recommendation_list = Ratings.find_highest_rated_by_similar_users(
                user_dict, similarity_list, user
            )
            Ratings.how_recommendations(
                id_to_title, recommendation_list,
                Show.recommended_movies_message
            )
