import csv
import os
import math


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

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

    def __repr__(self):
        return str(self)

    def find_average_rating(self, ratings):
        total = sum([t[1] for t in ratings])
        return float("%.2f" % (total / len(ratings)))




class User:
    def __init__(self, row, ratings):
        self.user_id = int(row['UserID'])
        self.age = int(row['Age'])
        self.sex = row['Sex']
        self.occupation = row['Occupation']
        self.ratings = ratings

    def __str__(self):
        return str("{}: Age: {}; Sex: {}; Occupation: {}; Ratings: {}".format(self.user_id, self.age, self.sex, self.occupation, self.ratings))

    def __repr__(self):
        return str(self)



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
        reader = csv.DictReader(f, fieldnames=['MovieID', 'MovieTitle'], delimiter='|')
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


# def get_rating_list(movie_ratings_dict, row):
#     rating_list = []
#     for key in movie_ratings_dict:
#         for rating in movie_ratings_dict[key]:
#             if rating[0] == row['UserID']:
#                 rating_list.append(rating)
#     return rating_list



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
    a = set([i[0] for i in user_dict[user1].ratings])

    b = set([i[0] for i in user_dict[user2].ratings])
    common = a & b
    print("\nCommon: ", common)
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

    if len(movies_both_rated) is 0:
        print("Those users have not rated any of the same movies, so we can't compare their tastes.")
        return ''

    a = get_ratings_for_common_list(user_dict, user, movies_both_rated)
    b = get_ratings_for_common_list(user_dict, user2, movies_both_rated)

    # Note that this is the same as vector subtraction.
    differences = [a[idx] - b[idx] for idx in range(len(movies_both_rated))]
    squares = [diff ** 2 for diff in differences]
    sum_of_squares = sum(squares)

    return 1 / (1 + math.sqrt(sum_of_squares))


def main():
    clear()
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
    # print(user_dict[356].ratings[:3])

    #top_picks = [(movie, rating)]
    top_picks = find_top_picks(movie_dict)
    # print(top_picks[:10])
    # print('\nTop: ')

    show_top_picks_with_title(movie_dict, top_picks, id_to_title, 30)
    # print(show_top_picks_with_title([top_picks[:20]], movie_ratings_dict))

    user = 25
    user2 = 1
    top_picks_for_user = find_top_picks_for_user(movie_ratings_dict, user_ratings_dict, top_picks, user)
    # print('\nUser top: ', top_picks_for_user[:3])
    show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title, 40)
    # print('\nUser top: ')
    # print(top_picks_for_user[:20])
    # print('\nShow method top picks: ')
    movies_both_rated = get_common_user_ratings(user_dict, user, user2)
    # print(common_ratings)
    similarity = euclidean_distance(user_dict, user, user2, movies_both_rated)
    print("Similarity: ", similarity)



if __name__ == '__main__':
    main()
