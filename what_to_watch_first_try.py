import csv
import os
import operator


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



class Movie:
    def __init__(self, row):
        self.id = int(row['MovieID'])
        self.title = row['MovieTitle']

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

    def __repr__(self):
        return str(self)



class User:
    def __init__(self, row):
        self.user_id = int(row['UserID'])
        self.age = int(row['Age'])
        self.sex = row['Sex']
        self.occupation = row['Occupation']

    def __str__(self):
        return str("{}: Age: {}; Sex: {}; Occupation: {}; Zipcode: {}".format(self.user_id, self.age, self.sex, self.occupation, self.zipcode))

    def __repr__(self):
        return str(self)



class Rating:
    def __init__(self, row):
        self.user_id = int(row['UserID'])
        self.movie_id = int(row['MovieID'])
        self.rating = int(row['Rating'])

    def __str__(self):
        return str("{}: {}".format(self.movie_id, self.rating))

    def __repr__(self):
        return str(self)



def get_movie_list():
    with open('u.item', encoding='latin_1') as f:
        movie_list = []
        reader = csv.DictReader(f, fieldnames=['MovieID', 'MovieTitle'], delimiter='|')
        for row in reader:
            movie_list.append(Movie(row))
    return movie_list


def get_movie_ratings_list():
    with open('u.data', encoding='latin_1') as f:
        ratings_list = []
        reader = csv.DictReader(f, fieldnames=['UserID', 'MovieID', 'Rating', 'Time'], delimiter='\t')
        [ratings_list.append(Rating(row)) for row in reader]
    return ratings_list


def get_user_list():
        with open('u.user', encoding='latin_1') as f:
            user_list = []
            reader = csv.DictReader(f, fieldnames=['UserID', 'Age', 'Sex', 'Occupation', "ZipCode"], delimiter='|')
            [user_list.append(User(row)) for row in reader]
        return user_list



def get_user_choice():
    choice = input("Would you like to:\n\n(1)Go to ratings\n\n      OR \n\n(2)Go to recommendations\n\n> ")
    check_get_user_choice(choice)
    return int(choice)


def check_get_user_choice(choice):
    if choice != '1' and choice != '2':
        print("Please choose a valid option. (1 or 2)")
        return get_user_choice()



def get_movie_choice():
    movie_choice = input("Please enter the numeric ID of the movie you want to check: ")
    check_get_movie_choice(movie_choice)
    return int(movie_choice)


def check_get_movie_choice(movie_choice):
    try:
        movie_choice = int(movie_choice)
    except:
        print("Enter a valid numeric ID. See README.md for a list of movies and IDs")
        return get_movie_choice()
    if movie_choice < 0 or movie_choice > 1682:
        print("Enter a valid ID. See README.md for a list of movies and IDs")
        return get_movie_choice()


def get_user_and_rating_list(ratings_list, movie_id, movie):
    all_ratings = []
    for i in ratings_list:
        if i.movie_id == movie.id:
            all_ratings.append((i.rating))
    return all_ratings


def print_movie_ratings(movie_id, movie_list, ratings_list):
    movie = movie_list[movie_id - 1]
    print('\n' + ('*' * 20) + '\n' + movie.title)
    all_ratings = get_user_and_rating_list(ratings_list, movie_id, movie)
    average_rating = get_average_rating(all_ratings)
    print_all_ratings(all_ratings, average_rating)


def print_all_ratings(all_ratings, average_rating):
    count = 0
    print("The average rating from {} user reviews: {}".format(len(all_ratings), average_rating))


def get_average_rating(all_ratings):
    total = 0
    count = 0
    for r in all_ratings:
        total += r
        count += 1
    return ("%.1f" % (total / count))


def get_movies_or_users():
    movies_or_users = input('Do you want to look at ratings by (1)movie or (2)user?\n>')
    check_get_user_choice(movies_or_users)
    return int(movies_or_users)

def find_user_to_look_up():
    user_to_look_up = input("Whose ratings would you like to see? Enter a user number from 1 to 943.\n>")
    check_user_to_look_up(user_to_look_up)
    return int(user_to_look_up)


def check_user_to_look_up(user_to_look_up):
    try:
        user_to_look_up = int(user_to_look_up)
    except:
        print("Enter a valid user ID. Valid IDs are 1-943.")
        return find_user_to_look_up()
    if user_to_look_up < 0 or user_to_look_up > 943:
        print("Enter a valid ID. Valid IDs are 1-943.")
        return find_user_to_look_up()


def get_user_ratings(user, user_list, ratings_list, movie_list):
    for i in user_list:
        if i.user_id == user:
            print("User {}: {}, {} years old. Occupation: {}.\n".format(i.user_id, i.sex, i.age, i.occupation))
    count = 1
    for r in ratings_list:
        if r.user_id == user:
            for m in movie_list:
                if m.id == r.movie_id:
                    print(m.title, "-", r.rating)
                    count += 1
    print("\nUser {} rated {} movies.".format(user, count))


def get_popular_movies(movie_list, ratings_list):
    movies_with_averages = []
    for m in movie_list:
        all_ratings = get_user_and_rating_list(ratings_list, m.id, m)
        average_rating = get_average_rating(all_ratings)
        movies_with_averages.append((m.title, average_rating))
    print(movies_with_averages)
    return movies_with_averages


def get_pop():
    with open('u.data', encoding='latin_1') as f:
        ratings_per_movie = {}
        reader = csv.DictReader(f, fieldnames=['User', 'Movie', 'Rating'], delimiter='\t')
        for row in reader:
            if row['Movie'] in ratings_per_movie:
                ratings_per_movie['Movie'].append(row['Rating'])
            else:
                ratings_per_movie['Movie'] = row['Rating']
    for i in ratings_per_movie:
        i['Movie'] = sum(i['Movie']) / len(i['Movie'])
    top_20 = []
    count = 0
    while count < 20:
        highest = max(ratings_per_movie.keys(), key=(lambda k: stats[k])
        top_20.append(highest, )


def main():
    clear()
    movie_list = get_movie_list()
    ratings_list = get_movie_ratings_list()
    user_list = get_user_list()
    popular = get_pop()
    print(popular)
    # popular_movies = get_popular_movies(movie_list, ratings_list)
    # print(popular_movies)

    print("Hello! Welcome to movie heaven.\n" + ('*' * 20))
    choice = get_user_choice()

    if choice == 1:
        movies_or_users = get_movies_or_users()
        if movies_or_users == 1:
            movie_id = get_movie_choice()
            print_movie_ratings(movie_id, movie_list, ratings_list)
        else:
            user = find_user_to_look_up()
            get_user_ratings(user, user_list, ratings_list, movie_list)

    else:
        pass


if __name__ == '__main__':
    main()
