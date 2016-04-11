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
        self.ratings = ratings
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
        for i in row[4:]:
            if row[i] == 1:
                self.genres.append(i)




class User:
    def __init__(self, row, ratings):
        self.user_id = int(row['UserID'])
        self.age = int(row['Age'])
        self.sex = row['Sex']
        self.occupation = row['Occupation']
        self.ratings = ratings
        self.highest_rated = self.find_highest_rated(self.ratings)

    def __str__(self):
        return str("{}: Age: {}; Sex: {}; Occupation: {}; Ratings: {}".format(self.user_id, self.age, self.sex, self.occupation, self.ratings))

    def __repr__(self):
        return str(self)

    def find_highest_rated(self, ratings):
        return sorted(ratings, key=sorter, reverse=True)



class Rating:
    def __init__(self, row, ratings):
        self.user_id = int(row['UserID'])
        self.movie_id = int(row['MovieID'])
        self.rating = int(row['Rating'])

    def __str__(self):
        return str("{}: {}".format(self.movie_id, self.rating))

    def __repr__(self):
        return str(self)



def get_movie_dict(movie_ratings_dict):
    with open('u.item', encoding='latin_1') as f:
        movie_dict = {}
        reader = csv.DictReader(f, fieldnames=['MovieID', 'MovieTitle', 'Release', '', 'URL', 'Unknown', 'Action' | 'Adventure' | 'Animation' |
              'Children\'s' | 'Comedy' | 'Crime' | 'Documentary' | 'Drama' | 'Fantasy', 'Film-Noir' | 'Horror' | 'Musical' | 'Mystery' | 'Romance' | 'Sci-Fi' |
              Thriller | War | Western], delimiter='|')
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


def find_top_picks(movie_dict, number_of_ratings=1):
    top_picks = []
    for i in movie_dict:
        if movie_dict[i].number_of_ratings >= number_of_ratings:
            top_picks.append((i, movie_dict[i].average))

    return sorted(top_picks, key=sorter, reverse=True)

def find_top_picks_for_user(movie_ratings_dict, user_ratings_dict, top_picks, user):
    user_top_picks = top_picks
    # print("Rating for first movie to find user picks (is 1 in it?): \n", movie_ratings_dict[318])
    for pick in top_picks:
        for i in movie_ratings_dict[pick[0]]:
            if i[0] == pick[0]:
                user_top_picks.remove(pick)
    return user_top_picks


def sorter(val):
    return val[1]

def show_top_picks_with_title(movie_dict, top_picks, id_to_title, number_to_show=20):
    count = 1
    for i in top_picks:
        if count >= number_to_show:
            return ''
        print(id_to_title[i[0]] + ':', i[1])
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
    if is_valid_user_id_input(user_dict, user_id, greeting):
        return int(user_id)
    else:
        clear()
        print_title_bar(greeting)
        print(("*" * 25) + '\n' + "Enter a valid User ID.\n" + ("*" * 25) + '\n')
        return get_user_id(user_dict, greeting)


def is_valid_user_id_input(user_dict, user_id, greeting):
    try:
        int(user_id)
    except:
        return False
    if int(user_id) not in user_dict.keys():
        return False

    return True

def ask_for_track_choice(track_choice_message):
    track = input("Please select from the following options:\n\n1) Browse movie and rating information\n2) Get movie recommendations\n\n>")

    if is_valid_track_input(track):
        return int(track)
    else:
        clear()
        print_title_bar(track_choice_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return ask_for_track_choice(track_choice_message)

def is_valid_track_input(track):
    try:
        int(track)
    except:
        return False
    if int(track) != 1 and int(track) != 2:
        return False

    return True

def ask_for_movie_or_user_track(movie_or_user_info_message):
    track = input("Please select from the following options:\n\n1) Browse movie information\n2) Browse user information\n\n>")

    if is_valid_track_input(track):
        clear()
        return int(track)
    else:
        clear()
        print_title_bar(movie_or_user_info_message)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return ask_for_movie_or_user_track(movie_or_user_info_message)


# def is_valid_movie_or_user_track_input(track, movie_or_user_info_message):
#     try:
#         int(track)
#     except:
#         return False
#     if int(track) != 1 and int(track) != 2:
#         return False
#
#     return True


def does_know_id(movie_or_user_info_message):

    knows = input("Do you know the ID of the movie you want to check? Don't worry if you don't - we'll help you find it! Just enter 'Y' for yes or 'N' for no.\n>")
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

def get_movie_id(lets_find_your_movie_message, search_for_movie_message):
    movie_id = input("Please enter the numeric ID for the movie you want to access. If you need to go back to search for the code, enter 0.\n>")
    if is_valid_movie_id(movie_id, search_for_movie_message):
        clear()
        return int(movie_id)
    else:
        clear()
        print_title_bar(lets_find_your_movie_message)
        print(("*" * 25) + '\n' + "Enter a valid Movie ID.\n" + ("*" * 25) + '\n')
        return get_movie_id(lets_find_your_movie_message, search_for_movie_message)

def is_valid_movie_id(movie_id):
    try:
        int(movie_id)
    except:
        return False
    if int(movie_id) == 0:
        clear()
        print_title_bar(search_for_movie_message)
        return search_for_movies(search_for_movie_message)
    return True

def display_movie_info(movie_dict, movie_id, movie_title):
    state = input("Would you like to:\n\n1) See general information about this movie\n2) See ratings for this movie\n>")

    if is_valid_track_input(state):
        clear()
        if state = 1:
            print_title_bar(movie_title)
            show_general_movie_info(movie_dict, movie_id, movie_title)
        else:
            print_title_bar(movie_title)
            show_movie_ratings_info(movie_dict, movie_id, movie_title)
    else:
        clear()
        print_title_bar(movie_title)
        print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
        return display_movie_info(movie_dict, movie_id, movie_title)


def show_general_movie_info(movie_dict, movie_id, movie_title):
    print("ID: {}\nAverage Rating: {}\nGenres: {}\n")
    option = input("From here, you can:\n\n1)See ratings details\n2) Look up another movie\n3)Exit to the main menu\n>")




def main():
    clear()
    greeting = "Welcome to Movie Meaven!"
    track_choice_message = "How would you like to explore the collection?"
    movie_or_user_info_message = "What information are you looking for?"
    movie_info_message = "Let's find a movie!"
    lets_find_your_movie_message = "Let's find your movie!"
    search_for_movie_message = "We can help you find what you're looking for!"

    print_title_bar(greeting)
    # movie_ratings_dict = {MovieID: [user_id, rating]}
    movie_ratings_dict = get_movie_ratings_dict()
    # print(movie_ratings_dict[1449])
    # movie_dict = {MovieID: MovieObject}
    movie_dict = get_movie_dict(movie_ratings_dict)
    # print(movie_dict[40])
    # id_to_title = {ID: Title}
    id_to_title = set_ids_to_titles(movie_dict)
    # print(id_to_title[2])
    # user_ratings_dict = {UserID:[movie_id, rating]}
    user_ratings_dict = get_user_ratings_dict()
    # print(user_ratings_dict[1])
    # user_dict = {UserID: UserObject}
    user_dict = get_user_dict(user_ratings_dict)

    user = get_user_id(user_dict, greeting)
    clear()
    print_title_bar(track_choice_message)

    track_choice = ask_for_track_choice(track_choice_message)
    if track_choice == 1:
        clear()
        print_title_bar(movie_or_user_info_message)
        movie_or_user_info = ask_for_movie_or_user_track(movie_or_user_info_message)
        if movie_or_user_info == 1:
            print_title_bar(movie_or_user_info_message)
            if does_know_id(movie_or_user_info_message):
                print_title_bar(lets_find_your_movie_message)
                movie_id = get_movie_id(lets_find_your_movie_message)
                movie_title = id_to_title[movie_id]
                print_title_bar(movie_title)
                display_movie_info(movie_dict, movie_id, movie_title, movie_info_message)
            else:
                print_title_bar(search_for_movie_message)
                search_for_movies(movie_dict)





    # print(user_dict[356].ratings[:3])
    # print("User dict, highest ratings from X: ", user_dict[1].highest_rated)
    top_picks = find_top_picks(movie_dict)
    # print(top_picks[:10])

    # show_top_picks_with_title(movie_dict, top_picks, id_to_title, 30)

    top_picks_for_user = find_top_picks_for_user(movie_ratings_dict, user_ratings_dict, top_picks, user)
    # show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title, 40)
    # print(top_picks_for_user[:20])
    movies_both_rated = get_common_user_ratings(user_dict, user, user2)
    similarity = euclidean_distance(user_dict, user, user2, movies_both_rated)

    similarity_list = get_similarity_list(user_dict, user)
    # print(similarity_list)

    recommendation_list = find_highest_rated_by_similar_users(user_dict, similarity_list, user)
    # print("\nRecommended list: ", recommendation_list)

    print_similar_recommendations(id_to_title, recommendation_list)



if __name__ == '__main__':
    main()
