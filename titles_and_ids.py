import csv


def main():

    # with open('README.md', 'a') as w:
    with open('u.data') as f:
        reader = csv.DictReader(f, fieldnames=['user', 'title'], delimiter= '\t')
        for row in reader:
            print(row['user'] + ": " + row['title'] + "\n")



if __name__ == '__main__':
    main()
