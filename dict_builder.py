import csv

class DictBuilder():
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
