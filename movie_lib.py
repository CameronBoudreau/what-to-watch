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




def set_ids_to_titles(movie_dict):
    id_to_title = {}
    for i in movie_dict:
        id_to_title[i] = movie_dict[i].title
    return id_to_title


def find_top_picks(movie_dict, number_of_ratings=50):
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

def show_top_picks_with_title(movie_dict, top_picks, id_to_title, number_to_show=10):
    count = 1
    for i in top_picks:
        if count > number_to_show:
            return ''
        print('{}. {}: {}'.format(count, id_to_title[i[0]], i[1]))
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
        if len(common) > 3:
            similarity_list.append((userID, sim))
        # print("\n\nSimilarity list: ", similarity_list)
    # print("\nSorted sim list: ", sorted(similarity_list, key=sorter, reverse=True))
    return sorted(similarity_list, key=sorter, reverse=True)


def print_similar_recommendations(id_to_title, recommendation_list):
    for i, item in enumerate(recommendation_list):
        print("{}. {}".format(i + 1, id_to_title[item[0]]))


def main():
    clear()
    print('\n' + '*' * 30)

    movie_ratings_dict = get_movie_ratings_dict()
    print("\nStep 1.1 - All ratings for Movie ID 138:\n", movie_ratings_dict[138])
    print('\n' + '*' * 30)

    movie_dict = get_movie_dict(movie_ratings_dict)
    print("\nStep 1.2 - Average rating for Movie ID 138: \n", movie_dict[138].average)
    print('\n' + '*' * 30)

    id_to_title = set_ids_to_titles(movie_dict)
    print("\nStep 1.3 - Title from Movie ID 138:\n", id_to_title[138])
    print('\n' + '*' * 30)

    user_ratings_dict = get_user_ratings_dict()

    user_dict = get_user_dict(user_ratings_dict)
    print("\nStep 1.4 - First 10 of all ratings for user 591\n", user_dict[591].ratings[:10])
    print('\n' + '*' * 30)

    top_picks = find_top_picks(movie_dict)
    print("\nStep 3.1 - First 10 values in list of the overall top picks (default 50 ratings to be included):\n")
    show_top_picks_with_title(movie_dict, top_picks, id_to_title, 10)
    print('\n' + '*' * 30)

    user = 25
    user2 = 1

    top_picks_for_user = find_top_picks_for_user(movie_ratings_dict, user_ratings_dict, top_picks, user)
    print("\nStep 3.2 - First 10 values in list of the top_picks_for_user:\n")
    show_top_picks_with_title(movie_dict, top_picks_for_user, id_to_title, 10)
    print('\n' + '*' * 30)

    movies_both_rated = get_common_user_ratings(user_dict, user, user2)
    print("\nStep 4.1 - First 10 values in list of movies that both specified users have rated:\n", movies_both_rated[:10])
    print('\n' + '*' * 30)

    similarity = euclidean_distance(user_dict, user, user2, movies_both_rated)
    print("\nStep 4.2 - Similarity rating of 2 users from euclidean_distance:\n", similarity)
    print('\n' + '*' * 30)

    similarity_list = get_similarity_list(user_dict, user)
    print("\nStep 5.1 - First 10 values in list of all users sorted by those whose taste is most similar to the user: \n", similarity_list[:10])
    print('\n' + '*' * 30)

    recommendation_list = find_highest_rated_by_similar_users(user_dict, similarity_list, user)

    print("\nStep 5.2 - First 10 recommendations based on tastes of similar users:\n")
    print_similar_recommendations(id_to_title, recommendation_list)
    print('\n' + '*' * 30)



if __name__ == '__main__':
    main()
