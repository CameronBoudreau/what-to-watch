import os
from what_to_watch_main import *

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


    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
