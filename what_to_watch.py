import csv
import os


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Movie:
    def __init__(self, row):
        self.id = int(row['MovieID'])
        self.title = row['MovieTitle']
        self.average_rating = None

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


def set_ids_to_titles(movie_list):
    id_to_title = {}
    for m in movie_list:
        id_to_title[m.id] = m.title
    return id_to_title




def main():
    movie_list = get_movie_list()
    id_to_title = set_ids_to_titles(movie_list)
    print(id_to_title)



if __name__ == '__main__':
    main()
