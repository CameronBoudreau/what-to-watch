

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
