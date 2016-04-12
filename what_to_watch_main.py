import csv
import os
import math
from time import sleep
import sys


def print_text(a_string, a_is_slow):
    if a_is_slow:
        for words in a_string + "\n":
            sys.stdout.write(words)
            sys.stdout.flush()
            sleep(.03)
    else:
        print(a_string)


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Movie:
    def __init__(self, row, ratings):
        self.id = int(row['MovieID'])
        self.title = row['MovieTitle']
        self.ratings = sorted(ratings, key=sorter, reverse=True)
        self.average = self.find_average_rating(ratings)
        self.number_of_ratings = len(ratings)
        self.url = row['URL']
        self.genres = self.set_genre_list(row)

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

    def __repr__(self):
        return str(self)

    def find_average_rating(self, ratings):
        total = sum([t[1] for t in ratings])
        return float("%.2f" % (total / len(ratings)))

    def set_genre_list(self, row):
        self.genres = []
        for key in row:
            if row[key] == '1' and key != 'MovieID':
                self.genres.append(key)
        return self.genres

    def sorter(self, val):
        return val[1]


class User:
    def __init__(self, row, ratings):
        self.user_id = int(row['UserID'])
        self.age = int(row['Age'])
        self.sex = row['Sex']
        self.occupation = row['Occupation']
        self.ratings = sorted(ratings, key=sorter, reverse=True)
        self.highest_rated = self.find_highest_rated(self.ratings)

    def __str__(self):
        return str("{}: Age: {}; Sex: {}; Occupation: {}; Ratings: {}".format(self.user_id, self.age, self.sex, self.occupation, self.ratings))

    def __repr__(self):
        return str(self)

    def find_highest_rated(self, ratings):
        return sorted(ratings, key=sorter, reverse=True)

    def sorter(self, val):
        return val[1]



def get_movie_dict(movie_ratings_dict):
    with open('u.item', encoding='latin_1') as f:
        movie_dict = {}
        reader = csv.DictReader(f, fieldnames=['MovieID', 'MovieTitle', '', '', 'URL', 'Unknown', 'Action', 'Adventure', 'Animation',
              "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',  'Western'], delimiter='|')
        for row in reader:
            movie_dict[int(row['MovieID'])] = Movie(row, movie_ratings_dict[int(row['MovieID'])])
    return movie_dict


def get_movie_ratings_dict():
    with open('u.data', encoding='latin_1') as f:
        movie_ratings_dict = {}
        reader = csv.DictReader(f, fieldnames=['UserID', 'MovieID', 'Rating', 'Time'], delimiter='\t')
        for row in reader:
            if int(row['MovieID']) in movie_ratings_dict:
                movie_ratings_dict[int(row['MovieID'])].append((int(row['UserID']), int(row['Rating'])))
            else:
                movie_ratings_dict[int(row['MovieID'])] = [(int(row['UserID']), int(row['Rating']))]
    return movie_ratings_dict


def get_user_ratings_dict():
    with open('u.data', encoding='latin_1') as f:
        user_ratings_dict = {}
        reader = csv.DictReader(f, fieldnames=['UserID', 'MovieID', 'Rating', 'Time'], delimiter='\t')
        for row in reader:
            if int(row['UserID']) in user_ratings_dict:
                user_ratings_dict[int(row['UserID'])].append((int(row['MovieID']), int(row['Rating'])))
            else:
                user_ratings_dict[int(row['UserID'])] = [(int(row['MovieID']), int(row['Rating']))]
    return user_ratings_dict


def get_user_dict(user_ratings_dict):
        with open('u.user', encoding='latin_1') as f:
            user_dict = {}
            reader = csv.DictReader(f, fieldnames=['UserID', 'Age', 'Sex', 'Occupation', "ZipCode"], delimiter='|')
            for row in reader:
                user_dict[int(row['UserID'])] = User(row, user_ratings_dict[int(row['UserID'])])
        return user_dict


def set_ids_to_titles(movie_dict):
    id_to_title = {}
    for i in movie_dict:
        id_to_title[i] = movie_dict[i].title
    return id_to_title


def find_top_picks(movie_dict, number_of_ratings=25):
    top_picks = []
    for i in movie_dict:
        if movie_dict[i].number_of_ratings >= number_of_ratings:
            top_picks.append((i, movie_dict[i].average))

    return sorted(top_picks, key=sorter, reverse=True)

def find_top_picks_for_user(user_dict, top_picks, user):
    user = user_dict[user]
    user_top_picks = top_picks

    for pick in top_picks:
        for i in user.ratings:
            if i[0] == pick[0]:
                user_top_picks.remove(pick)
    return user_top_picks


def sorter(val):
    return val[1]

def show_top_picks_with_title(movie_dict, top_picks, id_to_title, number_to_show=20):
    count = 1
    for i in top_picks:
        if count > number_to_show:
            return ''
        print("{}. {}: {}".format(count, id_to_title[i[0]], i[1]))
        count += 1


def get_common_user_ratings(user_dict, user1, user2):
    # print("UserID 1: ", user1)
    # print("UserID 2: ", user2)
    a = set([i[0] for i in user_dict[user1].ratings])
    # print("\nGetting common rating set a: ", a)
    b = set([i[0] for i in user_dict[user2].ratings])
    # print("\nGetting common rating set b: ", b)

    common = a & b
    # print("\nCommon: ", sorted(common))
    return sorted(common)


def get_ratings_for_common_list(user_dict, user, movies_both_rated):
    a = []
    for i in movies_both_rated:
        for r in user_dict[user].ratings:
            if r[0] == i:
                a.append(r[1])
    return a


def euclidean_distance(user_dict, user, user2, movies_both_rated):
    """Given two lists, give the Euclidean distance between them on a scale
    of 0 to 1. 1 means the two lists are identical.
    """
    # print("\nLength of common list: ", len(movies_both_rated))
    if len(movies_both_rated) < 5:
        # print("Those users have not rated any of the same movies, so we can't compare their tastes.")
        return 0

    a = get_ratings_for_common_list(user_dict, user, movies_both_rated)
    b = get_ratings_for_common_list(user_dict, user2, movies_both_rated)

    # Note that this is the same as vector subtraction.
    differences = [a[idx] - b[idx] for idx in range(len(movies_both_rated))]
    squares = [diff ** 2 for diff in differences]
    sum_of_squares = sum(squares)

    return float("%.2f" % (1 / (1 + math.sqrt(sum_of_squares))))


def find_highest_rated_by_similar_users(user_dict, similarity_list, user):
    highest_rated_movies = []
    for i in similarity_list[:25]:
        count = 0
        common = get_common_user_ratings(user_dict, user, i[0])
        # print("\nCommon: ", common)
        # Know what movies they have both rated. common = movieID set
        # while count < 6:
        for r in user_dict[i[0]].ratings[:10]:
            # print("\nStart of i.ratings loop item: ", r)
            if r[0] not in common:
                count += 1
                # print("Count: ", count)
                highest_rated_movies.append((r[0], r[1] * i[1]))

    return sorted(highest_rated_movies[:10], key=sorter, reverse=True)


def get_similarity_list(user_dict, user):
    similarity_list = []
    for userID in user_dict:
        common = get_common_user_ratings(user_dict, user, userID)
        sim = euclidean_distance(user_dict, user, userID, common)
        similarity_list.append((userID, sim))
        # print("\n\nSimilarity list: ", similarity_list)
    # print("\nSorted sim list: ", sorted(similarity_list, key=sorter, reverse=True))
    return sorted(similarity_list, key=sorter, reverse=True)


def print_similar_recommendations(id_to_title, recommendation_list):
    for i, item in enumerate(recommendation_list):
        print("{}. {}".format(i + 1, id_to_title[item[0]]))


def print_title_bar(text):
    print(("#" * (len(text) + 10)))
    print(("#" + ' ' * (len(text) + 8) + '#'))
    print("#    {}    #".format(text))
    print(("#" + ' ' * (len(text) + 8) + '#'))
    print(("#" * (len(text) + 10)) + '\n\n')


def get_user_id(user_dict, greeting):
    user_id = input("Please input your User ID:\n>")
    if is_valid_user_id_input(user_dict, user_id):
        clear()
        return int(user_id)
    else:
        clear()
        print_title_bar(greeting)
        print(("*" * 25) + '\n' + "Enter a valid User ID.\n" + ("*" * 25) + '\n')
        return get_user_id(user_dict, greeting)


def is_valid_user_id_input(user_dict, user_id):
    try:
        int(user_id)
    except:
        return False
    if int(user_id) not in user_dict.keys():
        return False

    return True

def ask_for_track_choice(track_choice_message):
    track = input("Please select from the following options:\n\n1) Browse movie and rating information\n2) Get movie recommendations\n3) Quit\n\n>")

    if is_valid_three_track_input(track):
        return int(track)
    else:
        clear()
        print_title_bar(track_choice_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return ask_for_track_choice(track_choice_message)

def is_valid_three_track_input(track):
    try:
        int(track)
    except:
        return False
    if int(track) != 1 and int(track) != 2 and int(track) != 3:
        return False

    return True


def is_valid_two_track_input(track):
    try:
        int(track)
    except:
        return False
    if int(track) != 1 and int(track) != 2:
        return False

    return True

def ask_for_movie_or_user_track(movie_or_user_info_message):
    track = input("Please select from the following options:\n\n1) Browse movie information\n2) Browse user information\n\n>")

    if is_valid_two_track_input(track):
        clear()
        return int(track)
    else:
        clear()
        print_title_bar(movie_or_user_info_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return ask_for_movie_or_user_track(movie_or_user_info_message)



def does_know_id(movie_or_user_info_message):

    knows = input("Do you know the ID of the movie you want to check? Don't worry if you don't - we'll help you find it!\nJust enter 'Y' for yes or 'N' for no.\n>")
    if check_knows(knows, movie_or_user_info_message):
        clear()
        if knows.lower() == 'y':
            return True
        else:

            return False
    else:
        clear()
        print_title_bar(movie_or_user_info_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return does_know_id(movie_or_user_info_message)


def check_knows(knows, movie_info_message):
    if not knows.isalpha():
        return False
    elif knows.lower() != 'y' and knows.lower() != 'n':
        return False

    return True

def get_movie_id(lets_find_your_movie_message):
    movie_id = input("Please enter the numeric ID for the movie you want to access. If you need to go back to search for the code, enter 0.\n>")
    if is_valid_movie_id(movie_id, lets_find_your_movie_message):
        clear()
        return int(movie_id)
    else:
        clear()
        print_title_bar(lets_find_your_movie_message)
        print(("*" * 25) + '\n' + "Enter a valid Movie ID.\n" + ("*" * 25) + '\n')
        return get_movie_id(lets_find_your_movie_message)


def is_valid_movie_id(movie_id, text):
    try:
        int(movie_id)
    except:
        return False
    if int(movie_id) < 0 or int(movie_id) > 1682:
        return False
    return True

def display_movie_info(movie_dict, movie_id, movie_title, greeting):
    choice = input("Would you like to:\n\n1) See general information about this movie\n2) See ratings for this movie\n>")

    if is_valid_two_track_input(choice):
        clear()
        if int(choice) == 1:
            print_title_bar(movie_title)
            show_general_movie_info(movie_dict, movie_id, movie_title, greeting)
        else:
            print_title_bar(movie_title)
            show_movie_ratings_info(movie_dict, movie_id, movie_title, greeting)
    else:
        clear()
        print_title_bar(movie_title)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return display_movie_info(movie_dict, movie_id, movie_title, greeting)


def show_general_movie_info(movie_dict, movie_id, movie_title, greeting):
    movie = movie_dict[movie_id]
    genres = movie.genres
    print("ID: {}\nAverage Rating: {}\nGenres: {}\nIMDB URL: {}".format(movie_id, movie.average, ', '.join(genres), movie.url))
    print('\n' + '*' * 30)

    option = input("\nFrom here, you can:\n\n1) See ratings details\n2) Return to the main menu\n>")

    if is_valid_two_track_input(option):
        if int(option) == 1:
            clear()
            print_title_bar(movie_title)
            show_movie_ratings_info(movie_dict, movie_id, movie_title, greeting)
        else:
            clear()
            print_title_bar("Hello Again!")
            return ''
    else:
        clear()
        print_title_bar(movie_title)
        print(("*" * 25) + '\n' + "Enter a valid option.\n" + ("*" * 25) + '\n\n')
        return show_general_movie_info(movie_dict, movie_id, movie_title, greeting)


# def is_valid_option_general(option):
#     try:
#         int(option)
#     except:
#         return False
#     if int(option) != 1 and int(option) != 2:
#         return False
#     return True


# def is_valid_option_ratings(option):
#     try:
#         int(option)
#     except:
#         return False
#     if int(option) != 1 and int(option) != 2 and int(option) != 3:
#         return False
#     return True


def show_movie_ratings_info(movie_dict, movie_id, movie_title, greeting, number_to_show=10):
    movie = movie_dict[movie_id]
    print("ID: {}\tTotal ratings: {}\tAverage Rating: {}\n\nTop {} ratings:".format(movie_id, len(movie.ratings), movie.average, number_to_show))
    for i, item in enumerate(movie.ratings[:number_to_show]):
        print("{}. User {} gave it a {}".format((i + 1), item[0], item[1]))
    print('\n' + '*' * 30)

    option = input("\nFrom here, you can:\n\n1) See more ratings\n2) See general movie information\n3) Return to the main menu\n>")

    if is_valid_three_track_input(option):
        if int(option) == 1:
            clear()
            print_title_bar(movie_title)
            number_to_show = get_number_to_show(len(movie.ratings), movie_title)
            show_movie_ratings_info(movie_dict, movie_id, movie_title, greeting, number_to_show)
        if int(option) == 2:
            clear()
            print_title_bar(movie_title)
            show_general_movie_info(movie_dict, movie_id, movie_title, greeting)
        else:
            clear()
            print_title_bar("Hello Again!")
            return ''
    else:
        clear()
        print_title_bar(movie_title)
        print(("*" * 25) + '\n' + "Enter a valid option.\n" + ("*" * 25) + '\n\n')
        return show_movie_ratings_info(movie_dict, movie_id, movie_title, greeting)


def get_number_to_show(total_ratings, text):
    number_to_show = input("How many items would you like to see? {} has {} to show.\n>".format(text, total_ratings))
    if is_valid_number_entry(number_to_show, total_ratings):
        clear()
        print_title_bar(text)
        return int(number_to_show)
    else:
        clear()
        print_title_bar(text)
        print(("*" * 25) + '\n' + "Enter a valid option.\n" + ("*" * 25) + '\n')
        return get_number_to_show(total_ratings, text)


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


def search_for_movies(movie_dict, search_for_movie_message):
    movie = input('Enter all or part of a movie title to search:\n>').lower()

    print("\nMovies containing those words:\n")
    for key in movie_dict:
    	if movie in movie_dict[key].title.lower():
    		print(str(movie_dict[key]))

    print('\n' + '*' * 30)

    choice = input("\nDo you want to:\n1) Enter a code you see\n2) Search again\n>")

    if is_valid_two_track_input(choice):
        if int(choice) == 1:
            # clear()
            # print_title_bar(lets_find_your_movie_message)
            print('')
            return get_movie_id(search_for_movie_message)
        else:
            clear()
            print_title_bar(search_for_movie_message)
            return search_for_movies(movie_dict, search_for_movie_message)
    else:
        clear()
        print_title_bar(search_for_movie_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return search_for_movies(movie_dict, search_for_movie_message)


def get_user_to_look_up(user_dict, find_user_message):
    user_id = input("Enter a User ID to look up. User IDs range from 1 to 943.\n>")

    if is_valid_user_id_input(user_dict, user_id):
        clear()
        return int(user_id)
    else:
        clear()
        print_title_bar(find_user_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return get_user_to_look_up(user_dict, find_user_message)


def display_user_ratings(user_dict, user_id, id_to_title, user_look_up_message, number_to_show=15, sort=0, greeting="Welcome to Movie Heaven!"):
    user = user_dict[user_id]
    print("User {} ({}, {}, {}) has rated {} movies. Showing 1 - {}: \n".format(user_id, user.age, user,sex, user.occupation, len(user.ratings), number_to_show))

    ratings = user.ratings

    if sort == 1:
        new_ratings = []
        for i in ratings:
            new_ratings.append((id_to_title[i[0]], i[1]))
        ratings = sorted(new_ratings)

    if sort == 0:
        for i, rating in enumerate(ratings[:number_to_show]):
            print("{}. {}: {}".format(i + 1, id_to_title[rating[0]], rating[1]))
    else:
        for i, rating in enumerate(ratings[:number_to_show]):
            print("{}. {}: {}".format(i + 1, rating[0], rating[1]))

    print('\n' + '*' * 30)

    option = input("\nFrom here, you can:\n\n1) See more ratings\n2) Toggle sort by movie title or rating\n3) Return to the main menu\n>")

    if is_valid_three_track_input(option):
        if int(option) == 1:
            clear()
            print_title_bar(user_look_up_message)
            number_to_show = get_number_to_show(len(ratings), user_look_up_message)
            display_user_ratings(user_dict, user_id, id_to_title, user_look_up_message, number_to_show, sort)
        if int(option) == 2:
            clear()
            if sort == 1:
                sort = 0
            else:
                sort = 1
            print("Sort: ", sort)
            print_title_bar(user_look_up_message)
            display_user_ratings(user_dict, user_id, id_to_title, user_look_up_message, number_to_show, sort)
        else:
            clear()
            print_title_bar("Hello Again!")
            return ''


def get_top_or_recommend(recommendations_track_message):
    choice = input("Would you like to:\n1) See the highest rated movies\n2) Get personalized recommendations\n>")

    if is_valid_two_track_input(choice):
        clear()
        if int(choice) == 1:
            return 1
        else:
            return 2
    else:
        clear()
        print_title_bar(recommendations_track_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return get_top_or_recommend(recommendations_track_message)


def display_top_rated_movies(movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, filtered=False, number_to_show=10):
    print("Out of the {} movies in the database, these are the top {}.\n".format(len(movie_dict), number_to_show))

    if filtered:
        show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title, number_to_show)
    else:
        show_top_picks_with_title(movie_dict, top_picks, id_to_title, number_to_show)

    print('\n' + '*' * 30)

    option = input("\nFrom here, you can:\n\n1) Display more movies\n2) Filter/Unfilter movies you have already seen\n3) Return to the main menu\n>")

    if is_valid_three_track_input(option):
        if int(option) == 1:
            clear()
            print_title_bar("How many are we looking for?")
            number_to_show = get_number_to_show(len(movie_dict), "The list")

            display_top_rated_movies(movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, filtered, number_to_show)
        elif int(option) == 2:
            clear()
            if filtered == False:
                filtered = True
            else:
                filtered = False
            print_title_bar("These are the top rated movies you haven't seen yet!")
            display_top_rated_movies(movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, filtered, number_to_show)
        elif int(option) == 3:
            clear()
            print_title_bar("Hello Again!")
            return ''
    else:
        clear()
        print_title_bar(top_rated_overall_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return display_top_rated_movies(movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, filtered, number_to_show)


def show_recommendations(id_to_title, recommendation_list, recommended_movies_message, number_to_show=10):
    print("These are the top 10 movies that similar uses have rated highly:\n")
    print_similar_recommendations(id_to_title, recommendation_list)

    option = input("\nPress any key to return to the main menu\n>")
    print('\n' + '*' * 30)

    clear()
    print_title_bar("Hello Again!")
    return ''



def main():
    clear()

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

    print_title_bar(greeting)
    # movie_ratings_dict = {MovieID: [user_id, rating]}
    movie_ratings_dict = get_movie_ratings_dict()
    # print(movie_ratings_dict[1449])
    # movie_dict = {MovieID: MovieObject}
    movie_dict = get_movie_dict(movie_ratings_dict)
    # print(movie_dict[40].genres)
    # id_to_title = {ID: Title}
    id_to_title = set_ids_to_titles(movie_dict)
    # print(id_to_title[2])
    # user_ratings_dict = {UserID:[movie_id, rating]}
    user_ratings_dict = get_user_ratings_dict()
    # print(user_ratings_dict[1])
    # user_dict = {UserID: UserObject}
    user_dict = get_user_dict(user_ratings_dict)
    while True:
        clear()

        print_title_bar(greeting)

        user = get_user_id(user_dict, greeting)

        print_title_bar(track_choice_message)

        track_choice = ask_for_track_choice(track_choice_message)
        if track_choice == 1:
        # """ Info Track """
            clear()
            print_title_bar(movie_or_user_info_message)
            movie_or_user_track = ask_for_movie_or_user_track(movie_or_user_info_message)
            if movie_or_user_track == 1:
                # """ Movie Track """
                print_title_bar(movie_info_message)
                if does_know_id(movie_info_message):
                    # """ Movie Info """
                    print_title_bar(lets_find_your_movie_message)
                    movie_id = get_movie_id(lets_find_your_movie_message)
                    movie_title = id_to_title[movie_id]
                    print_title_bar(movie_title)
                    display_movie_info(movie_dict, movie_id, movie_title, greeting)
                else:
                    # """ Search for Movies """
                    print_title_bar(search_for_movie_message)
                    movie_id = search_for_movies(movie_dict, search_for_movie_message)
                    movie_title = id_to_title[movie_id]
                    print_title_bar(movie_title)
                    display_movie_info(movie_dict, movie_id, movie_title, greeting)
            elif movie_or_user_track == 2:
                # """ User Track """
                clear()
                print_title_bar(find_user_message)
                user_id = get_user_to_look_up(user_dict, find_user_message)
                print_title_bar(user_look_up_message)
                display_user_ratings(user_dict, user_id, id_to_title, user_look_up_message)

        elif track_choice == 2:
            clear()
            print_title_bar(recommendations_track_message)
            top_or_recommend = get_top_or_recommend(recommendations_track_message)
            if top_or_recommend == 1:
                # Top Rated Movies
                top_picks = find_top_picks(movie_dict)
                top_picks_for_user = find_top_picks_for_user(user_dict, top_picks, user)
                top_picks = find_top_picks(movie_dict)

                print_title_bar(top_rated_overall_message)
                display_top_rated_movies(movie_dict, top_picks, top_picks_for_user, id_to_title, top_rated_overall_message, False)

                print_title_bar(top_rated_overall_message)
                show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title)
            else:
                # Recommendations
                print_title_bar(recommended_movies_message)
                # movies_both_rated = get_common_user_ratings(user_dict, user, user2)
                # similarity = euclidean_distance(user_dict, user, user2, movies_both_rated)
                similarity_list = get_similarity_list(user_dict, user)
                recommendation_list = find_highest_rated_by_similar_users(user_dict, similarity_list, user)
                show_recommendations(id_to_title, recommendation_list, recommended_movies_message)
                continue
        else:
            clear()
            print('\n\n')
            print_title_bar("Bye! Come back soon!")
            sleep(2.5)
            break

    clear()




    # top_picks_for_user = find_top_picks_for_user(movie_ratings_dict, user_ratings_dict, top_picks, user)
    # show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title, 40)




if __name__ == '__main__':
    main()
